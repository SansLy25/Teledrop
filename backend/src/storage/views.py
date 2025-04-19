from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, GenericAPIView, \
    UpdateAPIView
from rest_framework import mixins
from rest_framework.response import Response

from storage import serializers
from storage.models import Folder


class RootRetrieveView(RetrieveAPIView):
    serializer_class = serializers.RootFolderSerializer

    def get_object(self):
        return Folder.objects.get(owner=self.request.user, parent__isnull=True)


class FolderView(
    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "patch", "delete", "post"]
    serializer_class = serializers.FolderSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['current_folder'] = self.get_object()
        return context

    def get_object(self):
        folder = get_object_or_404(
            Folder,
            owner=self.request.user,
            id=self.kwargs.get("id")
        )
        if self.request.method in ["PATCH", "DELETE"] and folder.is_root():
            raise PermissionDenied("Root folder is immutable")
        return folder

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        user.current_folder = instance
        user.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CurrentFolderView(RetrieveAPIView):
    serializer_class = serializers.FolderSerializer
    def get_object(self):
        user = self.request.user
        if user.current_folder is None:
            user.current_folder = user.root_folder
            user.save()

        return user.current_folder


class FolderMoveView(UpdateAPIView):
    http_method_names = ['post']
    serializer_class = serializers.FolderMoveSerializer

    def get_object(self):
        folder = get_object_or_404(
            Folder,
            owner=self.request.user,
            id=self.kwargs.get("id")
        )
        return folder

    def check_target(self, target):
        if target.parent.owner != self.request.user:
            raise PermissionDenied("Target directory is not your")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            instance=self.get_object()
        )
        serializer.is_valid(raise_exception=True)
        self.check_target(serializer.validated_data['parent'])
        serializer.save()
        return Response(serializer.data, 200)


class FileView(
    GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = serializers.FileSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_object(self):
        return Folder.objects.get(
            parent__owner=self.request.user, id=self.kwargs.get('id')
        )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FileMoveView(UpdateAPIView):
    http_method_names = ['post']
    serializer_class = serializers.FileMoveSerializer

    def check_target(self, folder_id):
        target = get_object_or_404(Folder, id=folder_id)
        if target.parent.owner != self.request.user:
            raise PermissionDenied("Target directory is not your")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            instance=self.get_object()
        )
        serializer.is_valid(raise_exception=True)
        self.check_target(serializer.validated_data['parent'])
        serializer.save()
        return Response(200, serializer.data)

    def get_object(self):
        return Folder.objects.get(
            parent__owner=self.request.user,
            id=self.kwargs.get('id')
        )
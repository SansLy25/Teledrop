from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, GenericAPIView
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

    def get_object(self):
        try:
            folder = Folder.objects.get(
                owner=self.request.user, id=self.kwargs.get("id")
            )
            if self.request.method in ["PATCH", "DELETE"] and folder.is_root():
                raise PermissionDenied("Root folder is immutable")
            return folder
        except Folder.DoesNotExist:
            raise Http404
        except PermissionDenied:
            raise

    def get_serializer_context(self):
        current_folder = self.get_object()
        return {"current_folder": current_folder}

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
from rest_framework.generics import RetrieveAPIView

from users import serializers


class UserProfileView(RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.request.user

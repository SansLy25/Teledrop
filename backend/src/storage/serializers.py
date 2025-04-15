from rest_framework import serializers

from storage.models import Folder, File
from storage.exceptions import ConflictException


class FolderNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["name", "id"]


class FileNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["type", "size", "name"]


class RootFolderSerializer(serializers.ModelSerializer):
    folders = FolderNestedSerializer(many=True)
    files = FileNestedSerializer(many=True)

    class Meta:
        model = Folder
        fields = ["id", "folders", "files"]


class FolderSerializer(serializers.ModelSerializer):
    folders = FolderNestedSerializer(many=True, read_only="True")
    files = FileNestedSerializer(many=True, read_only="True")
    is_root = serializers.BooleanField(required=False, read_only=True)
    path = serializers.CharField(read_only=True)

    class Meta:
        model = Folder
        fields = ["id", "folders", "files", "name", "path", "is_root", "parent"]
        read_only_fields = ["parent", "folders", "files", "parent", 'id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["is_root"] = instance.is_root()
        if not representation["is_root"]:
            representation.pop("is_root")

        return representation

    def check_name_conflicts(self, name, parent):
        if Folder.objects.filter(name=name, parent=parent).exists():
            raise ConflictException()

    def update(self, instance, validated_data):
        self.check_name_conflicts(validated_data.get("name"), instance.parent)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        parent = self.context.get("current_folder")
        name = validated_data.get("name")
        self.check_name_conflicts(name, parent)
        validated_data["parent"] = parent
        return super().create(validated_data)


class FolderMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['parent']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'parent', 'size', 'type', 'name', 'path']
        read_only_fields = ['id', 'size', 'type', 'path', 'parent']


class FileMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['parent']

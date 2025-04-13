from django.db import models

from django.conf import settings


class Folder(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="folders",
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="all_owned_folders",
    )

    users_with_editing_access = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="shared_editable_folders",
    )

    users_with_view_access = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="shared_viewable_folders",
    )

    @property
    def path(self):
        path_segments = []
        folder = self
        while folder.parent is not None:
            path_segments.append(folder.name)
            folder = folder.parent

        return "/" + "/".join(path_segments[::-1])

    def set_parent_owner(self):
        self.owner = self.parent.owner

    def is_root(self):
        return self.parent is None

    def save(self, *args, **kwargs):
        if not hasattr(self, "owner"):
            self.set_parent_owner()

        super().save(*args, **kwargs)


class File(models.Model):
    TYPES = settings.FILE_TYPES

    name = models.CharField(max_length=200)
    telegram_id = models.BigIntegerField()
    size = models.IntegerField()
    type = models.CharField(
        choices=([(type["type"], type["verbose"]) for type in TYPES]),
    )

    parent = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
    )

    @property
    def path(self):
        return self.parent.path + self.name

    def save(self, *args, **kwargs):
        self.type = None
        try:
            extension = self.name.split(".")[-1]

            for type_info in self.TYPES:
                if extension in type_info["extensions"]:
                    self.type = type_info["type"]
                    break
        except IndexError:
            pass

        if self.type is None:
            self.type = "other"

        super().save(*args, **kwargs)

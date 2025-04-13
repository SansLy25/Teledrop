from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from storage.models import Folder

@receiver(post_save, sender=User)
def create_root_folder(sender, instance, created, **kwargs):
    if created and not instance.root_folder:
        folder = Folder.objects.create(name="", owner=instance)
        instance.root_folder = folder
        instance.save(update_fields=["root_folder"])

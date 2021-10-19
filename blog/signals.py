from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post
from django.core.files.storage import default_storage

@receiver(pre_delete,sender=Post)
def delete_profile_pic(sender,instance,**kwargs):
    p = instance
    try:
        if p.image:
            default_storage.delete(p.image.file.name)
    except:
        pass
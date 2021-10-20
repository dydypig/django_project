from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Friend
from django.core.files.storage import default_storage

@receiver(pre_delete,sender=Profile)
def delete_profile_pic(sender,instance,**kwargs):
    p = instance
    try:
        if p.image.file.name != 'default.jpg':
            default_storage.delete(p.image.file.name)
    except:
        pass

@receiver(post_save, sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        Friend.objects.create(user=instance)
    else:
        if hasattr(instance,'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)
        if hasattr(instance,'friend'):
            instance.friend.save()
        else:
            Friend.objects.create(user=instance)
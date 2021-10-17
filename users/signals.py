from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# @receiver(pre_save)
# def set_profile_cache(sender,instance,**kwargs):
#     pass

@receiver(post_save, sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
    else:
        try:
            instance.profile.save()
        except:
            Profile.objects.create(user=instance)
            instance.profile.save()

# @receiver(post_save, sender=User)
# def create_profile(sender,instance,**kwargs):
#     instance.profile.save()
# @receiver(pre_save, sender=User)
# def create_profile(sender,instance,**kwargs):
#     try:
#         instance.profile.save()
#     except AttributeError:
#         Profile.objects.create(user=instance)
#         instance.profile.save()


from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Post, PostCache
from django.core.files.storage import default_storage

@receiver(pre_delete,sender=Post)
def delete_profile_pic(sender,instance,**kwargs):
    p = instance
    try:
        if p.image:
            default_storage.delete(p.image.file.name)
    except:
        pass

@receiver(post_save,sender=Post)
def delete_profile_pic(sender,instance,created,**kwargs):
    if created:
        if instance.image:
            PostCache.objects.create(post=instance, image=instance.image.file.name)
        else:
            PostCache.objects.create(post=instance)
    else:
        pc = PostCache.objects.filter(post=instance).first()
        if pc and instance.image:
            if pc and pc.image and pc.image != instance.image.file.name:
                default_storage.delete(pc.image)
            pc.image = instance.image.file.name
            pc.save()
        elif pc and pc.image:
            default_storage.delete(pc.image)
            pc.image=None
            pc.save()
        elif not pc and instance.image:
            PostCache.objects.create(post=instance, image=instance.image.file.name)
        else:
            PostCache.objects.create(post=instance)
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Post

# @receiver(post_save,sender=Post)
# def delete_profile_pic(sender,instance,**kwargs):
#     p = instance
#     p.num_likes = p.likes.all().count()
#     p.save()
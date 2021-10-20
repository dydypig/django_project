from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_project.utils import image_resize

# Friends Model
class Friend(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,related_name='my_follower', blank=True)
    following = models.ManyToManyField(User,related_name='my_following', blank=True)
    friends = models.ManyToManyField(User,related_name='my_friend',blank=True)
    num_follower = models.IntegerField(default=0)
    num_following = models.IntegerField(default=0)
    # 0:private 1:public 2:local
    privacy = models.SmallIntegerField(default=1)
    
    @staticmethod
    def is_friends(instance,user_obj):
        if instance.user == user_obj:
            return 'Self'
        if user_obj in instance.follower.all() and user_obj in instance.following.all():
            instance.friends.add(user_obj)
            return 'Friend'
        if user_obj in instance.follower.all():
            instance.friends.remove(user_obj)
            return 'Follower'
        if user_obj in instance.following.all():
            instance.friends.remove(user_obj)
            return 'Following'
        instance.friends.remove(user_obj)
        return 'Stranger'

    def __str__(self):
        return f'{self.user.username} Friend'

    def save(self,*args,**kwargs):
        if self.id != None:
            self.num_follower = self.follower.all().count()
            self.num_following = self.following.all().count()
        super().save(*args,**kwargs)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default ='default.jpg',upload_to='profile_pics')
    dob = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # Note super().save function will be also called once in image_resize function.
    # So you have to put super().save function before image_resize. If you did opposite:
    # you will cause problems during creating Profile model. **kwargs will pass an initialization
    # argurment to super.save, if image_resize is called first, then the model will be saved inside
    # image_resize function when you call image.save(). Then **kwargs still pass the initialization
    # parater to super().save() and make it thinks it's creating modelel, witch will eventally fail
    # because it is alread saved and has an primary key already.
    # Model.objects.create() can only do force insert, as Model() can take force insert or update
    # depending on if a primary key is created or not.
    # search for difference between Model.objects.create(user=user) vs Model(user=user)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image.file.name != 'default.jpg':
            image_resize(self.image,300,300)
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_project.utils import image_resize


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
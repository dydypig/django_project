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
    
    def save(self,**kwarg):
        image_resize(self.image,300,300)
        super().save(**kwarg)
        # file = default_storage.open(self.image.name)
        # img = Image.open(file)
        # if img.height > 300 or img.width>300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     file=img.save(self.image.path)
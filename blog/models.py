from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_likes')
    image = models.ImageField(upload_to='blog_pics',null=True, blank=True)
    num_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self,**kwarg):
        if self.id != None:
            self.num_likes = self.likes.all().count()
        super().save(**kwarg)

    # This will be called when a new instance is created and where to go to
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    
class PostCache(models.Model):
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    image = models.TextField(default=None,null=True, blank=True)
    
    def __str__(self):
        return f'{self.post.title} Profile'



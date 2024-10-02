from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Add any additional fields you want
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    



class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()  # Rich text content
    tags = models.CharField(max_length=255, blank=True)  # Optional tags
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Optional image field
    user_id=models.PositiveIntegerField(null=True,blank=True)
    
    

    def __str__(self):
        return self.title

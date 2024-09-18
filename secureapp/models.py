from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    date=models.DateField(auto_now=True)

    def __str__(self):
        return self.file.name
    
class ImageUpload(models.Model):
    image = models.ImageField(upload_to='photos/')
    date=models.DateField(auto_now=True)


    def __str__(self):
        return self.image
# Create your models here.

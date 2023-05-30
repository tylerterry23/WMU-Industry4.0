from django.db import models

# Create your models here.

class HomeContent(models.Model):
    display_photo = models.ImageField(upload_to='display-pics/', default="display-pics/default.jpg")
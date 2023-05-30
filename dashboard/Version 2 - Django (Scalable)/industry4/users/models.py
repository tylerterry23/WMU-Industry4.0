from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Classification(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.DO_NOTHING, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile-pics/', default="profile-pics/default.jpg")
    contribution_year = models.CharField(max_length=200, blank=True, null=True, editable=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # if classification is is not faculty advisor
        if self.classification.name != "Faculty Advisor" and self.contribution_year == "":
            now = datetime.now()
            self.contribution_year = f"{now.year}-{now.year+1}"
        elif self.contribution_year != "":
            self.contribution_year = self.contribution_year
        else:
            self.contribution_year = "N/A"

        super(Profile, self).save(*args, **kwargs)

    @property 
    def imageURL(self):

        try:
            url = self.profile_image.url
        except:
            url = ''

        return url

    class Meta:
        ordering = ['created']

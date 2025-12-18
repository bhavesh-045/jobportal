from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


ROLES_CHOICES = [
    ('student','Student'),
    ('recruiter','Recruiter'),
    ('admin','Admin')
]

def user_profie_path(instance,filename):
    return f'profile_pics/{instance.full_name}/{filename}'

def user_resume_path(instance,filename):
    return f'resumes/{instance.full_name}/{filename}'

class CustomUser(AbstractUser):
    email =  models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,blank=True,null=True)
    profile_image = models.ImageField(upload_to=user_profie_path,default='default_profile.png')
    resume = models.FileField(upload_to=user_resume_path,blank=True,null=True)
    role =models.CharField(max_length=20,choices=ROLES_CHOICES,default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','full_name','role']

    def __str__(self):
        return f"{self.email} ({self.role})"
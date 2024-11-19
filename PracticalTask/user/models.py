from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Not Specified'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True) 

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)


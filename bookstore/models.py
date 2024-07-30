import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils import timezone
class User(AbstractUser):  
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    class Meta:
     swappable = 'AUTH_USER_MODEL'
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(max_length=12, default=datetime.date.today)
    time = models.CharField(max_length=12, default="00:00")
    status = models.BooleanField(default=False)
    controle = models.CharField(max_length=100 , default="")
    time1 = models.CharField(max_length=12, default="00:00")
    time2 = models.CharField(max_length=12, default="00:00")
    is_publisher = models.BooleanField(default=False)
    is_admin= models.BooleanField(default=False)
    urgent = models.CharField(max_length=100 , default="")
    Nands= models.CharField(max_length=100, default="")
    conforme = models.CharField(max_length=100 , default="")
    type = models.CharField(max_length=100 , default="None")
    fiche = models.CharField(max_length=100 , default="None")
    implutation = models.CharField(max_length=100 , default="None")
    UAP= models.CharField(max_length=100, default="")
    time_difference = models.CharField(max_length=100, default="")
    produit= models.CharField(max_length=100, default="")
    def __str__(self):
        return self.title
    def delete(self, *args, **kwargs):
     super().delete(*args, **kwargs) 
class DeleteRequest(models.Model):
    delete_request = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.delete_request
class Feedback(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.feedback



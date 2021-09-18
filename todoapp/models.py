from django.db import models

#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	def __str__(self):
		return self.email

class Task(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, blank=True)
	text = models.CharField(max_length=100)
	is_completed = models.BooleanField(default=False)

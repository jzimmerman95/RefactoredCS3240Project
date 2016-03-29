from django.db import models

# Create your models here.
class UserInformation(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200, default='none')
	email = models.CharField(max_length=200, default='none')
	firstname = models.CharField(max_length=200, default='none')
	lastname = models.CharField(max_length=200, default='none')

from django.db import models

class UserInformation(models.Model):
	username = models.CharField(max_length=200, default='none')
	password = models.CharField(max_length=200, default='none')
	email = models.EmailField(max_length=200, default='none')
	firstname = models.CharField(max_length=200, default='none')
	lastname = models.CharField(max_length=200, default='none')
	publickey = models.CharField(max_length=200, default='none')

class Groups(models.Model):
	groupname = models.CharField(max_length=200, default='none')
	owner = models.CharField(max_length=200, default='none')
	username = models.CharField(max_length=200, default='none')
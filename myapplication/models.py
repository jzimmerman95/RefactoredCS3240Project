from django.db import models

class UserInformation(models.Model):
	username = models.CharField(max_length=200, default='none')
	password = models.CharField(max_length=200, default='none')
	email = models.EmailField(max_length=200, default='none')
	firstname = models.CharField(max_length=200, default='none')
	lastname = models.CharField(max_length=200, default='none')
	def __str__(self):
        return self.username

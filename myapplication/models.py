from django.db import models
from django.utils import timezone
import json

class UserInformation(models.Model):
	username = models.CharField(max_length=200, default='none')
	# password = models.CharField(max_length=200, default='none')
	email = models.EmailField(max_length=200, default='none')
	firstname = models.CharField(max_length=200, default='none')
	lastname = models.CharField(max_length=200, default='none')
	publickey = models.CharField(max_length=200, default='none')
	role = models.CharField(max_length=50, default='user')
	#numSiteManagers = models.IntegerField()

CHOICES = (  
	('yes', 'yes'),
	('no', 'no'),
)

CHOICES2 = (
	('public', 'public'),
	('private', 'private'),
)

class Report(models.Model):
	reportname = models.CharField(max_length=100)
	owner = models.CharField(max_length=100, default="none")
	summary = models.CharField(max_length=200)
	description = models.TextField()
	#containsencrypted = models.CharField(max_length=3, choices=CHOICES, default="no")
	isprivate = models.CharField(max_length=7, choices=CHOICES2, default="public")
	timestamp = models.DateTimeField(default=timezone.now, blank=True)

class ReportFiles(models.Model):
	reportname = models.CharField(max_length=100)
	#isencrypted = models.BooleanField(default=False)
	isencrypted = models.BooleanField(choices=CHOICES, default=False)
	#isencrypted = models.CharField(default="no", max_length=3)
	uploadfile = models.FileField(upload_to='.')

class ReportGroups(models.Model):
	reportname = models.CharField(max_length=100)
	groupname = models.CharField(max_length=200)

class Folders(models.Model):
	foldername = models.CharField(max_length=100)
	owner = models.CharField(max_length=200, default='none')
	reports = models.CharField(max_length=255) # must check if this works

	def setreports(self, x):
		self.reports = json.dumps(x)

	def getreports(self, x):
		return json.loads(self.reports)

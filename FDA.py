import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def promptLogin():
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')
	login(user, pwd)

def login(user, pwd): 
	user = authenticate(username=user, password=pwd)
	if user is not None:
		if user.is_active:
			print("User is active.")
	else: 
		print("That username or password is not valid.")
		print("Type 't' to try again.")
		retry = input()
		if (retry == 't'):
			promptLogin()
		else: 
			print("Communication terminated.")

if __name__=="__main__":
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')

	login(user, pwd)
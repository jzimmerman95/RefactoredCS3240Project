from django import forms
from django.forms import ModelForm
from .models import UserInformation
from django.contrib.auth.models import User

class UserSignUpForm(ModelForm):
	class Meta:
		model = UserInformation
		fields=('username', )

class UserSignInForm(ModelForm):
	class Meta:
		model = User
		fields=('username',)

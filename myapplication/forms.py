from django.forms import ModelForm
from .models import UserInformation

class UserSignUpForm(ModelForm):
        class Meta:
                model = UserInformation
		fields = ['username', 'password', 'email', 'firstname', 'lastname']

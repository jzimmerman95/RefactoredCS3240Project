from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import UserInformation
from .forms import UserSignUpForm

# Create your views here.
def sign_up(request):
	return render(request, 'myapplication/signUp.html', {})

def sign_user_in(request):
	if request.method == 'POST':
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username', '')
			pwd = request.POST.get('password', '')
			email = request.POST.get('email', '')
			fname = request.POST.get('firstname', '')
			lname = request.POST.get('lastname', '')
			user_obj = UserInformation(username = username, password = pwd, email = email, firstname = fname, lastname = lname)
			user_obj.save()
			return HttpResponseRedirect('sign_up')
	else:
		form = UserSignUpForm()
	return render(request, 'signUp.html', {
		'form': UserSignUpForm(),
	})
		

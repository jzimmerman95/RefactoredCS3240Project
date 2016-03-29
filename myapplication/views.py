from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm
from .models import UserInformation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def home_page(request):
	return render(request, 'myapplication/homePage.html', {})

def sign_up(request):
	return render(request, 'myapplication/signUp.html', {})

def sign_user_up(request):
	if request.method == 'POST':
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username', '')
			pwd = request.POST.get('password', '')
			email = request.POST.get('email', '')
			fname = request.POST.get('fname', '')
			lname = request.POST.get('lname', '')
			# insert the user into the  model you created
			user_inf_obj = UserInformation(username = username, password = pwd, email = email, firstname = fname, lastname = lname)
			user_inf_obj.save()
			# create and save a user object for authentication
			user = User.objects.create_user(username=username, password=pwd, first_name=fname, last_name=lname)
			user.save()
			return HttpResponseRedirect('successful_signup')
	else:
		form = UserSignUpForm()
	return render(request, 'myapplication/signUp.html', {'form': form,})

def sign_in(request):
		return render(request, 'myapplication/signIn.html', {})

def sign_user_in(request):
		if request.method == 'POST':
			form = UserSignInForm(request.POST)
			if form.is_valid():
				username=request.POST.get('username', '')
				pwd = request.POST.get('password', '')
				user = authenticate(username=username, password=pwd)
				if user is not None:
    				# the password verified for the user
    				if user.is_active:
    					return HttpResponseRedirect('member_home_page')
					else:
        				return HttpResponseRedirect('sign_in')
				else:
    				# the authentication system was unable to verify the username and password
    				return HttpResponseRedirect('sign_in')

def member_home_page(request):
	return render(request, 'myapplication/memberHomePage.html', {})

def successful_signup(request):
	return render(request, 'myapplication/successfulSignUp.html', {})	

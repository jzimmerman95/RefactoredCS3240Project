from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm
from .models import UserInformation

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
			user_inf_obj = UserInformation(username = username, password = pwd, email = email, firstname = fname, lastname = lname)
			user_inf_obj.save()
			return HttpResponseRedirect('successful_signup')
	else:
		form = UserSignUpForm()
	return render(request, 'myapplication/signUp.html', {'form': form,})

def sign_in(request):
		return render(request, 'myapplication/signIn.html', {})

def successful_signup(request):
	return render(request, 'myapplication/successfulSignUp.html', {})	

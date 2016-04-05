from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm, ReportForm
from .models import UserInformation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# imports for encrytion
from Crypto.PublicKey import RSA
from Crypto import Random

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
			# generate key
			random_generator = Random.new().read
			key = RSA.generate(1024, random_generator)
			publicKey = key.publickey()
			# insert the user into the  model you created, including the generated public key
			user_inf_obj = UserInformation(username = username, password = pwd, email = email, firstname = fname, lastname = lname, publickey = publicKey)
			user_inf_obj.save()
			# create and save a user object for authentication
			user = User.objects.create_user(username=username, password=pwd, first_name=fname, last_name=lname)
			user.save()
			return HttpResponseRedirect('home_page')
	else:
		form = UserSignUpForm()
	return render(request, 'myapplication/signUp.html', {'form': form,})

def sign_in(request):
		return render(request, 'myapplication/signIn.html', {})

def sign_user_in(request):
	username=request.POST.get('username', '')
	pwd = request.POST.get('password', '')
	user = authenticate(username=username, password=pwd)
	if user is not None:
		if user.is_active:
			return render(request, 'myapplication/memberHomePage.html', {})
		else:
			return render(request, 'myapplication/failedLogin.html', {})
	else: 
		return render(request, 'myapplication/failedLogin.html', {})

def member_home_page(request):
	return render(request, 'myapplication/memberHomePage.html', {})

def failed_login(request):
	return render(request, 'myapplication/failedLogin.html', {})

def create_report(request):
	if request.method == 'POST':
	# 	# create a form instance and populate it with data from the request:
	# 	#form = ReportForm(request.POST)
		form = ReportForm(request.POST)
	# 	# check whether it's valid:
		if form.is_valid():
	# 		# process the data in form.cleaned_data as required
			print("Valid form")
		return HttpResponseRedirect('member_home_page')
	# # if a GET (or any other method) we'll create a blank form
	else:
		form = ReportForm()
	return render(request, 'myapplication/createReport.html', {'form': form})	

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm
from .models import UserInformation
from .models import Groups
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# imports for encrytion
from Crypto.PublicKey import RSA
from Crypto import Random
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

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
			publicKey = key.publickey().exportKey()
			# insert the user into the  model you created, including the generated public key
			user_inf_obj = UserInformation(username=username, password=pwd, email=email, firstname=fname, lastname=lname, publickey=publicKey)
			user_inf_obj.save()
			# create and save a user object for authentication
			user = User.objects.create_user(username=username, password=pwd, first_name=fname, last_name=lname)
			user.save()
			# set session username, first name, last name, email, and publickey
			request.session['username'] = username
			request.session['firstname'] = fname
			request.session['lastname'] = lname
			request.session['email'] = email
			request.session['publickey'] = publicKey
			return HttpResponseRedirect('member_home_page')
	else:
		form = UserSignUpForm()
	return render(request, 'myapplication/signUp.html', {'form': form,})

def sign_in(request):
		return render(request, 'myapplication/signIn.html', {})

def sign_user_in(request):
	username = request.POST.get('username', '')
	pwd = request.POST.get('password', '')
	user = authenticate(username=username, password=pwd)
	if user is not None:
		if user.is_active:
			c.execute('SELECT * FROM myapplication_userinformation WHERE username=?', (username,))
			user_data = c.fetchone()
			print(user_data)
			# set session username, first name, last name, email, and publickey
			request.session['username'] = username
			request.session['firstname'] = user_data[3]
			request.session['lastname'] = user_data[4]
			request.session['email'] = user_data[2]
			request.session['publickey'] = user_data[5]
			return render(request, 'myapplication/memberHomePage.html', {'user': user,})
		else:
			return render(request, 'myapplication/failedLogin.html', {})
	else: 
		return render(request, 'myapplication/failedLogin.html', {})

def member_home_page(request):
	return render(request, 'myapplication/memberHomePage.html', {})

def failed_login(request):
	return render(request, 'myapplication/failedLogin.html', {})	

def create_group(request):
	return render(request, 'myapplication/createGroup.html', {})

def create_user_group(request):
	group_name = request.POST.get('groupname', '')
	user = request.session['username']
	group = Groups(groupname=group_name, owner=user, username=user)
	group.save()
	return render(request, 'myapplication/memberHomePage.html', {})


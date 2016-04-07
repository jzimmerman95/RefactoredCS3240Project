from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.servers.basehttp import FileWrapper
from .forms import UserSignUpForm, ReportForm, RenameReportForm
from .models import UserInformation, Report, ReportFiles, ReportGroups
# for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# imports for encrytion
from Crypto.PublicKey import RSA
from Crypto import Random
from django.core.exceptions import ObjectDoesNotExist
# to pass session variables to a template
from django.template import RequestContext


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
		form = ReportForm(request.POST, request.FILES)
		if form.is_valid():
			# create a report object
			reportname = request.POST.get('reportname')
			summary = request.POST.get('summary')
			desc = request.POST.get('description')
			containsEncrypted = request.POST.get('containsencrypted')
			isprivate = request.POST.get('isprivate')
			# use session variables 
			# owner = request.session.get('username')
			# SET DUMMY SESSION VARIABLE
			owner = "username1"

			try:
				r = Report.objects.get(reportname=reportname)
				# A report with that name already exists - send the form back to user with an error
				form = ReportForm(request.POST)
				form.add_error('reportname', "A report with that name already exists: please try a different name")
				return render(request, 'myapplication/createReport.html', {'form': form})
			except ObjectDoesNotExist:
				report_obj = Report(reportname=reportname, owner=owner, summary=summary, description=desc, containsencrypted=containsEncrypted, isprivate=isprivate)
				report_obj.save()
				
				# store all files associated with that report in the file database
				for filename in request.FILES:
					uploadfile=request.FILES[filename]
					report_file_obj=ReportFiles(reportname=reportname, uploadfile=uploadfile)
					report_file_obj.save()

				# store all groups associated with that (private) report in the file database
				if isprivate == "private":
					groups = request.POST.get('groups')
					if groups != "":
						groups = groups.split(',')
						for group in groups:
							group_obj = ReportGroups(reportname=reportname, groupname=group.strip())
							group_obj.save()
				
				return HttpResponseRedirect('manage_reports')				
	# # if a GET (or any other method) we'll create a blank form
	else:
		form = ReportForm()
	return render(request, 'myapplication/createReport.html', {'form': form})

def view_reports(request):
	# SET DUMMY SESSION VARIABLE
	request.session['firstname'] = "Colleen"
	request.session['username'] = "username1"
	return render(request, 'myapplication/viewReports.html', {'reports': Report.objects.all(), 'reportfiles': ReportFiles.objects.all()}, context_instance=RequestContext(request))	

def manage_reports(request):
	if request.method == 'POST':
		form = RenameReportForm(request.POST)
		if form.is_valid():
			# handle form data - rename the report if possible
			oldreportname=request.POST.get('oldreportname')
			newreportname=request.POST.get('newreportname')
			try:
				# see if the report exists
				report = Report.objects.get(reportname=oldreportname)
				# check that a report with the proposed new name does not already exist
				try:
					# report with new proposed name already exists
					reportNameCheck = Report.objects.get(reportname=newreportname)
					form = RenameReportForm(request.POST)
					form.add_error('newreportname', "A report with that name already exists - please enter a different new report name")
					return render(request, 'myapplication/manageReports.html', {'form': form, 'comp': '', 'show': 'show'})
				except ObjectDoesNotExist:
					# there is no error and report may be renamed
					# change the report's name
					report.reportname = newreportname
					report.save()
					# if the report has files, change the name for each associated file
					try: 
						reportFile = ReportFiles.objects.filter(reportname=oldreportname)
						for r in reportFile:
							r.reportname = newreportname
							r.save()
					# otherwise continue
					except ObjectDoesNotExist:
						pass
					# if the report has groups, change the name for each associated group 
					try: 
						reportGroup = ReportGroups.objects.filter(reportname=oldreportname)
						for r in reportGroup:
							r.reportname = newreportname
							r.save()
					# otherwise continue
					except ObjectDoesNotExist:
						pass
			except ObjectDoesNotExist:
				# if report does not exist, pop up an error somehow
				form = RenameReportForm(request.POST)
				form.add_error('oldreportname', "A report with that name does not exist - please enter a valid report name")
				return render(request, 'myapplication/manageReports.html', {'form': form, 'comp': '', 'show': 'show'})
			form = RenameReportForm()
			complete = "The name of " + oldreportname + " has been changed to " + newreportname
			return render(request, 'myapplication/manageReports.html', {'form': form, 'comp': complete, 'show': ''})
	else:
		form = RenameReportForm()
	return render(request, 'myapplication/manageReports.html', {'form': form, 'comp': '', 'show': ''})








from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponseRedirect, HttpResponse
from django.core.servers.basehttp import FileWrapper
from .forms import UserSignUpForm, ReportForm, EditFileForm, EditGroupForm, CreateFolderForm, RenameFolderForm, SearchReportsForm, ResetPassForm, RequestNewKeyPairForm, CreateGroupForm
from .models import UserInformation, Report, ReportFiles, ReportGroups, Folders, Groups, Messages, GroupUsers
# for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# imports for encrytion
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64decode
from django.core.exceptions import ObjectDoesNotExist
# to pass session variables to a template
from django.template import RequestContext

from django.core.files import File 
import os
import mimetypes
from django.contrib import messages
from django.utils import timezone
import ast

# Create your views here.
def home_page(request):
	try: 
		admin = User.objects.get(username='admin')
	except ObjectDoesNotExist:
		# make an admin (site manager) account here 
		# generate key
		random_generator = Random.new().read
		key = RSA.generate(1024, random_generator)
		publicKey = key.publickey().exportKey()
		user_inf_obj = UserInformation(username='admin', email='safecollab@gmail.com', firstname='Admin', lastname='Admin', publickey=publicKey, role='sitemanager', numsitemanagersmade=0)
		user_inf_obj.save()
		user = User.objects.create_user(username='admin', password='adminpass', first_name='Admin', last_name='Admin')
		user.save()
	return render(request, 'myapplication/homePage.html', {})

def sign_user_up(request):
	if request.method == 'POST':
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username', '')
			pwd = request.POST.get('password', '')
			pwd2 = request.POST.get('password2', '')
			email = request.POST.get('email', '')
			fname = request.POST.get('fname', '')
			lname = request.POST.get('lname', '')

			# ensure username is unique
			try: 
				u = UserInformation.objects.get(username=username)
				form.add_error('username', 'That username is taken. Please choose a different username.')
				return render(request, 'myapplication/signUp.html', {'form':form})
			except ObjectDoesNotExist:
				if pwd == pwd2: 
					# generate key
					random_generator = Random.new().read
					key = RSA.generate(1024, random_generator)
					publicKey = key.publickey().exportKey()
					# insert the user into the  model you created, including the generated public key
					user_inf_obj = UserInformation(username = username, email = email, firstname = fname, lastname = lname, publickey = publicKey, role='user', numsitemanagersmade=-1)
					user_inf_obj.save()
					# create and save a user object for authentication
					user = User.objects.create_user(username=username, password=pwd, first_name=fname, last_name=lname)
					user.save()					
					# set session username, first name, last name, email, and publickey
					request.session['username'] = username
					request.session['firstname'] = fname
					request.session['lastname'] = lname
					request.session['email'] = email
					request.session['role'] = 'user'
					request.session['loggedin'] = True
					# # use django's built-in login function to log the user in
					user = authenticate(username=username, password=pwd)
					login(request, user)
					# send user to page with modal pop-up displaying his/her private key, prompt them to write it down
					# format private key
					privateKey = str(key.exportKey())
					privateKey = privateKey.strip()
					privateKey = privateKey.replace(' ', '\r\n')
					return render(request, 'myapplication/showPrivateKey.html', {'pkey':key.exportKey()})
				else: 
					form.add_error('fname', 'Your passwords do not match. Please make sure that your passwords match.')
					return render(request, 'myapplication/signUp.html', {'form':form})
	else:
		form = UserSignUpForm()
	return render(request, 'myapplication/signUp.html', {'form': form})

def show_pkey(request):
	return render(request, 'myapplication/showPrivateKey.html', {})

def sign_in(request):
	return render(request, 'myapplication/signIn.html', {})

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sign_user_in(request):
	username = request.POST.get('username', '')
	pwd = request.POST.get('password', '')
	user = authenticate(username=username, password=pwd)
	if user is not None:
		if user.is_active:
			# set session variables
			userInf = UserInformation.objects.get(username=username)
			request.session['username'] = username
			request.session['firstname'] = userInf.firstname
			request.session['lastname'] = userInf.lastname
			request.session['email'] = userInf.email
			request.session['publickey'] = userInf.publickey
			request.session['role'] = userInf.role
			request.session['loggedin'] = True
			# use django's built-in login method to log the user in
			login(request, user)
			if userInf.role == 'sitemanager':
				return HttpResponseRedirect('admin_home_page')
				#return render(request, 'myapplication/adminHomePage.html', {}, context_instance=RequestContext(request))
			else: 
				return HttpResponseRedirect('member_home_page')
				# passForm = ResetPassForm()
				# keyPairForm = RequestNewKeyPairForm()
				# return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':keyPairForm, 'passForm':passForm}, context_instance=RequestContext(request))
		else:
			return render(request, 'myapplication/failedLogin.html', {}, )
	else: 
		return render(request, 'myapplication/failedLogin.html', {})

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
#@login_required
def member_home_page(request):
	if 'loggedin' in request.session:
		# the user is logged in 
		passForm = ResetPassForm()
		keyPairForm = RequestNewKeyPairForm()
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':keyPairForm, 'passForm':passForm}, context_instance=RequestContext(request))
	else: 
		return HttpResponseRedirect('home_page')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home_page(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		return render(request, 'myapplication/adminHomePage.html', {}, context_instance=RequestContext(request))
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def admin_manage_reports(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		return render(request, 'myapplication/adminManageReports.html', {}, context_instance=RequestContext(request))
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def failed_login(request):
	return render(request, 'myapplication/failedLogin.html', {})	

def create_group(request):
	if 'loggedin' in request.session:
		form = CreateGroupForm()
		form.setChoices(request)
		return render(request, 'myapplication/createGroup.html', {'form': form,})
	else: 
		return HttpResponseRedirect('home_page')

def create_user_group(request):
	if 'loggedin' in request.session: 
		if request.method == 'POST':
			form = CreateGroupForm(request.POST)

		group_name = request.POST.get('groupname', '')
		user = request.session['username']

		if (Groups.objects.filter(groupname=group_name).exists()):
			form.add_error('groupname', 'The group name you entered is already taken. Please enter a new one.')
		else:
			group = Groups(groupname=group_name, owner=user, username=user)
			group.save()
			users = request.POST.getlist('users')
			for user in users:
				group_users_obj = GroupUsers(groupname=group.groupname, username=user)
				group_users_obj.save()

		form = CreateGroupForm(request.POST)
		form.setChoices(request)

		members = {}
		for group in Groups.objects.all():
			members[group.groupname] = []
			for member in GroupUsers.objects.filter(groupname=group.groupname):
				members[group.groupname].append(member.username)

		if request.session['role']=='sitemanager':
			return render(request, 'myapplication/adminViewGroups.html', {'form': form, 'members': members})
		else:
			user = request.session['username']
			groups = Groups.objects.all().filter(username=user)
			return render(request, 'myapplication/ViewGroups.html', {'groups': groups, 'form': form, 'members': members})
	else: 
		return HttpResponseRedirect('home_page')

def admin_view_groups(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		members = {}
		for group in Groups.objects.all():
			members[group.groupname] = []
			for member in GroupUsers.objects.filter(groupname=group.groupname):
				members[group.groupname].append(member.username)
		return render(request, 'myapplication/adminViewGroups.html', {'groups':Groups.objects.all(), 'members': members})
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def manage_groups(request):
	user = request.session['username']
	groups = Groups.objects.all().filter(username=user)
	form = CreateGroupForm(request.POST)
	form.setChoices(request)
	groupNames = []
	members = {}
	for group in Groups.objects.all():
		groupNames.append(group.groupname)
		members[group.groupname] = []
		for member in GroupUsers.objects.filter(groupname=group.groupname):
			members[group.groupname].append(member.username)

	return render(request, 'myapplication/ViewGroups.html', {'groups': Groups.objects.all(), 'form': form, 'groupNames': groupNames, 'members': members})

def view_groups(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			oldgroupname = request.POST.get('oldgroupname')
			groupname = request.POST.get('groupname')

			g = Groups.objects.get(groupname=oldgroupname)
			g.groupname = groupname
			g.save()

	else:
		pass 

	users = request.POST.getlist('users')
	for user in users:
		group_users_obj = GroupUsers(groupname=groupname, username=user.username)
		group_users_obj.save()

	groupNames = []
	for group in Groups.objects.all():
		groupNames.append(group.groupname)
	form = CreateGroupForm()
	form.setChoices(request)
	return render(request, 'myapplication/viewGroups.html', {'form': form, 'groups': Groups.objects.all(), 'groupNames': groupNames})	


def admin_delete_group(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		if request.method == "POST":
			reportToDelete = request.POST.get('deleteGroup')
			inst = Groups.objects.get(groupname=reportToDelete)
			inst.delete()
		return render(request, 'myapplication/adminViewGroups.html', {'groups':Groups.objects.all()})
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def delete_group(request):
	if request.method == "POST":
		reportToDelete = request.POST.get('deleteGroup')
		inst = Groups.objects.get(groupname=reportToDelete)
		if GroupUsers.objects.filter(groupname=reportToDelete).exists():
			for user in GroupUsers.objects.filter(groupname=reportToDelete):
				user.delete()
		inst.delete()

	members = {}
	for group in Groups.objects.all():
		members[group.groupname] = []
		for member in GroupUsers.objects.filter(groupname=group.groupname):
			members[group.groupname].append(member.username)

	form = CreateGroupForm(request.POST)
	form.setChoices(request)

	return render(request, 'myapplication/viewGroups.html', {'groups':Groups.objects.all(), 'members': members, 'form': form})

def add_users_to_group(request):
	users = request.POST.getlist('users')
	for user in users:
		user_obj = GroupUsers(groupname=request.POST["addUsers"], username=user)
		user_obj.save()

	members = {}
	for group in Groups.objects.all():
		members[group.groupname] = []
		for member in GroupUsers.objects.filter(groupname=group.groupname):
			members[group.groupname].append(member.username)

	form = CreateGroupForm(request.POST)
	form.setChoices(request)

	if request.session['role']=='sitemanager':
		return render(request, 'myapplication/adminViewGroups.html', {'groups': Groups.objects.all(), 'form': form, 'members': members})
	else:
		user = request.session['username']
		groups = Groups.objects.all().filter(username=user)
		return render(request, 'myapplication/ViewGroups.html', {'groups': groups, 'form': form, 'members': members})

def delete_users_from_group(request):
	users = request.POST.getlist('users')
	for user in users:
		user_obj = GroupUsers.objects.filter(groupname=request.POST['deleteUsers'], username=user)
		user_obj.delete()

	members = {}
	for group in Groups.objects.all():
		members[group.groupname] = []
		for member in GroupUsers.objects.filter(groupname=group.groupname):
			members[group.groupname].append(member.username)

	form = CreateGroupForm(request.POST)
	form.setChoices(request)

	if request.session['role']=='sitemanager':
		return render(request, 'myapplication/adminViewGroups.html', {'groups': Groups.objects.all(), 'form': form, 'members': members})
	else:
		user = request.session['username']
		groups = Groups.objects.all().filter(username=user)
		return render(request, 'myapplication/ViewGroups.html', {'groups': groups, 'form': form, 'members': members})


def create_report(request):
	if 'loggedin' in request.session:
		if request.method == 'POST':
			form = ReportForm(request.POST, request.FILES)
			form.setChoices(request)
			if form.is_valid():
				# create a report object
				reportname = request.POST.get('reportname')
				summary = request.POST.get('summary')
				desc = request.POST.get('description')
				# containsEncrypted = request.POST.get('containsencrypted')
				isprivate = request.POST.get('isprivate')
				# TODO: get session variables 
				owner = request.session.get('username')
				# SET DUMMY SESSION VARIABLE
				# owner = "username1"

				try:
					r = Report.objects.get(reportname=reportname)
					# A report with that name already exists - send the form back to user with an error
					form = ReportForm(request.POST)
					form.add_error('reportname', "A report with that name already exists: please try a different name")
					return render(request, 'myapplication/createReport.html', {'form': form})
				except ObjectDoesNotExist:
					report_obj = Report(reportname=reportname, owner=owner, summary=summary, description=desc, isprivate=isprivate) #containsencrypted=containsEncrypted,
					report_obj.save()
					
					for filename in request.FILES:
						index = filename.strip('extra_field_')
						if 'extra_isencrypted_'+index not in request.POST.keys():
							isenc = "off"
							uploadfile=request.FILES[filename]
							report_file_obj=ReportFiles(reportname=reportname, uploadfile=uploadfile, isencrypted=False)
							report_file_obj.save()
						else: 
							isenc = request.POST['extra_isencrypted_'+index]
							uploadfile=request.FILES[filename]
							report_file_obj=ReportFiles(reportname=reportname, uploadfile=uploadfile, isencrypted=""+isenc)
							report_file_obj.save()

					# store all groups associated with that (private) report in the file database
					groups = request.POST.getlist('groups')
					for group in groups:
						report_group_obj = ReportGroups(reportname=reportname, groupname=group)
						report_group_obj.save()
					return HttpResponseRedirect('manage_reports')				
		else:
			form = ReportForm()
			form.setChoices(request)
		return render(request, 'myapplication/createReport.html', {'form': form})
	else: 
		return HttpResponseRedirect('home_page')

def admin_view_reports(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		return render(request, 'myapplication/adminViewReports.html', {'reports':Report.objects.all(), 'reportfiles':ReportFiles.objects.all()}, context_instance=RequestContext(request))
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def admin_manage_users(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		return render(request, 'myapplication/adminManageUsers.html', {'users':User.objects.all(), 'userInf':UserInformation.objects.all()}, context_instance=RequestContext(request))
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def admin_suspend_user(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		if request.method == 'POST':
			u = request.POST['username']
			user = User.objects.get(username=u)
			if user.is_active:
				user.is_active = False
				user.save()
			else:
				user.is_active = True
				user.save()
		return render(request, 'myapplication/adminManageUsers.html', {'users':User.objects.all(), 'userInf':UserInformation.objects.all()}, context_instance=RequestContext(request)) 
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def admin_make_sitemanager(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		if request.method == 'POST': 
			u = request.POST['username']
			sm = request.POST['sm']
			smInf = UserInformation.objects.get(username=sm)
			if smInf.numsitemanagersmade < 3:
				userToChange = UserInformation.objects.get(username=u)
				userToChange.role = "sitemanager"
				userToChange.numsitemanagersmade = 0
				userToChange.save()
				smInf.numsitemanagersmade = smInf.numsitemanagersmade + 1
				smInf.save()
				error = "None"
			else: 
				error = "You have already made three users site managers."
		return render(request, 'myapplication/adminManageUsers.html', {'error': error, 'users':User.objects.all(), 'userInf':UserInformation.objects.all()}, context_instance=RequestContext(request)) 
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def view_shared_reports(request):
	if 'loggedin' in request.session:
		username = request.session.get('username')
		sharedReports = []
		for group in Groups.objects.filter(username=username):
			for r in ReportGroups.objects.filter(groupname=group.groupname):
				rep = Report.objects.get(reportname=r.reportname)
				sharedReports.append(rep)
		return render(request, 'myapplication/viewSharedReports.html', {'reports': sharedReports, 'reportfiles':ReportFiles.objects.all()})
	else: 
		return HttpResponseRedirect('home_page')

def view_reports(request):
	if 'loggedin' in request.session:
		if request.method == 'POST':
			form = ReportForm(request.POST)
			if form.is_valid():
				#newreportname = request.POST.get('newreportname')
				oldreportname = request.POST.get('oldreportname')
				reportname = request.POST.get('reportname')
				summary = request.POST.get('summary')
				desc = request.POST.get('description')
				#containsEncrypted = request.POST.get('containsencrypted')
				isprivate = request.POST.get('isprivate')

				r = Report.objects.get(reportname=oldreportname)
				r.reportname = reportname
				r.summary = summary
				r.description = desc
				#r.containsEncrypted = containsEncrypted
				r.isprivate = isprivate
				r.save()
				try: 
					r2 = ReportFiles.objects.filter(reportname=oldreportname)
					for rep in r2:
						rep.reportname = reportname
						rep.save()
				except ObjectDoesNotExist:
					pass
				try:
					r3 = ReportGroups.objects.filter(reportname=oldreportname)
					for rep in r3:
						rep.reportname = reportname
						rep.save()
				except ObjectDoesNotExist:
					pass
				# Modify report name in folder(s) if necessary
				for folder in Folders.objects.all():
					reportList = folder.reports.split(',')
					for r in reportList:
						if r.strip() == oldreportname:
							reportList.remove(r)
							reportList.append(reportname)
							folder.reports = ",".join(str(x) for x in reportList)
							folder.save()

				HttpResponseRedirect('view_reports')
			else:
				HttpResponseRedirect('home_page')
		else:
			pass 
		# form = RenameReportForm()
		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else: 
		return HttpResponseRedirect('home_page')

def view_reports_folder(request):
	if 'loggedin' in request.session:
		form = CreateFolderForm()
		renameForm = RenameFolderForm()
		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReportsFolder.html', {'renameForm': renameForm, 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('home_page')

def rename_folder(request):
	if 'loggedin' in request.session:
		if request.method == 'POST':
			renameForm = RenameFolderForm(request.POST)
			if renameForm.is_valid():
				newfoldername = request.POST.get('newfoldername')
				oldfoldername = request.POST.get('foldertorename')
				folderError = False
				# check that the new folder name does not exist
				for f in Folders.objects.all():
					if f.foldername == newfoldername:
						folderError = True
				if folderError == True:
					# return with error
					form = CreateFolderForm()
					# renameForm = RenameFolderForm()
					renameForm.add_error('newfoldername', 'A folder with that name already exists. Please choose a different folder name.')
					folderInfo = []
					for folder in Folders.objects.all():
						tup = [folder.foldername, folder.owner]
						folderInfo.append(tup)
					return render(request, 'myapplication/viewReportsFolder.html', {'showRenameForm': 'showRenameForm', 'renameForm': renameForm, 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))

				else: 
					# update folder name
					fol = Folders.objects.get(foldername=oldfoldername)
					fol.foldername = newfoldername
					fol.save()
		else: 
			pass
		form = CreateFolderForm()
		renameForm = RenameFolderForm()
		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReportsFolder.html', {'renameForm': renameForm, 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))
	else: 
		return HttpResponseRedirect('home_page')

def delete_folder(request):
	if 'loggedin' in request.session:
		if request.method=="POST":
			foldertodelete = request.POST.get('foldertodelete')
			f = Folders.objects.get(foldername=foldertodelete)
			f.delete()
		form = CreateFolderForm()
		renameForm = RenameFolderForm()
		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReportsFolder.html', {'renameForm': renameForm, 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('home_page')

def admin_delete_report(request):
	if 'loggedin' in request.session and request.session['role'] == 'sitemanager':
		if request.method == "POST":
			reportToDelete = request.POST.get('deleteReport')
			inst = Report.objects.get(reportname=reportToDelete)
			inst.delete()
			try:
				r_files = ReportFiles.objects.filter(reportname=reportToDelete)
				for rep in r_files:
					rep.delete()
			except ObjectDoesNotExist:
				pass
			try: 
				r_groups = ReportGroups.objects.filter(reportname=reportToDelete)
				for rep in r_groups:
					rep.delete()
			except ObjectDoesNotExist:
				pass
			# delete report from folder(s) if necessary
			for folder in Folders.objects.all():
				reportList = folder.reports.split(',')
				for r in reportList:
					if r.strip() == reportToDelete:
						reportList.remove(r)
						folder.reports = ",".join(str(x) for x in reportList)
						folder.save()
			# HttpResponseRedirect('view_reports')
		else: 
			pass 
		return render(request, 'myapplication/adminViewReports.html', {'reports':Report.objects.all()}, context_instance=RequestContext(request))
	elif 'loggedin' in request.session:
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':RequestNewKeyPairForm(), 'passForm':ResetPassForm()})
	else: 
		return HttpResponseRedirect('home_page')

def delete_report(request):
	if 'loggedin' in request.session:
		if request.method == "POST":
			reportToDelete = request.POST.get('deleteReport')
			inst = Report.objects.get(reportname=reportToDelete)
			inst.delete()
			try:
				r_files = ReportFiles.objects.filter(reportname=reportToDelete)
				for rep in r_files:
					rep.delete()
			except ObjectDoesNotExist:
				pass
			try: 
				r_groups = ReportGroups.objects.filter(reportname=reportToDelete)
				for rep in r_groups:
					rep.delete()
			except ObjectDoesNotExist:
				pass
			# delete report from folder(s) if necessary
			for folder in Folders.objects.all():
					reportList = folder.reports.split(',')
					for r in reportList:
						if r.strip() == reportToDelete:
							reportList.remove(r)
							folder.reports = ",".join(str(x) for x in reportList)
							folder.save()
			# HttpResponseRedirect('view_reports')
		else: 
			pass 
		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect('home_page')

def add_files(request):
	if 'loggedin' in request.session: 
		if request.method == "POST":
			fileForm = EditFileForm(request.POST, request.FILES)
			if fileForm.is_valid():
				# get the report name
				reportname = request.POST.get('fileeditreportname')
				# store all files associated with that report in the file database

				for filename in request.FILES:
					index = filename.strip('extra_field_')
					if 'extra_isencrypted_'+index not in request.POST.keys():
						uploadfile=request.FILES[filename]
						report_file_obj=ReportFiles(reportname=reportname, uploadfile=uploadfile, isencrypted=False)
						report_file_obj.save()
					else: 
						isenc = request.POST['extra_isencrypted_'+index]
						uploadfile=request.FILES[filename]
						report_file_obj=ReportFiles(reportname=reportname, uploadfile=uploadfile, isencrypted=""+isenc)
						report_file_obj.save()
		else: 
			pass

		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect('home_page')

def remove_files(request):
	if 'loggedin' in request.session:
		if request.method == "POST":
			fileForm = EditFileForm(request.POST, request.FILES)
			if fileForm.is_valid():
				reportname = request.POST.get('fileeditreportname')
				filestoremove = request.POST.get('filestoremove').split(',')
				filesWithErrors = []
				for f in filestoremove:
					try: 
						fileObj = ReportFiles.objects.get(uploadfile=f.strip())
						fileObj.delete()
					except ObjectDoesNotExist:
						filesWithErrors.append(f)
				if len(filesWithErrors) > 0:
					# there were invalid file names
					form = ReportForm()
					fileForm = EditFileForm(request.POST)
					groupForm = EditGroupForm()
					createFolderForm = CreateFolderForm()
					fileForm.add_error('filestoremove', "There was at least one invalid file name")
					reportNames = []
					for report in Report.objects.all():
						reportNames.append(report.reportname)

					folderInfo = []
					for folder in Folders.objects.all():
						tup = [folder.foldername, folder.owner]
						folderInfo.append(tup)
					return render(request, 'myapplication/viewReports.html', {'show': 'show', 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
		else: 
			pass
		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect('home_page')

def edit_groups(request):
	if 'loggedin' in request.session:
		if request.method == "POST":
			groupForm = EditGroupForm(request.POST)
			if groupForm.is_valid():
				reportname = request.POST.get('editgroupsreportname')
				groupstoadd = request.POST.get('groupstoadd').split(',')
				groupstoremove = request.POST.get('groupstoremove').split(',')
				# TODO: get session variables 
				owner = request.session.get('username')
				# SET DUMMY SESSION VAR
				# owner = "username1"
				# TODO: check that groups to add the report to a) exist and b) are owned by this owner
				# TODO: check that groups to remove the report from a) contain the report now
				pass
		else:
			pass
		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()
		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect('home_page')

def manage_reports(request):
	if 'loggedin' in request.session: 
		searchForm = SearchReportsForm();
		return render(request, 'myapplication/manageReports.html', {'searchForm':searchForm})
	else: 
		return HttpResponseRedirect('home_page')

def create_folder(request):
	if 'loggedin' in request.session: 
		if request.method == "POST":
			form = CreateFolderForm(request.POST)
			if form.is_valid():
				# TODO: get session username to 
				username = request.session.get('username')
				# for now, dummy variable 
				# username = "username1"
				foldername = request.POST.get('foldername')
				reports = request.POST.get('reports')
				error = False
				if reports != '':
					reportList = reports.split(',')
					for r in reportList:
						try:
							rep = Report.objects.get(reportname=r.strip())
							if rep.owner != username:
								# the existing report does not belong to the user - send form back with error
								error = True
						except ObjectDoesNotExist:
							# at least one report does not exist - send form back with error 
							error = True
				if error == False:
					# you can make the folder with reports
					folder_obj = Folders(foldername=foldername, reports=reports, owner=username)
					folder_obj.save()
				else:
					#form = CreateFolderForm()
					form.add_error('reports', "At least one report does not belong to you or does not exist. Please enter valid report names.")
					folderInfo = []
					for folder in Folders.objects.all():
						tup = [folder.foldername, folder.owner]
						folderInfo.append(tup)
					return render(request, 'myapplication/viewReportsFolder.html', {'show':'show', 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))
		else:
			pass
		form = CreateFolderForm()
		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReportsFolder.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('home_page')

def add_reports_folder(request):
	if 'loggedin' in request.session:
		if request.method == "POST":
			createFolderForm = CreateFolderForm(request.POST)
			if createFolderForm.is_valid():
				# TODO: get session username to 
				username = request.session.get('username')
				# for now, dummy variable 
				# username = "username1"
				foldername = request.POST.get('foldername')
				reports = request.POST.get('reports')
				reportsToAddList = reports.split(',')
				# errorFolder = False
				errorReports = False
				for r in reportsToAddList:
					try:
						rep = Report.objects.get(reportname=r.strip())
						if rep.owner != username:
							# the existing report does not belong to the user - send form back with error
							errorReports = True
					except ObjectDoesNotExist:
						# at least one report does not exist - send form back with error 
						errorReports = True
				if errorReports == False:
					# you can add those reports to the folder's reports
					f = Folders.objects.get(foldername=foldername)
					existingReportsList = f.reports.split(',')
					for r in reportsToAddList:
						if r.strip() not in existingReportsList:
							existingReportsList.append(r)
					f.reports = ",".join(str(x) for x in existingReportsList)
					f.save()	
				else:
					createFolderForm=CreateFolderForm(request.POST)
					createFolderForm.add_error('reports', "At least one report does not belong to you or does not exist. Please enter valid report names.")
					
					form = ReportForm()
					fileForm = EditFileForm()
					groupForm = EditGroupForm()

					reports = []
					if request.method == "POST": 
						folderName = request.POST.get('foldername')
						if (folderName != 'None') and (folderName != '') and (folderName != None):
							f = Folders.objects.get(foldername=(request.POST.get('foldername')))
							if len(f.reports) > 0:
								l = f.reports.split(',')
								for r in l:
									if r.strip() != '':
										reports.append(Report.objects.get(reportname=r.strip()))
						else: 
							reports = Report.objects.all()
					else: 
						reports = Report.objects.all()

					reportNames = []
					for report in Report.objects.all():
						reportNames.append(report.reportname)

					folderInfo = []
					for folder in Folders.objects.all():
						tup = [folder.foldername, folder.owner]
						folderInfo.append(tup)
					return render(request, 'myapplication/viewReports.html', {'show2':'show2', 'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
		else:
			pass

		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		createFolderForm = CreateFolderForm()
		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else: 
		return HttpResponseRedirect('home_page')

def remove_report_folder(request):
	if 'loggedin' in request.session:
		if request.method == "POST":
			reportToDelete = request.POST.get('deleteReport')
			folderName = request.POST.get('foldername')
			f = Folders.objects.get(foldername=folderName)
			reportsList = f.reports.split(',')
			for r in reportsList:
				if r.strip() == reportToDelete:
					reportsList.remove(r)
			# reportsList.remove(reportToDelete.strip())
			f.reports = ",".join(str(x) for x in reportsList)
			f.save()
			HttpResponseRedirect('view_reports')
		else: 
			pass 
		form = ReportForm()
		fileForm = EditFileForm()
		groupForm = EditGroupForm()
		createFolderForm = CreateFolderForm()

		reports = []
		if request.method == "POST": 
			folderName = request.POST.get('foldername')
			if (folderName != 'None') and (folderName != '') and (folderName != None):
				f = Folders.objects.get(foldername=(request.POST.get('foldername')))
				if len(f.reports) > 0:
					l = f.reports.split(',')
					for r in l:
						if r.strip() != '':
							reports.append(Report.objects.get(reportname=r.strip()))
			else: 
				reports = Report.objects.all()
		else: 
			reports = Report.objects.all()

		reportNames = []
		for report in Report.objects.all():
			reportNames.append(report.reportname)

		folderInfo = []
		for folder in Folders.objects.all():
			tup = [folder.foldername, folder.owner]
			folderInfo.append(tup)
		return render(request, 'myapplication/viewReports.html', {'folderInfo': folderInfo, 'folders': Folders.objects.all(), 'createFolderForm': createFolderForm, 'folderName': request.POST.get('foldername'), 'form': form, 'fileForm': fileForm, 'groupForm': groupForm, 'reports': reports, 'reportfiles': ReportFiles.objects.all(), 'reportgroups': ReportGroups.objects.all(), 'reportNames': reportNames}, context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect('home_page')

def log_out(request):
	logout(request)
	return render(request, 'myapplication/signIn.html', {})

def download_unencrypted_files(request):
	if 'loggedin' in request.session:
		filename = request.POST.get('fileToDownload')
		f = ReportFiles.objects.get(uploadfile=filename).uploadfile

		path = f.path # Get file path
		wrapper = FileWrapper( open( path, "rb" ) )
		content_type = mimetypes.guess_type( path )[0]

		response = HttpResponse(wrapper, content_type = content_type)
		response['Content-Length'] = os.path.getsize( path )
		fname, file_extension = os.path.splitext(path)
		response['Content-Disposition'] = 'attachment; filename='+filename
		return response
	else:
		return HttpResponseRedirect('home_page')

def search_reports(request):
	if 'loggedin' in request.session:
		if request.method == 'POST':
			searchForm = SearchReportsForm(request.POST)
			if searchForm.is_valid():
				user = request.session.get('username')

				reportsForUser = []
				# add all public reports
				for report in Report.objects.all():
					if report.isprivate == 'public':
						reportsForUser.append(report)
					if report.isprivate == 'private' and report.owner == user:
						reportsForUser.append(report)
				# add all private reports shared with user
				for group in Groups.objects.filter(username=user):
					# add all of the reports that are shared with that group
					for rep in ReportGroups.objects.filter(groupname=group.groupname):
						r = Report.objects.get(reportname=rep.reportname)
						if r not in reportsForUser:
							reportsForUser.append(r)

				searchterms = request.POST.get('searchTerms')
				nameError = False
				reportName = ""
				reportOwner =""
				reportAvail = ""
				reportsToReturn = []
				if "AND" in searchterms:
					searchterms = searchterms.split('AND')
					for term in searchterms:
						termPair = term.split(':')
						if termPair[0].strip() == 'reportname':
							reportName = termPair[1].strip()
							print(reportName)
						elif termPair[0].strip() == 'owner':
							reportOwner = termPair[1].strip()
						elif termPair[0].strip() == 'availability':
							reportAvail = termPair[1].strip()
						else:
							# there is an error in the listing of terms 
							nameError = True

					if reportName != "" and reportOwner != "" and reportAvail != "":
						report = Report.objects.get(reportname=reportName)
						if report.owner == reportOwner and report.isprivate == reportAvail:
							# check that the user has access
							if report in reportsForUser:
								reportsToReturn.append(report)
					elif reportName != "" and reportOwner != "":
						report = Report.objects.get(reportname=reportName)
						if report.owner == reportOwner:
							if report in reportsForUser:
								reportsToReturn.append(report)
					elif reportName != "" and reportAvail != "":
						report = Report.objects.get(reportname=reportName)
						if report.isprivate == reportAvail and report in reportsForUser:
							reportsToReturn.append(report)
					elif reportOwner != "" and reportAvail != "":
						for r in reportsForUser:
							if r.owner == reportOwner and r.isprivate == reportAvail:
								reportsToReturn.append(r)

				elif "OR" in searchterms:
					searchterms = searchterms.split('OR')
					for term in searchterms:
						termPair = term.split(':')
						if termPair[0].strip() == 'reportname':
							reportName = termPair[1].strip()
						elif termPair[0].strip() == 'owner':
							reportOwner = termPair[1].strip()
						elif termPair[0].strip() == 'availability':
							reportAvail = termPair[1].strip()
						else:
							# there is an error in the listing of terms 
							nameError = True

					if reportName != "":
						for r in reportsForUser:
							if r.reportname == reportName:
								reportsToReturn.append(r)
					if reportOwner != "":
						for r in reportsForUser:
							if r.owner == reportOwner and r not in reportsToReturn:
								reportsToReturn.append(r)
					if reportAvail != "":
						for r in reportsForUser:
							if r.isprivate == reportAvail and r not in reportsToReturn:
								reportsToReturn.append(r)
				else: 
					termPair = searchterms.split(':')
					if termPair[0].strip() == 'reportname':
						reportName = termPair[1].strip()
					elif termPair[0].strip() == 'owner':
						reportOwner = termPair[1].strip()
					elif termPair[0].strip() == 'availability':
						reportAvail = termPair[1].strip()
					else:
						# there is an error in the listing of terms 
						nameError = True

					# find the appropriate report(s)
					if reportName != "":
						report = Report.objects.get(reportname=reportName)
						if report in reportsForUser:
							reportsToReturn.append(report)
					elif reportOwner != "":
						for r in reportsForUser:
							if r.owner == reportOwner:
								reportsToReturn.append(r)
					elif reportAvail != "":
						for r in reportsForUser:
							if r.isprivate == reportAvail:
								reportsToReturn.append(r)
				if nameError == True:
					searchForm.add_error('searchTerms', 'The search terms were not entered in the correct format. Please enter search terms as specified by the example search input.')
					return render(request, 'myapplication/manageReports.html', {'searchForm':searchForm})
				else: 
					return render(request, 'myapplication/viewSearchedReports.html', {'reports': reportsToReturn, 'reportfiles': ReportFiles.objects.all()})
		else: 
			pass 
		HttpResponseRedirect('manage_reports')
	else:
		return HttpResponseRedirect('home_page')

def reset_pass(request):
	if 'loggedin' in request.session: 
		if request.method == "POST":
			passForm = ResetPassForm(request.POST)
			if passForm.is_valid():
				oldpwd = request.POST.get('oldpwd')
				newpwd = request.POST.get('newpwd')
				newpwd2 = request.POST.get('newpwd2')
				username = request.session.get('username')
				# authenticate user
				user = authenticate(username=username, password=oldpwd)
				if user is not None:
					if newpwd == newpwd2:
						# reset the password
						u = User.objects.get(username=username)
						u.set_password(newpwd)
						u.save()
					else: 
						# the two passwords did not match
						passForm.add_error('newpwd', 'Your passwords do not match. Please make sure your passwords match.')
						return render(request, 'myapplication/memberHomePage.html', {'show':'show', 'passForm':passForm, 'keyPairForm':RequestNewKeyPairForm()})
				else: 
					# user is not an existing user (for some reason)
					passForm.add_error('oldpwd', 'You have entered an invalid existing password.')
					return render(request, 'myapplication/memberHomePage.html', {'show':'show', 'passForm':passForm, 'keyPairForm':RequestNewKeyPairForm()})
			return render(request, 'myapplication/memberHomePage.html', {'resetComplete':'resetComplete', 'passForm':ResetPassForm(), 'keyPairForm': RequestNewKeyPairForm()})
		else: 
			passForm = ResetPassForm()
		keyPairForm = RequestNewKeyPairForm()
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':keyPairForm, 'passForm':passForm})
	else:
		return HttpResponseRedirect('home_page')

def request_private_key(request):
	if 'loggedin' in request.session: 
		if request.method == "POST":
			keyPairForm = RequestNewKeyPairForm(request.POST)
			if keyPairForm.is_valid():
				uname = request.POST.get('username')
				pwd = request.POST.get('pwd')
				username = request.session.get('username')
				user = authenticate(username=username, password=pwd)
				if user is not None:
					user = UserInformation.objects.get(username=username)
					# generate a new key pair
					random_generator = Random.new().read
					key = RSA.generate(1024, random_generator)
					publicKey = key.publickey() #.exportKey()
					# save the new public key into the database
					user.publickey = publicKey
					user.save()
					# send user to page with modal pop-up displaying his/her private key, prompt them to write it down
					return render(request, 'myapplication/showPrivateKey.html', {'pkey':key.exportKey()})
				else: 
					# user does not exist
					keyPairForm.add_error('username', 'Your username or password is incorrect. Please enter valid credentials in order to obtain a new key pair.')
					return render(request, 'myapplication/memberHomePage.html', {'showKeyPairError':'showKeyPairError', 'keyPairForm':keyPairForm, 'passForm':ResetPassForm()})
		else: 
			keyPairForm = RequestNewKeyPairForm()
		passForm = ResetPassForm()
		return render(request, 'myapplication/memberHomePage.html', {'keyPairForm':keyPairForm, 'passForm':passForm})
	else:
		return HttpResponseRedirect('home_page')

def messages(request):
	inbox_list = Messages.objects.order_by('-created')
	personal_inbox = []
	for m in inbox_list:
		if m.recipient_username == request.session.get('username'):
			personal_inbox.append(m)
	context = {'personal_inbox': personal_inbox}
	return render(request, 'myapplication/messages.html', context)

def new_message(request):
	if request.method == "POST":
		form = MessageForm(request.POST)
		if form.is_valid():
			sender = request.session.get('username')
			subject = request.POST['subject']
			body = request.POST['body']
			receiver = request.POST['recipient_username']
			try: 
				rec = UserInformation.objects.get(username=receiver)
			except ObjectDoesNotExist:
				return render(request, 'myapplication/new_message.html', {'receiverError':'That user does not exist. Please type in a valid recipient username'})
			if 'encrypted' in request.POST.keys():
				encrypted=request.POST['encrypted']
				public_key = UserInformation.objects.get(username=receiver).publickey
				public_key = RSA.importKey(public_key)
				enc_data = public_key.encrypt(str.encode(body), 32) #str.encode(body)
				# cast encrypted data as a string
				enc_data = str(enc_data[0])
				msg_obj = Messages(sender=sender, recipient_username=receiver, subject=subject, body=enc_data, encrypted=""+encrypted)
				msg_obj.save()
			else:
				msg_obj = Messages(sender=sender, recipient_username=receiver, subject=subject, body=body, encrypted=False)
				msg_obj.save()

			return HttpResponseRedirect('messages')

	else:
		form = MessageForm()
	return render(request, 'myapplication/new_message.html', {'form': form})

def delete_message(request):
	ID = request.POST['deleteMessageID']
	Messages.objects.get(id = ID).delete()
	return HttpResponseRedirect('messages')

def display_message(request):
	ID = request.POST['id']
	return render(request, 'myapplication/display_message.html', {'message':Messages.objects.get(id = ID)})

def decrypt_message(request):
	ID = request.POST['decryptMessageID']
	# get and import the private key
	privateKey = request.POST['privateKey']
	# ensure formatting 
	privateKey = privateKey.strip('-----BEGIN RSA PRIVATE KEY-----')
	privateKey = privateKey.strip('-----END RSA PRIVATE KEY-----')
	privateKey = privateKey.strip()
	privateKey = privateKey.replace(' ', '\r\n')
	privateKey = '-----BEGIN RSA PRIVATE KEY-----\r\n' + privateKey + '\r\n-----END RSA PRIVATE KEY-----'
	privateKey = ''.join(privateKey)
	try: 
		privateKey = RSA.importKey(privateKey)
	except:
		inbox_list = Messages.objects.order_by('-created')
		personal_inbox = []
		for m in inbox_list:
			if m.recipient_username == request.session.get('username'):
				personal_inbox.append(m)
		context = {'personal_inbox': personal_inbox, 'error': 'Please enter a valid private key. Your key may have extraneous leading or ending spaces.'}
		return render(request, 'myapplication/messages.html', context)
	# # decode
	body = Messages.objects.get(id=ID).body #.decode('utf-8')
	decrypted = privateKey.decrypt(ast.literal_eval(str(body)))
	return render(request, 'myapplication/display_message.html', {'encmsg':True, 'message': Messages.objects.get(id=ID), 'messagebody':decrypted})

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()



# for authentication


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import django.core.servers.basehttp
from django.db import models
from django.db.models.query import QuerySet
from django.template import RequestContext
from myapplication.models import UserInformation, Report





def promptLogin():
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')
	login(user, pwd)

def login(username, pwd):
	user = authenticate(username=username, password=pwd)
    #print()
	if user is not None:
		if user.is_active:

			 options(username)
	else:
		print("That username or password is not valid.")
		print("Type 't' to try again.")
		retry = input()
		if (retry == 't'):
			promptLogin()
		else: 
			print("Communication terminated.")

def options(username):
	#name = QuerySet.filter(username = username)
    from django.db import connection

    #tables = connection.introspection.table_names()
    #seen_models = connection.introspection.installed_models(tables)
    #print(tables)
    #print(seen_models)
    userInf = UserInformation.objects.get(username = username)
    #print(userInf.firstname)
    #request.session['firstname'] = userInf.firstname
    print("Welcome " + userInf.firstname)
    print("Please choose an option:")
    print("a. Reports")
    choice = input("Choice: ")
    if(choice == "a"):
        seeReports(username)
    return 0
def seeReports(username):
    print("Reports")
    report_list = Report.objects.filter(owner = username)
    for file in report_list:
        print("Report Name: " +  file.reportname)
        print("Summary: " +  file.summary)
        print("Description: " +  file.description)
        #print("Report last updated: " + str(file.timestamp))
        print()
    #print(report_list)
if __name__=="__main__":
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')

	login(user, pwd)
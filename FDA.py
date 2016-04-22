import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from myapplication.models import Report, ReportFiles, ReportGroups, Groups

def promptLogin():
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')
	login(user, pwd)

def login(username, pwd): 
	user = authenticate(username=username, password=pwd)
	if user is not None:
		if user.is_active:
			print("User is active.")
			# call method to offer options 
			menu(username)
	else: 
		print("That username or password is not valid.")
		print("Type 't' to try again.")
		retry = input()
		if (retry == 't'):
			promptLogin()
		else: 
			print("Communication terminated.")

def menu(user):
	print("Please select a menu option by typing the corresponding letter: ")
	print("1. View My Reports")
	print("2. View Shared Reports")
	print("Type 'quit' to quit")

	mainMenuChoice = input()
	if mainMenuChoice == '1':
		# view my reports
		reports = Report.objects.filter(owner=user)
		print("Report Name\tSummary\tDescription\tPublic/Private\tTime of Creation")
		count = 1
		repList = []
		for r in reports:
			print(str(count)+": "+r.reportname+"\t"+r.summary+"\t"+r.description+"\t"+r.isprivate+"\t"+str(r.timestamp))
			tup = (str(count), r.reportname)
			repList.append(tup)
			count+=1
		print("To view a report's files, type the report's corresponding number. To return to the main menu, type 'main'. To quit, type 'quit'")
		subMenuChoice = input()
		while(subMenuChoice != 'quit'):
			if subMenuChoice == 'main':
				menu(user)
			else:
				found = show_files(subMenuChoice, repList)
				if found == False:
					print("The report you selected does not exist. View the files from another report by typing its corresponding number, type 'main' to see main menu options, or type 'quit' to quit.")
				else:
					print("View the files from another report by typing its corresponding number, type 'main' to see main menu options, or type 'quit' to quit.")
			subMenuChoice=input()
	elif mainMenuChoice == '2':
		# view shared reports
		groups = Groups.objects.filter(username=user)
		for group in groups:
			print(group.groupname+" reports: ")
			print("Report Name\tSummary\tDescription\tPublic/Private\tTime of Creation")
			count = 1
			repList = []
			for r in ReportGroups.objects.filter(groupname=group.groupname):
				r = Report.objects.get(reportname=r.reportname)
				print(str(count)+": "+r.reportname+"\t"+r.summary+"\t"+r.description+"\t"+r.isprivate+"\t"+str(r.timestamp))
				tup = (str(count), r.reportname)
				repList.append(tup)
				count+=1
		print("To view a report's files, type the report's corresponding number. To return to the main menu, type 'main'. To quit, type 'quit'")
		subMenuChoice = input()
		while (subMenuChoice != 'quit'):
			if subMenuChoice == 'main':
				menu(user)
			else:
				found = show_files(subMenuChoice, repList)
				if found == False:
					print("The report you selected does not exist. View the files from another report by typing its corresponding number, type 'main' to see main menu options, or type 'quit' to quit.")
				else:
					print("View the files from another report by typing its corresponding number, type 'main' to see main menu options, or type 'quit' to quit.")
			subMenuChoice = input()
	print("Goodbye.")
	return

def show_files(subMenuChoice, repList):
	found = False
	for tup in repList:
		if tup[0] == subMenuChoice:
			# display the files from this report
			for f in ReportFiles.objects.filter(reportname=tup[1]):
				print(f.uploadfile.name)
			return True
	return False

if __name__=="__main__":
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')

	login(user, pwd)





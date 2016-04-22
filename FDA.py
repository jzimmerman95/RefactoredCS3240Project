import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from myapplication.models import Report, ReportFiles, ReportGroups, Groups
# imports for encrytion
from Crypto.PublicKey import RSA

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
		print ("Options: ")
		print("View a report's files by typing the report's corresponding number.")
		print("Type 'main' to return to the main menu")
		print("Type 'quit' to quit")
		subMenuChoice = input()
		fileList = []
		while(subMenuChoice != 'quit'):
			if subMenuChoice == 'main':
				menu(user)
			elif 'download' in subMenuChoice:
				# downloading a file
				download(fileList, subMenuChoice)
			else:
				found = show_files(subMenuChoice, repList, fileList)
				if found == False:
					print("The report you selected does not exist.")
					print ("Options: ")
					print("View a report's files by typing the report's corresponding number.")
					print("Type 'main' to return to the main menu")
					print("Type 'quit' to quit")
				else:
					print ("Options: ")
					print("View a report's files by typing the report's corresponding number.")
					print("Download a file by typing 'download' followed by the file's corresponding number")
					print("Type 'main' to return to the main menu")
					print("Type 'quit' to quit")
			subMenuChoice=input()
		if subMenuChoice == 'quit':
			print("Goodbye.")
			return
	elif mainMenuChoice == '2':
		# view shared reports
		groups = Groups.objects.filter(username=user)
		print("Report Name\tSummary\tDescription\tPublic/Private\tTime of Creation\tGroup")
		for group in groups:
			count = 1
			repList = []
			for r in ReportGroups.objects.filter(groupname=group.groupname):
				r = Report.objects.get(reportname=r.reportname)
				print(str(count)+": "+r.reportname+"\t"+r.summary+"\t"+r.description+"\t"+r.isprivate+"\t"+str(r.timestamp)+"\t"+group.groupname)
				tup = (str(count), r.reportname)
				repList.append(tup)
				count+=1
		print("To view a report's files, type the report's corresponding number. To return to the main menu, type 'main'. To quit, type 'quit'")
		subMenuChoice = input()
		fileList = []
		while (subMenuChoice != 'quit'):
			if subMenuChoice == 'main':
				menu(user)
			elif 'download' in subMenuChoice:
				# downloading a file
				download(fileList, subMenuChoice)
			else:
				found = show_files(subMenuChoice, repList, fileList)
				if found == False:
					print("The report you selected does not exist.")
					print ("Options: ")
					print("View a report's files by typing the report's corresponding number.")
					print("Type 'main' to return to the main menu")
					print("Type 'quit' to quit")
				else:
					print ("Options: ")
					print("View a report's files by typing the report's corresponding number.")
					print("Download a file by typing 'download #', where # is the file's corresponding number")
					print("Type 'main' to return to the main menu")
					print("Type 'quit' to quit")				
			subMenuChoice = input()
		if subMenuChoice == 'quit':
			print("Goodbye.")
			return
	print("Goodbye.")
	return

def show_files(subMenuChoice, repList, fileList):
	found = False
	del fileList[:]
	for tup in repList:
		if tup[0] == subMenuChoice:
			# display the files from this report
			count = 1
			for f in ReportFiles.objects.filter(reportname=tup[1]):
				tup = (str(count), f)
				fileList.append(tup)
				if f.isencrypted == 1:
					print(str(count)+": "+f.uploadfile.name+" \t(encrypted)")
				else:
					print(str(count)+": "+f.uploadfile.name)
				count+=1
			return True
	return False

def download(fileList, subMenuChoice):
	num = subMenuChoice[9:]
	for f in fileList:
		if f[0] == num:
			if f[1].isencrypted == 1:
				download_encrypted_file(f[1].uploadfile.name)
			else:
				download_unencrypted_file(f[1].uploadfile.name)

def download_unencrypted_file(filename):
	print("Download "+filename)
	
def download_encrypted_file(filename):
	print("Please enter the decryption key: ")
	key = input()
	#key.decrypt("something")
	print("Download "+filename)

if __name__=="__main__":
	user = input('Please enter username: ')
	pwd = input('Please enter password: ')

	login(user, pwd)





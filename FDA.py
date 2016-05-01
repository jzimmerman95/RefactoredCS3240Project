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
from myapplication.models import UserInformation, Report, ReportFiles
from myapplication.views import getFile
from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType

import requests

import tkinter as tk

TITLE_FONT = ("Helvetica", 18, "bold")
username = ""

class SampleApp(tk.Tk):

    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}



        for F in (WelcomeFrame, LoginFrame, OptionFrame, ErrorFrame):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            #F.setUser(use)
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to the FDA", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Login",
                           command=lambda: controller.show_frame("LoginFrame"))
        button.pack()

class LoginFrame(tk.Frame):




    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user = ""
        self.pwd = ""
        label_1 = tk.Label(self, text="Username")
        label_2 = tk.Label(self, text="Password")

        entry_1 = tk.Entry(self)
        entry_2 = tk.Entry(self, show="*")

        label_1.grid(row=0, sticky="E")
        label_2.grid(row=1, sticky="E")
        entry_1.grid(row=0, column=1)
        entry_2.grid(row=1, column=1)

        #checkbox = tk.Checkbutton(self, text="Keep me logged in")
        #checkbox.grid(columnspan=2)

        logbtn = tk.Button(self, text="Login", command= lambda: self._login_btn_clickked(entry_1, entry_2))
        #self._login_btn_clickked
        logbtn.grid(columnspan=2)
        #logbtn.pack()

    def setUserPass(self, username):
        self.user = username
        #self.pwd = pwd

    def getUser(self):
        return self.user

    #def getPwd(self):
    #    return self.pwd

    def _login_btn_clickked(self, entry_1,entry_2):
        # print("Clicked")
        username = entry_1.get()

        pwd = entry_2.get()
        #print("something")
        #print(username)
        #print(pwd)
        user = authenticate(username=username, password=pwd)
        if user is not None:

            if user.is_active:
                "authenticated"
                print("authenticated")
                self.setUserPass(username)
                #newUser(username)
                page_two = self.controller.get_page("OptionFrame")
                page_two.setUser(username)
                page_two.isSignedIn(username)
                return (self.controller.show_frame("OptionFrame"))
        else:
            #print("That username or password is not valid.")
            #print("Type 't' to try again.")
            #retry = input()
            #if (retry == 't'):
            return (self.controller.show_frame("ErrorFrame"))
            #else:
            #    print("Communication terminated.")





class OptionFrame(tk.Frame):
    def __init__(self, parent, controller):


        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user = ""
        #username = LoginFrame.getUser(self)
        #print("Username: " + username)
        from django.db import connection

    #tables = connection.introspection.table_names()
    #seen_models = connection.introspection.installed_models(tables)
    #print(tables)
    #print(seen_models)

        page_one = self.controller.get_page("LoginFrame")


        value = page_one.getUser()
        self.setUser(value)


    def getFirstName(self, username):
        from django.db import connection
        username = self.user
        print(username)
        if(username != ""):
            userInf = UserInformation.objects.get(username=username)
            return userInf.firstname
        else:
            print("bleh")

    def setUser(self, username):
        self.user = username

    def isSignedIn(self, username):
        if(username != ""):
            #print("Value: " + value)

            #userInf = UserInformation.objects.get(username=username)
            firstname = self.getFirstName(username)
            #print(userInf.firstname)
            #request.session['firstname'] = userInf.firstname
            print("Welcome " + firstname)
            #print("Please choose an option:")
            #print("a. Reports")
            #print("b. Shared Reports")
            #choice = input("Choice: ")
            #if (choice == "a"):
            #    seeReports(username)




            label = tk.Label(self, text=("Welcome " + firstname), font=TITLE_FONT)
            label.pack(side="top", fill="x", pady=10)
            button = tk.Button(self, text="Logout",
                               command=lambda: self.logout())
            button.pack()

    def logout(self):
        for child in self.winfo_children():
            child.destroy()

        return self.controller.show_frame("LoginFrame")


class ErrorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user = ""

        label = tk.Label(self, text="Login Failed", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("LoginFrame"))
        button.pack()

    def setUser(self, username):
        self.user = username

def promptLogin():
    user = input('Please enter username: ')
    pwd = input('Please enter password: ')
    login(user, pwd)


def login(username, pwd):
    #user = authenticate(username=username, password=pwd)
    requests.get()
    # print()
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
    # name = QuerySet.filter(username = username)
    from django.db import connection

    #tables = connection.introspection.table_names()
    #seen_models = connection.introspection.installed_models(tables)
    #print(tables)
    #print(seen_models)
    userInf = UserInformation.objects.get(username=username)
    #print(userInf.firstname)
    #request.session['firstname'] = userInf.firstname
    print("Welcome " + userInf.firstname)
    print("Please choose an option:")
    print("a. Reports")
    print("b. Shared Reports")
    choice = input("Choice: ")
    if (choice == "a"):
        seeReports(username)
    return 0


def seeReports(username):
    print("Reports")
    report_list = Report.objects.filter(owner=username)
    for file in report_list:
        print("Report Name: " + file.reportname)
        print("Summary: " + file.summary)
        print("Description: " + file.description)
        print("ReportFiles: ")
        file_list = ReportFiles.objects.filter(reportname = file.reportname)
        #print(file_list)
        for i in file_list:
            if(i.isencrypted == True):
                print(str(i.uploadfile) + " (encrypted)")
            else:
                print(i.uploadfile)
        # print("Report last updated: " + str(file.timestamp))
        print()
        #print(report_list)
    #ReportFile = input("Enter name of file you'd like to download or press enter for to not download: ")

    #full_list = ReportFiles.objects.get()
    #if ReportFile in full_list:
    #test_list = ReportFiles.objects.all()
    #for x in test_list:
    #if ReportFile in test_list:
        #print(x.uploadfile)
        #if x.uploadfile == ReportFile:
            #downloadFile(test_list[1].uploadfile)
    #downloadFile(x.uploadfile, ReportFile)
    downloadFile()

def downloadFile():

    #response = getFile(RequestContext)
    #r = render(RequestContext, response, {})
    outfile = 'outfile.txt'
    string = input("Enter filename: ")
    url = ('http://127.0.0.1:8000/get_file/?page=' + string)
    print(url)
    r = requests.get(url)

    print(r)
    #with open(data, "wb") as o:
    #    o.write(data)
    #with open(file_path, 'rb') as f:
        #with open(os.path.join(os.path.expanduser('~'),'Documents', string[2:]), "wb") as o:

            #if (ReportFile.isencrypted == True):
            #    for line in f:
                        #e_text = obj2.decrypt(line)
                        #print(e_text)
                        #o.write(e_text)
                    #o.close()
                    #f.close()
            #else:
                #for line in f:

                    #print(e_text)
                #    o.write(line)
                #o.close()
                #f.close()

    return 0
    #return 0



if __name__ == "__main__":
    # app = tkinter.Tk()
    #app.title('File Download Application')

    #usertitle = tkinter.Label(app, text="Username: ")
    #usertitle.grid(row = 0, column = 0, sticky = "E")
    #passtitle = tkinter.Label(app, text="Password: ")
    #passtitle.grid(row = 1, column = 0, sticky = "E")

    #user = tkinter.Entry(app)
    #user.grid(row = 0, column = 1)
    #pwd = tkinter.Entry(app, show='*')
    ##pwd.grid(row = 1, column = 1)


    #usertitle.pack()
    #user.pack()
    #passtitle.pack()
    #pwd.pack()

    #app = SampleApp()
    #app.title("File Download Application")
    #app.mainloop()

    user = input('Please enter username: ')
    pwd = input('Please enter password: ')

    login(user, pwd)
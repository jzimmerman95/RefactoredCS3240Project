from django import forms
from django.forms import ModelForm
from .models import UserInformation, Folders, Groups, Messages, GroupUsers
from django.contrib.auth.models import User
from django.forms.widgets import Select

class UserSignUpForm(ModelForm):
	class Meta:
		model = UserInformation
		fields=('username',)

CHOICES = (  
	('yes', 'yes'),
	('no', 'no'),
)

CHOICES2 = (
	('public', 'public'),
	('private', 'private'),
)

class ReportForm(forms.Form):
	reportname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'reportnameid'}))
	summary = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id':'summaryid'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'id':'descriptionid'}))
	isprivate = forms.ChoiceField(choices=CHOICES2, required=True, widget=forms.Select(attrs={'id':'isprivateid'}))
	uploadfile = forms.FileField(widget=forms.FileInput(attrs={'id': 'uploadfileid'}))
	isencrypted = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'isencryptedid'}))
	extra_field_count = forms.CharField(widget=forms.HiddenInput(attrs={'id':'extra_field_countid'}))
	groups = forms.MultipleChoiceField(widget=forms.SelectMultiple())

	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		self.fields['uploadfile'].required = False
		self.fields['extra_field_count'].required = False
		self.fields['groups'].required = False
		self.fields['isencrypted'].required = False
		self.fields['groups'].required = False
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

	def setChoices(self, request):
		CHOICES3 = []
		for group in GroupUsers.objects.filter(username=request.session['username']):
			CHOICES3.append((group.groupname, group.groupname))
		self.fields['groups'].choices = CHOICES3

class EditFileForm(forms.Form):
	filestoremove = forms.CharField(widget=forms.TextInput(attrs={'id':'filestoremoveid'}))
	uploadfile = forms.FileField(widget=forms.FileInput(attrs={'id': 'uploadfileid'}))
	isencrypted = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'isencryptedid'}))
	extra_field_count = forms.CharField(widget=forms.HiddenInput())
	
	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(EditFileForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		self.fields['uploadfile'].required = False
		self.fields['filestoremove'].required = False
		self.fields['extra_field_count'].required = False
		self.fields['isencrypted'].required = False
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

class EditGroupForm(forms.Form):
	groupstoadd = forms.CharField(widget=forms.TextInput(attrs={'id':'groupstoaddid'}))
	groupstoremove = forms.CharField(widget=forms.TextInput(attrs={'id':'groupstoremoveid'}))

class CreateFolderForm(ModelForm):
	class Meta:
		model = Folders
		fields = ('foldername', 'reports', )

	def __init__(self, *args, **kwargs):
		super(CreateFolderForm, self).__init__(*args, **kwargs)
		self.fields['foldername'].widget.attrs.update({'id': 'foldernameid'})
		self.fields['reports'].widget.attrs.update({'id': 'reportsid'})
		self.fields['reports'].required = False

class RenameFolderForm(forms.Form):
	newfoldername=forms.CharField(max_length=100)

class SearchReportsForm(forms.Form):
	searchTerms=forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'id':'searchtermsid', 'placeholder':'reportname:myreport OR owner:myname OR availability:private'}))

class CreateGroupForm(forms.Form):
	groupname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'groupnameid'}))
	users = forms.MultipleChoiceField(widget=forms.SelectMultiple())

	def __init__(self, *args, **kwargs):
		super(CreateGroupForm, self).__init__(*args, **kwargs)
		self.fields['groupname'].initial = ''
		self.fields['users'].required = False

	def setChoices(self, request):
		USER_CHOICES = []
		for user in UserInformation.objects.all():
			USER_CHOICES.append((user.username, user.username))
		self.fields['users'].choices = USER_CHOICES
	
class ResetPassForm(forms.Form):
	oldpwd = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
	newpwd = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
	newpwd2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))

class RequestNewKeyPairForm(forms.Form):
	username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
	pwd = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))


class MessageForm(forms.Form):
	class Meta:
		model = Messages
		fields = ('recipient_username', 'subject', 'body', 'encrypted')

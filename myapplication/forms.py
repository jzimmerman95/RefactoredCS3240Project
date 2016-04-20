from django import forms
from django.forms import ModelForm
from .models import UserInformation, Folders
from django.contrib.auth.models import User

class UserSignUpForm(ModelForm):
	class Meta:
		model = UserInformation
		fields=('username', )

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
	#containsencrypted = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.Select(attrs={'id':'containsencryptedid'}))
	isprivate = forms.ChoiceField(choices=CHOICES2, required=True, widget=forms.Select(attrs={'id':'isprivateid'}))
	groups = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id': 'groupsid'}))
	uploadfile = forms.FileField(widget=forms.FileInput(attrs={'id': 'uploadfileid'}))
	isencrypted = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'isencryptedid'}))
	#isencrypted = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	#isencrypted = forms.CharField()
	extra_field_count = forms.CharField(widget=forms.HiddenInput(attrs={'id':'extra_field_countid'}))

	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		self.fields['uploadfile'].required = False
		self.fields['extra_field_count'].required = False
		self.fields['groups'].required = False
		self.fields['isencrypted'].required = False
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

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

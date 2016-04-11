from django import forms
from django.forms import ModelForm
from .models import UserInformation
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
	containsencrypted = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.Select(attrs={'id':'containsencryptedid'}))
	isprivate = forms.ChoiceField(choices=CHOICES2, required=True, widget=forms.Select(attrs={'id':'isprivateid'}))
	groups = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id': 'groupsid'}))
	uploadfile = forms.FileField(widget=forms.FileInput(attrs={'id': 'uploadfileid'}))
	extra_field_count = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		self.fields['uploadfile'].required = False
		self.fields['extra_field_count'].required = False
		self.fields['groups'].required = False
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

class EditFileForm(forms.Form):
	filestoremove = forms.CharField(widget=forms.TextInput(attrs={'id':'filestoremoveid'}))
	uploadfile = forms.FileField(widget=forms.FileInput(attrs={'id': 'uploadfileid'}))
	extra_field_count = forms.CharField(widget=forms.HiddenInput())
	
	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(EditFileForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		self.fields['uploadfile'].required = False
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

# class RenameReportForm(forms.Form):
# 	oldreportname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
# 	newreportname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

# class RenameReportForm(forms.Form):
# 	newreportname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'id':'newreportname'}))






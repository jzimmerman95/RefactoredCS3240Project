from django import forms
from django.forms import ModelForm
from .models import UserInformation
from django.contrib.auth.models import User

class UserSignUpForm(ModelForm):
	class Meta:
		model = UserInformation
		fields=('username', )

class ReportForm(forms.Form):
	reportname = forms.CharField(max_length=100)
	summary = forms.CharField(max_length=200)
	description = forms.CharField(widget=forms.Textarea)
	containsencrypted = forms.BooleanField()
	uploadfile = forms.FileField()
	extra_field_count = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields
		for index in range(int(extra_fields)):
			# generate extra fields in the number specified via extra_fields
			self.fields['extra_field_{index}'.format(index=index)] = \
				forms.CharField()

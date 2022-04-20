from django import forms

from productinfo.models import Customer


class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'

	def clean_first_name(self):
		return self.cleaned_data['first_name'].strip()

	def clean_last_name(self):
		return self.cleaned_data['last_name'].strip()

	def clean_disambiguator(self):
		if len(self.cleaned_data['disambiguator']) == 0:
			result = self.cleaned_data['disambiguator']
		else:
			result = self.cleaned_data['disambiguator'].strip()
		return result

	def clean_username(self):
		return self.cleaned_data['username'].strip()

	def clean_password(self):
		return self.cleaned_data['password'].strip()


from django import forms
from mongoengine import *
from datetime import *

#forms for the collections

#created on handled in field
class CategoryForm(forms.Form):
	cname = forms.CharField()
	isActive = forms.BooleanField(required=False)

class StatusForm(forms.Form):
	name = forms.CharField()
	isActive = forms.BooleanField(required=False)

class UserForm(forms.Form):
	username = forms.CharField()
	fname = forms.CharField()
	lname = forms.CharField()
	isActive = forms.BooleanField(required=False)

class todoForm(forms.Form):
	def is_valid(self):
		if super(todoForm, self).is_valid():
			if user.objects(username=self.cleaned_data['assigned_to']) and status.objects(name=self.cleaned_data['status']) and category.objects(catname=self.cleaned_data['category']):
				return True
			else:
				if not user.objects(username=self.cleaned_data['assigned_to']):
					print('user problem')
				if not status.objects(name=self.cleaned_data['status']):
					print(self.cleaned_data['status'])
					print('status problem')
				if not category.objects(catname=self.cleaned_data['category']):
					print('category problem')
				print()
				print('error in intitial form validation')
				print()
				return False
		else:
			print()
			print('initial problem')
			print()
			return False

	description = forms.CharField()
	details = forms.CharField()
	#created on
	target_date = forms.DateField(input_formats = ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"])
	status = forms.CharField(widget=forms.TextInput(attrs={'list' : 'status-options'} ) )
	category = forms.CharField(widget = forms.TextInput(attrs = {'list' : 'category-options'} ) )
	assigned_to = forms.CharField(widget = forms.TextInput(attrs = {'list' : 'user-options'} ) )

#field classes for mongoengine

class category(Document):
	catname = StringField(unique=True)
	isActive = BooleanField()
	createdOn = DateField( default = date.today() )

class status(Document):
	name = StringField(unique=True)
	isActive = BooleanField()
	createdOn = DateField( default = date.today() )

class user(Document):
	username = StringField(unique=True)
	fname = StringField(required=True)
	lname = StringField(required=True)
	isActive = BooleanField(required=True)
	createdOn = DateField(default=date.today())

class todo(Document):
	description = StringField()
	details = StringField()
	createdOn = DateField(default=date.today())
	target_date = DateField()
	status = ReferenceField(status)
	category = ReferenceField(category)
	assigned_to = ReferenceField(user)
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django import forms

from .models import Task, User

class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
	    super(SignupForm, self).__init__(*args, **kwargs)

	    for fieldname in ['username', 'email', 'password1', 'password2']:
	    	self.fields[fieldname].help_text = None

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['text']
		widgets = {
		            'text' : forms.TextInput(attrs={
		                'id' : 'task_text',
		                'required' : True,
		                'placeholder' : 'Write Something..',
		            })
		        }
	def __init__(self, *args, **kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['text'].label = ""
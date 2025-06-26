from django import forms
from .models import Problem
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, Ticket, Events, ToDo

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('birth_date', 'photo', 'bio', 'location')

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'note', 'compleks', 'problem', 'company', 'user', 'partnyor', 'start', 'end', 'color', 'status', 'file']

class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name', 'start', 'end', 'color', 'status']

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['name', 'note', 'compleks', 'user', 'start', 'end', 'color', 'status', 'file']
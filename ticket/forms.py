from django import forms
from django.forms import ModelForm
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'

class UpdateProblemForm(ModelForm):

    class Meta:
        model = Problem
        fields = '__all__'
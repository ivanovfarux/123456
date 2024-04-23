from django import forms
from .models import *


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = "__all__"
from django import forms
from django.forms import ModelForm
from .models import Problem,  User


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'

class UpdateProblemForm(ModelForm):

    class Meta:
        model = Problem
        fields = '__all__'

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['title', 'author', 'publication_date']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields =('name', 'photo', 'email', 'password', 'mobile_number', 'date_of_birth')
#         # fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#
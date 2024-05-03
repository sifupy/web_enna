# In forms.py
from django import forms

class LoginForm(forms.Form):
    matricul = forms.CharField(label='Matricul', max_length=20, required=True)  # Unique field for login
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)  # Password field

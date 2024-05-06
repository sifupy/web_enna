from django import forms

class LoginForm(forms.Form):
    matricul = forms.CharField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Matricule',
        'style': 
        'background-color:#F0EDFFCC;border-radius:16px;width:300px'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
      'placeholder': 'mot de passe',
        'style': 
        'background-color:#F0EDFFCC;border-radius:16px;width:300px'  
    }))

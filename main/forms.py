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
class relve_Form(forms.Form):
    matricule1 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Matricule'
    }),label="Matricule")
    date_debut = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Date Début'
    }), label="Date ")
  

class ats_Form(forms.Form):
    matricule2 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Matricule'
    }),label="Matricule")
    date= forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Date Début'
    }), label="Date ")
    nbrmois = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Nombre mois'
    }))

class attestation_Form(forms.Form):
    matricule3 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Matricule'
    }),label="Matricule")
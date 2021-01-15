from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CrearUsuario(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(label='Usuario')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    

    class Meta:
	    model = User
	    fields = ['username', 'email', 'password1', 'password2']
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

#Register Form used in the register process, it adds the fields specified in the "Profile" model (Except for email status which is automatic)
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254, help_text='Mandatory, must be fulfilled')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, max_length=254)
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=100)
   
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

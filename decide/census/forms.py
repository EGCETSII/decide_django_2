from django import forms
from voting.models import Voting
from django.forms import ModelMultipleChoiceField
from django.db.models import Q
class CensusAddLdapForm(forms.Form):
    #Atributos
    voting = forms.ModelChoiceField(label='Votación a la que desea añadir censo', empty_label="-", queryset=Voting.objects.all().filter(start_date__isnull=True, end_date__isnull=True), required=True,)
    urlLdap = forms.CharField(label='Url del servidor LDAP', widget=forms.TextInput(attrs={'placeholder': 'ldap://urlDeServidorLdap:Puerto'}), required=True)
    treeSufix = forms.CharField(label='Rama del arbol del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=TuDominio,dc=com'}), required=True)
    pwd = forms.CharField(label='Contraseña del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'Contraseña'}), required=True)
    group = forms.CharField(label='Grupo que quiere incluir en la votacion', widget=forms.TextInput(attrs={'placeholder': 'Grupo 1'}), required=True)
    
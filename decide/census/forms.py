from django import forms
from django.contrib.auth.models import Group


class importForm(forms.Form):
    name = forms.CharField(max_length=80, min_length=1, label='Nombre del grupo', required=True)
    is_public = forms.BooleanField(label='Público', required=False)
    file = forms.FileField(label='Archivo txt o xlsx', required=True)


class exportForm(forms.Form):
    group = forms.ModelChoiceField(label='Selecciona grupo a exportar', queryset=Group.objects.all())
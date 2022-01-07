from django import forms
from .views import ParentGroup
from django.contrib.auth.models import Group


class importForm(forms.Form):
    name = forms.CharField(max_length=80, min_length=1, label='Nombre del grupo', required=True)
    is_public = forms.BooleanField(label='Público', required=False)
    file = forms.FileField(label='Archivo txt o xlsx', required=True)


class exportForm(forms.Form):
    group = forms.ModelChoiceField(label='Selecciona grupo a exportar', queryset=Group.objects.all())


class GroupOperationsForm(forms.Form):
    group_name = forms.CharField(
        max_length=80, label='Nombre del grupo generado')

    base_group = forms.ModelChoiceField(queryset=ParentGroup.objects.all(
    ), label='Grupo base sobre el que se aplica la operación')

    groups = forms.ModelMultipleChoiceField(queryset=ParentGroup.objects.all(),
                                            label='Grupos')

    is_public = forms.BooleanField(
        required=False, label='¿Quiere que el grupo sea público?')

    operation = forms.ChoiceField(label='Operación', choices=(('union', 'Unión'), (
        'intersection', 'Intersección'), ('difference', 'Diferencia')))

    def clean(self):
        cleaned_data = super().clean()

        groups = cleaned_data.get('groups')
        base_group = cleaned_data.get('base_group')

        if base_group in groups:
            raise forms.ValidationError(
                'El grupo base sobre el que quieres aplica la operación no puede estar seleccionado en la lista de grupos')

        return cleaned_data

    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')

        if not group_name or not isinstance(group_name, str) or group_name.isspace():
            raise forms.ValidationError(
                'Es obligatorio introducir un nombre para el grupo')

        if ParentGroup.objects.filter(name=group_name).exists():
            raise forms.ValidationError(
                f'Ya existe un grupo con nombre \'{group_name}\', por favor, introduce otro nombre')

        return group_name.strip()

    def clean_is_public(self):
        is_public = self.cleaned_data.get('is_public')

        if not isinstance(is_public, bool):
            return forms.ValidationError('Si desea que el grupo sea público, marque la casilla')

        return is_public

    def clean_operation(self):
        operation = self.cleaned_data.get('operation')

        if operation not in {'union', 'intersection', 'difference'}:
            raise forms.ValidationError(
                'Las operaciones disponibles son: union, intersection y difference')

        return operation
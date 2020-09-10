from django import forms

from .models import clientes


class clientesForm(forms.ModelForm):
    class Meta:

        model = clientes
        fields = [

            'nombre',
            'cedula',
            'telefono',
            'marca',
            'matricula',
            'diaentrada',
            'vahiculo',
            'vigencia'

        ]

from django.forms import ModelForm , Form

from .models import Quadro, Empresa
from django import forms


def Empresa_Projetos():
    return [(item[0], '{0}'.format(item[1])) for item in
             Empresa.objects.all().values_list('id', 'nome').order_by('id')]


class QuadroForm(ModelForm):
    class Meta ():
        model = Quadro
        fields = ['descricao',]


class Empresa_ProjetosForm(Form):
        empresas = forms.ChoiceField(choices=Empresa_Projetos(), )
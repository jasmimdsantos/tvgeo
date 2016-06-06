from django.forms import ModelForm , Form

from .models import Quadro, Empresa, Area, ImpactoProjeto, Diagnostico
from django import forms


def Empresa_Projetos():
    return [(item[0], '{0}'.format(item[1])) for item in
             Empresa.objects.all().values_list('id', 'nome').order_by('id')]


def Areas():
    return [(item[0], '{0}'.format(item[1])) for item in
             Area.objects.all().values_list('id', 'nome').order_by('id')]


class QuadroForm(ModelForm):
    class Meta ():
        model = Quadro
        fields = ['descricao',]


class Empresa_ProjetosForm(Form):
        empresas = forms.ChoiceField(choices=Empresa_Projetos(), )


class AreaForm(ModelForm):
    class Meta():
        model = Area
        fields = ['descricao',]

class ImpactoProjetoForm(ModelForm):

    class Meta():
        model = ImpactoProjeto
        fields = ['descricao', 'impacto_FK', 'tipo_area_FK', 'meio_FK', 'area_FK']


class DiagnosticoForm(ModelForm):
    class Meta():
        model = Diagnostico
        fields = ['descricao', 'tipo_area_FK', 'meio_FK', 'area_FK']
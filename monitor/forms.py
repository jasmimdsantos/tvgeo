# -*- coding: utf-8 -*-
#!/usr/bin/env python


from django.db import models
from projetos.models import Campanha, PtoMonit
from param.models import Param, Classe, Legislacao
from django import forms


class frmGrafico(forms.Form):

    TIPO = (
            ('*', ("Todos")),
            ('S', ("Superficie")),
            ('ZF', ("1/2 Zona Fótica")),
            ('F', ("Fundo")),
           )


    usinas = forms.ModelMultipleChoiceField(queryset=PtoMonit.objects.filter(level=1))
    campanhas = forms.ModelMultipleChoiceField(queryset=Campanha.objects.all())
    classe  = forms.ModelChoiceField(queryset=Classe.objects.all())
    legislacao = forms.ModelChoiceField(queryset=Legislacao.objects.all())
    sufixo = forms.ChoiceField(choices=TIPO)


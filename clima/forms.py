# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django import forms

class PesquisaEstacaoFRM(forms.Form):
    nomeEstacao  = forms.CharField(label='Estação', max_length=100)
    nomeTexto    = forms.CharField(label='Texto', max_length=100, initial='', required=False)

class PesquisaAutomaticasFRM(forms.Form):


    MES_CHOICES  = (
        ('99',  'Geral'),
        ('0',  'Anual'),
        ('1',  'Janeiro'),
        ('2',  'Fevereiro'),
        ('3',  'Março'),
        ('4',  'Abril'),
        ('5',  'Maio'),
        ('6',  'Junho'),
        ('7',  'Julho'),
        ('8',  'Agosto'),
        ('9',  'Setembro'),
        ('10', 'Outubro'),
        ('11', 'Novembro'),
        ('12', 'Dezembro'),
    )

    ANO_CHOICES  = (
        ('2014', '2014'),
        ('2015', '2015'),

    )



    nomeEstacao  = forms.CharField(label='Estação', max_length=100)
    ano          = forms.ChoiceField(choices=ANO_CHOICES)
    mes          = forms.ChoiceField(choices=MES_CHOICES)
    nomeTexto    = forms.CharField(label='Texto', max_length=100, initial='', required=False)
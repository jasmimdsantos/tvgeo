# -*- coding: utf-8 -*-
#!/usr/bin/env python

from .regras import Grafico
from django.db import models
from .models import Campanha, PtoMonit, Medicao, Param
from .forms import frmGrafico
from . import prograph
from django.shortcuts import render
from django.shortcuts import render_to_response


def proc_medicao(tipo, colusinas, colcampanha):

    parametros = []
    pontos = []

    for item in PtoMonit.objects.filter(level=2):

        sigla = item.sigla.upper()
        if sigla.endswith('ZF'):
            zona = 'ZF'
        elif sigla.endswith('F'):
            zona = 'F'
        else:
            zona = 'S'

        if item.id not in pontos and \
           (tipo == zona or tipo == '*') and \
           item.parent_id in colusinas:
            pontos.append(item.id)

    for item in Medicao.objects.all():
        if item.Campanha_FK_id in colcampanha :
            if item.PtoMonit_FK_id in pontos :
                if item.Parametro_FK_id not in parametros:
                    parametros.append(item.Parametro_FK_id)

    return parametros, pontos



# Create your views here.
def viewGrafico(request):

    grafJson = ''
    link = ''
    if request.method == 'POST':
            form = frmGrafico(request.POST)
            if form.is_valid():
                colusinas = [ vlr.id for vlr in form.cleaned_data['usinas'] ]
                colcampanha =  [ vlr.id for vlr in form.cleaned_data['campanhas'] ]

                classe     = request.POST['classe']
                sufixo  = request.POST['sufixo']
                legislacao = request.POST['legislacao']

                (parametros, pontos) = proc_medicao(sufixo,
                                          colusinas,
                                          colcampanha)

                link = prograph.processa(pontos, colcampanha, parametros, legislacao, classe )
    else:
        form = frmGrafico()

    return render(request, 'monitor/frmGrafico.html', {'form': form, 'grafJson': grafJson, 'link': link} )


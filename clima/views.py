from django.http import HttpResponse
from django.template import RequestContext , loader
from .forms import PesquisaEstacaoFRM , PesquisaAutomaticasFRM
from . import models as db
from .regras import NormalGraficos
from .graficosa import GeraGraficos
from .regrasa import Medicao
from datetime import datetime
from django.utils import http
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from django.core import serializers
from toolbox import sitetools


@login_required ( )
def clima ( request ):
    context = sitetools.sitemap ( request.get_full_path ( ) ).context
    template = loader.get_template ( 'clima/clima.html' )
    return HttpResponse ( template.render ( context ) )


@login_required ( )
def normais ( request ):
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    if request.method == 'POST':
        form = PesquisaEstacaoFRM ( request.POST )
        if form.is_valid ( ):
            nomeEstac = form.cleaned_data[ 'nomeEstacao' ]
            estacao = db.Station.objects.filter ( Nome__contains=nomeEstac )
            texto = u'{0}'.format ( form.cleaned_data[ 'nomeTexto' ] )

            if texto.strip ( ) == '':
                texto = estacao[ 0 ].Nome

            texto = texto.replace ( '-' , ' ' ).replace ( '.' , ' ' ).replace ( '(' , ' ' ).replace ( ')' , ' ' )
            texto = http.urlquote ( texto )

            if estacao:
                return redirect (
                    '/clima/normais/grafnormais/{0}/{1}/'.format ( estacao[ 0 ].id , texto.replace ( ' ' , '_' ) ) )
    else:
        form = PesquisaEstacaoFRM ( )

    colEstacoes = db.Station.objects.filter ( tipo='N' ).values_list ( 'Nome' , flat=True )
    saida = '['
    for i in colEstacoes:
        saida += '\'' + i + '\','
    saida += ']'

    context = {'estacoes': saida , 'form': form}
    context.update ( page )

    context = RequestContext ( request , context )
    template = loader.get_template ( 'clima/normais.html' )

    return HttpResponse ( template.render ( context ) )


@login_required ( )
def grafnormais ( request , station , texto ):
    page = sitetools.sitemap ( request.get_full_path ( ) ).context

    texto = http.urlunquote ( texto )
    estacao = {}
    try:
        estacao = db.Station.objects.get ( pk=station )
    except:
        return redirect ( '/clima/normais/' )

    grf = NormalGraficos( station , texto ).getGrafico ( )

    template = loader.get_template ( 'clima/grafnormais.html' )

    context = RequestContext ( request , {'estacao': estacao , 'graficos': grf} )
    context.update( page )

    return HttpResponse ( template.render ( context ) )


@login_required ( )
def automaticas ( request ):
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    if request.method == 'POST':

        form = PesquisaAutomaticasFRM ( request.POST )
        if form.is_valid ( ):
            nomeEstac = form.cleaned_data[ 'nomeEstacao' ]
            mes = form.cleaned_data[ 'mes' ]
            ano = form.cleaned_data[ 'ano' ]
            texto = u'{0}'.format ( form.cleaned_data[ 'nomeTexto' ] )
            estacao = db.Station.objects.filter ( Nome__contains=nomeEstac )

            if texto.strip ( ) == '':
                texto = estacao[ 0 ].Nome

            texto = texto.replace ( '-' , ' ' ).replace ( '.' , ' ' ).replace ( '(' , ' ' ).replace ( ')' , ' ' )
            texto = http.urlquote ( texto )

            if estacao:
                if mes == '99':
                    return redirect ( '/clima/automaticas/grafautomaticatotal/{0}/{1}'.format ( estacao[ 0 ].id , texto ) )
                else:
                    return redirect (
                        '/clima/automaticas/grafautomatica/{0}/{1}/{2}/{3}/'.format ( estacao[ 0 ].Codigo , mes , ano , texto ) )
    else:
        form = PesquisaAutomaticasFRM ( )

    colEstacoes = db.Station.objects.filter ( tipo='A' ).values_list ( 'Nome' , flat=True )
    saida = '['
    for i in colEstacoes:
        saida += '\'' + i + '\','
    saida += ']'
    context = RequestContext ( request , {'estacoes': saida , 'form': form} )
    context.update ( page )

    template = loader.get_template ( 'clima/automaticas.html' )

    return HttpResponse ( template.render ( context ) )


@login_required ( )
def grafAutomatica ( request , station , ano , mes , texto ):
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    texto = texto.replace ( '_' , ' ' )

    obj = GeraGraficos ( )
    year = int ( ano )
    month = int ( mes )
    if month == 0:
        tipo = "A"
        month = 1
    else:
        tipo = 'D'

    datadefinida = datetime ( year , month , 1 )
    result = obj.pool ( station , datadefinida , tipo , texto )

    context = RequestContext ( request , {'result': result} )
    context.update ( page )
    template = loader.get_template ( 'clima/graflinha.html' )

    return HttpResponse ( template.render ( context ) )


def getautomaticajson ( request , station ):
    result = json.dumps ( {'dados': Medicao ( ).graficos ( station )} )
    return HttpResponse ( result , content_type='text/javascript' )


def dadosAutomatica ( request , station ):
    result = json.dumps ( {'dados': Medicao ( ).graficos ( station )} )

    return HttpResponse ( result , content_type='text/javascript' )


@login_required ( )
def grafAutomaticaTotal ( request , station , texto ):
    texto = texto.replace ( '_' , ' ' )
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    estacao = {}
    try:
        estacao = db.Station.objects.get ( pk=station )
    except:
        return redirect ( 'clima/estacoes/' )

    if texto.strip ( ) == '':
        texto = estacao.Nome

    credits = {'text': 'Powered by: Terravision' ,
               'href': 'http://www.terravisiongeo.com.br/'
               }

    context = RequestContext ( request , {'estacao': estacao , 'credits': credits , 'texto': texto} )
    context.update ( page )
    template = loader.get_template ( 'clima/grafautomaticatotal.html' )

    return HttpResponse ( template.render ( context ) )


@login_required ( )
def mapaestacoes ( request ):
    context = RequestContext ( request )
    template = loader.get_template ( 'clima/mapaestacoes.html' )
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )
    return HttpResponse ( template.render ( context ) )


def mapafocoincendio ( request ):
    context = RequestContext ( request )
    template = loader.get_template ( 'clima/mapafocoincendio.html' )
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )

    return HttpResponse ( template.render ( context ) )


def focoCalor ( request , id ):
    reg = db.FocoItem.objects.get ( id=id )

    saida = {'Temp': reg.Temp , 'FireFlag': reg.FireFlag , 'Data': reg.foco_FK.dataUTC , 'id': reg.id}
    context = RequestContext ( request , {'foco': saida} )
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )
    template = loader.get_template ( 'clima/focoCalor.html' )

    return HttpResponse ( template.render ( context ) )

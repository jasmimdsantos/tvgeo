# -*- coding: utf-8 -*-
#!/usr/bin/env python

import django
from normais.models import Parametro, Classe, Resultado
import json

# convert a dictionary to a class
class Struct(object):
    def __init__(self, adict):
        """
        Convert a dictionary to a class
        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

def get_object(adict):
    """
    Convert a dictionary to a class
    @param :adict Dictionary
    @return :class:Struct
    """
    return Struct(adict)



class Chart:

    def it(self, _tipo, _title, _xAxis, _yAxis, _pltOptions,_credits,  _legend, _series, _id, _subtitle):

        saida = { }

        saida['id'] = _id

        if not  _tipo:
            raise ValueError('Tipo não definido');

        saida['type'] = _tipo

        if _title:
            saida['title'] = { 'text' :  _title }

        if _title:
            saida['subtitle'] = { 'text' :  _subtitle }

        if _xAxis:
            saida['xAxis'] = _xAxis

        if _yAxis:
            saida['yAxis'] = _yAxis

        if _pltOptions:
            saida['plotOptions'] =  _pltOptions

        if _credits:
            saida['credits'] = _credits

        saida['legend'] =  'true' if  _legend else 'false'

        if _series:
            saida['series'] = _series

        return saida

class NormalGraficos:



    def __init__(self, _idStation, _texto):
        self.idStation = _idStation
        self.yAxis = ''
        self.meses = ['jan','fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago','stb', 'out', 'nov', 'dez']
        self.texto = _texto.replace('_', ' ')


    def getEixo(self, idSerie):

        data = []
        resultParam = Parametro.objects.get(codigo = idSerie)

        resultSerie  = Resultado.objects.filter(
                                        Station_FK_id = self.idStation,
                                        Parametro_FK__codigo = idSerie)
        if len(resultSerie) > 0:
            dicionario = resultSerie[0].__dict__
            for mes in self.meses:
                data.append( float(dicionario[mes]))

        self.yAxis =  {
                         'title': {  'text': resultParam.unidade.encode('latin-1')}
                      }



        saida =  {'name' : resultParam.Nome.encode('latin-1') , 'color': resultParam.corGrafico.encode('latin-1'), 'data' : data   }

        return saida



    def plotOptions(self,tipo):

        plotOptions = ''
        if tipo == 'line':
            plotOptions =  { 'line' : {    'dataLabels': {  'enabled': 'true'  } }  }
        else:
            plotOptions = {  'column': {'pointPadding': 0.1, 'borderWidth': 0,
                                        'dataLabels': {'enabled': 'true' }  } }

        return plotOptions

    def getGrafico(self):


        xAxis = { 'categories'  :  self.meses, 'crosshair': 'true'  }

        credito = {  'text': 'Fonte: INMET 1961-1990 -  Powered by Terravision',
                     'href': 'http://www.terravisiongeo.br/'
                  }

        colGrafico = []
        col = [    {    'id'        : 1,
                        'title'     : 'Precipitação Acumulada',
                        'tipo'      : 'column',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [11,] },

                   {    'id'        : 2,
                        'title'     : 'Temperaturas',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : True,
                        'series'    : [1,2,3,] } ,
                   {    'id'        : 3,
                        'title'     : 'Precipitação Máxima 24h',
                        'tipo'      : 'column',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [12,] } ,
                   {    'id'        : 4,
                        'title'     : 'Temperatura Mínima Absoluta',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [5,] } ,
                   {    'id'        : 5,
                        'title'     : 'Temperatura Máxima Absoluta',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [4,] } ,
                   {    'id'        : 6,
                        'title'     : 'Deficit e Superávit Hídrico',
                        'tipo'      : 'area',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [19,] } ,
                   {    'id'        : 7,
                        'title'     : 'Umidade Relativa',
                        'tipo'      : 'column',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [10,] } ,
                   {    'id'        : 8,
                        'title'     : 'Nebulosidade',
                        'tipo'      : 'area',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [9,] } ,
                   {    'id'        : 9,
                        'title'     : 'Pressão',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [6,] },
                   {    'id'        : 10,
                        'title'     : 'Insolação',
                        'tipo'      : 'column',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [7,] } ,
                   {    'id'        : 11,
                        'title'     : 'Dias com Chuva',
                        'tipo'      : 'column',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [13,] } ,
                   {    'id'        : 12,
                        'title'     : 'Direção Predominante do Vento',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : True,
                        'series'    : [14,15,16,17,18,] },
                   {    'id'        : 13,
                        'title'     : 'Velocidade do Vento',
                        'tipo'      : 'line',
                        'categ'     : 99,
                        'credito'   : 0,
                        'legend'    : False,
                        'series'    : [14,] },
            ]

        for item in col:

            colSeries = []
            for parametro in  item['series']:

                if item['id'] == 12:
                    continue

                linha = self.getEixo(parametro)
                if item['tipo'] == 'area':
                    linha['negativeColor'] = 'red'


                if len(linha['data']) > 0:
                    colSeries.append(  linha )

            if len(colSeries) > 0:
                itemGrafico = Chart().it( item['tipo'],
                                     item['title'],
                                     xAxis,
                                     self.yAxis,
                                     self.plotOptions(item['tipo']),
                                     credito,
                                     item['legend'],
                                     colSeries,
                                     item['id'],
                                     self.texto )


                colGrafico.append(itemGrafico)

        return colGrafico

"""
http://jsfiddle.net/5m4djL4b/
http://jsfiddle.net/5r3ffoky/
http://jsfiddle.net/w172sc4t/

"""
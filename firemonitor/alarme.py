# -*- coding: utf-8 -*- 
#!/usr/bin/env python 

import django
import requests
from toolbox.staticmap import StaticMap
from .models import Projeto, Camada, Equipe, FocoWFABBA
from .models import Alarme, ItemAlarme, FocoFIRMS
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.geos import GEOSGeometry, Polygon
from  toolbox.maillib import Email
from django.contrib.sites.models import Site

def KelvinToCelcius(t):
    if t <0:
        return t
    return float(t)- float(273.15)


class AlarmeProc:

    def __init__(self):
        self.__Alarme = None
        self.__Projeto = None

    def __addAlarme(self):

        obj = Alarme(Projeto_FK = self.__Projeto)
        obj.save()
        self.__Alarme = obj

    def __getPolygon(self, url):

        ds = DataSource(url)
        layer = ds[0]
        col = layer.get_geoms()
        self.__centroid = ( col[0][0].centroid.x,\
                            col[0][0].centroid.y  )
        self.__poly = layer

    def __addItemAlarme(self, record):

        query = ItemAlarme.objects.filter( foco_id = record.id)
        self.__poly.spatial_filter = record.posicao.extent

        if len(query) == 0 and len(self.__poly) > 0:

            if not self.__Alarme :
                self.__addAlarme()

            objRegra = ItemAlarme() 
            objRegra.Alarme_FK = self.__Alarme
            objRegra = FocoToItemAlarme().\
                       getMixin(record,objRegra)
            objRegra.save()

            self.__poly.spatial_filter = None

    def __processaProjeto(self, table):

        for record in table:
            self.__addItemAlarme(record)

    def processa(self):
        for record in Projeto.objects.all():
            objcamada = Camada.objects.filter( Projeto_FK__id = record.id,\
                                               isExtent = True )[0]
            self.__getPolygon( objcamada.url) 
            self.__Projeto = record 

            self.__processaProjeto(FocoFIRMS.objects.all())
            self.__processaProjeto(FocoWFABBA.objects.all())

            markers = []
            for item in ItemAlarme.objects.filter(Alarme_FK = self.__Alarme):
                markers.append( [ item.posicao[0], item.posicao[1] ] ) 

            if len(markers) > 0:
                mapa = StaticMap()
                mapa.markers = markers 
                mapa.filename = 'mapaAlarme{0}'.format(self.__Alarme.id)
                path = mapa.processa( self.__centroid) 
            
                url = 'http://' + Site.objects.get_current().domain +  '/mailalertafoco/{0}/'.\
                    format(self.__Alarme.id)

                r = requests.get(url)

                for item in Equipe.\
                            objects.\
                            filter(Projeto_FK_id = self.__Projeto.id):
                            destinatario = '{0} <{1}>'.\
                                        format(item.nome,\
                                                item.email)

                            objMail = Email()
                            objMail.EnviaMSG('Fire Monitor - Alerta de Foco de Incêndio',
                                            r.content,
                                            [ destinatario, ],
                                            True )

 


class FocoToItemAlarme:
   
    def __confidencialidade_wfabba(self, flag):

        percent = [100,90,85,70,60, 20]
        return percent[flag]

    def getMixin(self, record, objItemAlarme ): 
          
        modelo = (  'dataregUTC', 'dataUTC', 'posicao', \
                    'temp', 'confianca', 'satellite',\
                    'pixsize', 'firesize', 'foco_id', 'alg' )

        firms  = (  'dataregUTC', 'dataUTC', 'posicao', \
                    'bright', 'confidence',   'satellite',\
                    'scan', 'track', 'id', 'FIRMS')

        wfabba = (  'dataregUTC', 'dataUTC', 'posicao',\
                    'Temp', 'FireFlag', 'satellite',\
                    'PixSize', 'FireSize', 'id', 'WAFBBA')

        table = firms if type(record) == FocoFIRMS else wfabba

        objInstance = {}
        indice = 0 
        for cpo in table:
            key = modelo[indice]
            value = None
            if key == 'alg':
                value = cpo
            if key == 'satellite': 
                if table == firms:
                    value = 'AQUA' if value == 'A' else 'TERRA' 
                else:
                    value = 'Goes-13'

            if not value:
                value = getattr(record,cpo)
    
            if key == 'temp':
                value = KelvinToCelcius(value)

            if key == 'confianca':
                if table == wfabba:
                    value = self.__confidencialidade_wfabba(value)


            setattr(objItemAlarme, key, value)
            indice += 1

        return  objItemAlarme
 


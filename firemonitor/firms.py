# -*- coding: utf-8 -*- 
#!/usr/bin/env python 

import django
from monitor.models import FocoFIRMS
from datetime import datetime, timedelta
from dateutil import parser
from ftplib import FTP
import sys
from os import path, walk,  remove
import shutil
from normais.models import Station
from proj import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import OGRGeometry

class FIRMS:

    class FireFtp():

        def processa(self, data):
            arquivo = 'South_America_MCD14DL_{0}{1}.txt'.\
                      format( data.year,\
                              data.timetuple().tm_yday)

            url = 'nrt1.modaps.eosdis.nasa.gov'
            caminho = 'FIRMS/South_America/' 
            entrada =  settings.FIRMS_PATH + '/entrada/'
            saida   =  settings.FIRMS_PATH + '/saida/'

            try:
                ftp = FTP(url)
                ftp.login('nlima', 'Wilson2013')
                ftp.cwd (caminho)

                gravar = entrada + arquivo
                ftp.retrbinary('RETR ' +  arquivo, open(gravar, 'wb').write) 
                ftp.quit()
            except:
                raise


    def __init__(self):
        

        f = self.FireFtp()
        #  Processa ontem
        ontem = datetime.now() - timedelta(days=1)
        f.processa( ontem )

        #processa hoje
        f.processa( datetime.utcnow() )
        
        del f

        url = 'http://geonode.terravisiongeo.com.br/geoserver/geonode/ows?\
service=WFS&version=1.0.0&request=GetFeature&typeName=geonode:estados_2010&\
CQL_FILTER=regiao_id=4%20or%20id=1&outputFormat=application/json'
        ds = DataSource(url)
        self.layer = ds[0]

    def getArquivos(self):

        entrada =  settings.FIRMS_PATH + '/entrada/'
        saida   =  settings.FIRMS_PATH + '/saida/'
        arquivos = []

        for dirpath, dirs, files in walk(entrada):  
            for file in files:
                caminho = [  '{0}{1}'.format(dirpath, file),\
                             '{0}{1}'.format(saida, file) ] 
                arquivos.append(caminho)

        return arquivos


    def processa(self):
        for arquivo, arqsaida in self.getArquivos():

            f = open(arquivo, 'r')
            dados = []
            for line in f:
                dados.append( line.split(','))
            f.close()

            for reg in dados[1:]:
                mask = '{0} {1}:00'.format(reg[5], reg[6])

                _dataRegUTC = datetime.utcnow()
                _posicao    = 'SRID=4326;POINT({0} {1})'.format(reg[1], reg[0])
                _bright     = float(reg[2] )
                _scan       = float(reg[3])
                _track      = float(reg[4])
                _dataUTC    = parser.parse(mask) 
                _satellite  = reg[7]
                _confidence = float(reg[8])
                _version    = reg[9] 
                _brightT31  = float(reg[10])
                _frp        = float(reg[11])
               
                ponto = OGRGeometry(_posicao)
                self.layer.spatial_filter = ponto.extent

                query = FocoFIRMS.objects.filter(dataUTC = _dataUTC,\
                                                 posicao = _posicao,\
                                                 satellite = _satellite)

                if ( len(self.layer) > 0 and len(query) == 0 ) :
                   regFocoItem = FocoFIRMS(dataregUTC = _dataRegUTC,\
                                           posicao    = _posicao,\
                                           bright     = _bright,\
                                           scan       = _scan,\
                                           track      = _track,\
                                           dataUTC    = _dataUTC,\
                                           satellite  = _satellite,\
                                           confidence = _confidence,\
                                           version    = _version,\
                                           brightT31  = _brightT31,\
                                           frp        = _frp\
                                        )

                   regFocoItem.save()

                self.layer.spatial_filter = None 

            # Se já foi processado apaga 
            if path.isfile(arqsaida):
                remove(arqsaida)

            shutil.move(arquivo, arqsaida)


def run():
    obj = FIRMS()
    obj.processa()

if __name__ == "__main__":
    obj = FIRMS()
    obj.processa()





import ftplib


from .models import FocoWFABBA
from datetime import datetime, timedelta
from ftplib import FTP
from os import path, walk
import shutil
import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import OGRGeometry

class WFABBA:

    class FireFtp():

        def diretorio(self):
            return '{0}{1}'.format( datetime.utcnow().year,
                                    datetime.utcnow().timetuple().tm_yday)

        def processa(self):
            url = 'ftp.ssec.wisc.edu'
            caminho = 'pub/abba/v65/goes-13/text/' + self.diretorio()
            entrada = settings.WFABBA_PATH + '/entrada/'
            saida  =  settings.WFABBA_PATH + '/saida/'
            ftp = FTP(url)
            ftp.login()
            ftp.cwd (caminho)

            try:
                files = ftp.nlst()
            except ftplib.error_perm as resp:
                if str(resp) == "550 No files found":
                    print("No files in this directory")
                else:
                    raise

            for arquivo in files:
                naoExisteEntrada = not path.exists(entrada + arquivo)
                naoExisteSaida = not path.exists(saida + arquivo)

                if  naoExisteSaida and naoExisteEntrada:
                    gravar = entrada + arquivo
                    ftp.retrbinary('RETR ' +  arquivo, open(gravar, 'wb').write)
            ftp.quit()

    def __init__(self):

        f = self.FireFtp()
        f.processa()
        url = 'http://geonode.terravisiongeo.com.br/geoserver/geonode/ows?\
service=WFS&version=1.0.0&request=GetFeature&typeName=geonode:estados_2010&\
CQL_FILTER=regiao_id=4%20or%20id=1&outputFormat=application/json'
        ds = DataSource(url)
        self.layer = ds[0]

    def getArquivos(self):

        entrada = settings.WFABBA_PATH + '/entrada/'
        saida  =  settings.WFABBA_PATH + '/saida/'
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
                dados.append( line.split())
            f.close()
            

            ano    = int(dados[3][1][:4]) 
            mes    = 1
            dia    = 1
            hora   = int(dados[3][3][:2])
            minuto = int( dados[3][3][-2:]) 

            datahora = datetime(ano, mes, dia, hora, minuto) 
            
            dias   = int(dados[3][1][-3:]) - 1
            datahora = datahora + timedelta(days=dias)

            datareg = datetime.utcnow()

            for reg in dados[5:]:
                _posicao = 'SRID=4326;POINT({0} {1})'.format(reg[0], reg[1])
                _Satzen      = float(reg[2] ) 
                _PixSize     = float(reg[3] )
                _T4          = float(reg[4] )
                _T11         = float(reg[5] ) 
                _FireSize    = float(reg[6] ) 
                _Temp        = int(reg[7].replace('.','')   )
                _FRP         = int(reg[8].replace('.','')   )
                _Ecosystem   = int(reg[9].replace('.','')   )
                _FireFlag    = int(reg[10].replace('.','')  )



                ponto = OGRGeometry('POINT ({0} {1})'.format(reg[0], reg[1]))
                self.layer.spatial_filter = ponto.extent
                if len(self.layer) > 0 :
                    regFocoItem = FocoWFABBA( dataUTC     = datahora,
                                              dataregUTC  = datareg,
                                              arquivo     = arquivo,
                                              posicao     = _posicao,
                                              Satzen      = _Satzen,
                                              PixSize     = _PixSize,
                                              T4          = _T4,
                                              T11         = _T11,
                                              FireSize    = _FireSize,
                                              Temp        = _Temp,
                                              FRP         = _FRP,
                                              Ecosystem   = _Ecosystem,
                                              FireFlag    = _FireFlag )
                    regFocoItem.save()

                self.layer.spatial_filter = None

            shutil.move(arquivo, arqsaida)


def run():
    obj = WFABBA()
    obj.processa()


if __name__ == "__main__":
    obj = WFABBA()
    obj.processa()





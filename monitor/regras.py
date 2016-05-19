# -*- coding: utf-8 -*-
#!/usr/bin/env python

import django
from projetos.models import Medicao, PtoMonit, Campanha
from param.models import  Param
import datetime

import requests
import base64
import json


def getCampanha(idProjeto, dataHora):

    colCampanha = Campanha.objects.\
                    filter(Projeto_FK_id = idProjeto,\
                            ano = dataHora.year,\
                            mes = dataHora.month)

    if len(colCampanha)  == 0:
        nmCamp = 'Campanha {0}/{1}'.format(dataHora.month, dataHora.year)
        objCampanha = Campanha( nome = nmCamp,
                                mes  =  dataHora.month,
                                ano  =  dataHora.year,
                                Projeto_FK_id = idProjeto)
        objCampanha.save()
    else:
        objCampanha = colCampanha[0]

    return objCampanha


class Grafico:

        def __getGrafico(self):
            cfg = self.__getJson()
            option = {"infile":cfg,"constr":"Chart"}
            url = 'http://tvbhdesenv.terravision.local:3003/'
            headers = {"Content-Type": "application/json" }
            r = requests.post(url, headers=headers, data= json.dumps(option)  )
            imgdata = base64.b64decode(r.content)

            t = datetime.datetime.now()
            arquivo = str((t-datetime.datetime(1970,1,1)).total_seconds()) + '.jpeg'
            with open(self.arquivo, 'wb') as f:
               f.write(imgdata)
            return arquivo


        def __getJson(self):
            cfg = "{ title: { text: '" + self.titulo +"' } ,\
                     subtitle: { text: '" + self.subtitulo + "' },\
                     credits : { enabled : true, text : 'powered by: Brandt Meio Ambiente'},\
                     xAxis: { categories: " + self.categorias + " },\
                     yAxis: { min: 0, title: { text: '" + self.unidade + "' }, tickInterval:"  + self.interval + "},\
                     series:" + self.series + " }"
            return cfg

        def __Processa(self, idParametro, pontos, campanhas):
            mat = []
            MESES = ('---', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov',' dez')


            colMedicao = Medicao.objects.filter(Parametro_FK_id = idParametro).all()
            if len(pontos) > 0:
                colMedicao = colMedicao.filter(PtoMonit_FK_id__in=pontos).all()
            if len(campanhas) > 0:
                colMedicao = colMedicao.filter(Campanha_FK_id__in=campanhas).all()

            col =[]
            acamp = []
            aptos = []
            for item in colMedicao:
                idCamp  = item.Campanha_FK_id
                idPonto = item.PtoMonit_FK_id

                if idCamp not in acamp:
                    acamp.append(idCamp)

                if idPonto not in aptos:
                    aptos.append(idPonto)

                col.append( [idCamp ,idPonto , float(item.vlr) ])

            for y in acamp:
		for x in aptos:
			z = [ vlr for  vlr in col if vlr[0] == y and vlr[1] == x]
			if len(z) == 0:
                            col.append( [y, x, -1] )


            objParam  = Param.objects.get(pk=idParametro)
            resultParametro = u'{0} - {0} '.format(objParam.nome, objParam.unidade_FK.sigla)

            resultPontos  = [ str(sigla.encode('ascii', 'ignore')) for sigla in PtoMonit.objects.filter(id__in=aptos).values_list('sigla', flat=True) ]

            aValores  = []
            colCampanha = [ '{0}/{1}'.format(MESES[mes],+ano) for ano,mes  in  Campanha.objects.filter(id__in=acamp).values_list('ano', 'mes')]
            acamp.append('VMP')
            indice = 0
            for itcamp in acamp:
                if itcamp == 'VMP':
                    linha = ([ 'VMP', [ float(objParam.vlrTeto) for x in resultPontos ] ])
                else:
                    linha = ([ colCampanha[indice], [ float(x[2]) for x in col if  x[0] == itcamp  ] ])
                    indice += 1
                aValores.append(linha)



            series = "["
            for item in aValores:
                if item[0] == 'VMP':
                    itemSeries = "{ type:'line', color:'red' , name:'" +  item[0] + "',  data:" + str(item[1]) + "},"
                else:
                    itemSeries = "{ type:'column' , name:'" +  item[0] + "',  data:" + str(item[1]) + "},"

                series += itemSeries
            series = series[0:-1] +  "]"

            self.titulo = ''
            self.subtitulo = ''
            self.unidade = objParam.nome + '-' + objParam.unidade_FK.sigla
            self.categorias = str(resultPontos)
            self.series = series
            self.interval = str(objParam.intervalo)


	def runFile(self, idParametro, pontos, campanhas):
            self.__Processa(idParametro, pontos, campanhas)
            sefl.__getGrafico()

	def runJson(self, idParametro, pontos, campanhas):
            self.__Processa(idParametro, pontos, campanhas)
            return self.__getJson()

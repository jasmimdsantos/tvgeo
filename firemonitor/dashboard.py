# -*- coding: utf-8 -*-
#!/usr/bin/env python

import django
from .models   import KPI, KPI_Nivel, Projeto, Equipe
from .fma      import FMA
from toolbox.tools    import ObjectView
from .previsao import Previsao
from roi.models       import ROI
from .models   import Alarme, ItemAlarme
from datetime         import datetime, date, timedelta
from toolbox.tools    import add_months

class DashBoard:
        
    def execute(self, idProjeto, data):

        dash = {}

        reg = Projeto.objects.get(id = idProjeto)

        dash['projeto'] = u'{0} - {1}'.format( reg.codigo, reg.nome)

        dash['equipe'] = Equipe.objects.filter(Projeto_FK = idProjeto)

        objFMA = FMA()
        dash['estacao']  = objFMA.getEstacaoByOMM(reg.wmo_automatica)
        dash['clima'] = objFMA.getClima(reg.wmo_automatica, data)

        colecao = objFMA.formula(reg.wmo_automatica, data)
        dash['fma'] =  colecao
        situaacaoatual  = colecao[-1]

        data = situaacaoatual.data
        dash['data']        = data 

        dash['parametros']  = self._DahsParametros(situaacaoatual)

        dash['colorFMA']  = dash['parametros'][5].color
        dash['colorFMAP'] = dash['parametros'][6].color 

        dash['previsao']  = Previsao(reg.codIBGE)

        dash['graphFMA'] = self.GraficoFMA(colecao)
        
        dash['roi'] = ROI\
                       .objects\
                       .values( 'id', 'ROIID',\
                               'municip', 'distrito',\
                               'local', 'responsavel',\
                               'data')\
                       .all() 


        dash['alarme'] = ItemAlarme.objects.all().select_related()







        return  ObjectView(dash)



    def GraficoFMA(self, colecao):

        colFMA   = [ float(item.fma)  for item in colecao ] 
        colFMAP  = [ float(item.fmap) for item in colecao ]    

        graph = {}
        graph['titulo'] = 'Formula de Monte Alegre'
        graph['subtitulo'] =  str(colecao[-1].data)
        graph['tituloY'] = 'Indice da Formula'
        graph['unidade'] = 'indice'


        data = colecao[0].data
        data = add_months(data, -1) 
        dia  = {}
        dia['dia'] = int(data.day)
        dia['mes'] = int(data.month)
        dia['ano'] = int(data.year)

        graph['data'] = dia

        col = []
        objKPI = KPI.objects.get(nome = 'FMA')
        for item in KPI_Nivel.objects.filter( KPI_FK = objKPI):
            linha = [  float( item.v1), 
                       float( item.v2), \
                       str(item.cor), 
                       str(item.texto), \
                       str("#606060") ]
            col.append(linha)

        graph['plotBands'] = col

        graph['series'] = [ ['FMA' , colFMA], ['FMA+', colFMAP ]  ]

        return graph





    def _DahsParametros(self, resultFMA):
        
        camposParametro = ('ordem', 'nome', 'unidade', 'icone', 'msg', )

        campos = ('diaschuva', 'velVento', 'umid', 'pressao',\
                    'temperatura','fma', 'fmap',)

        pos = (1,3, 4, 5, 6, 7, 8)
        
        col = []

        indice = 0
        for item in campos:
            registro = {}
            objKPI = KPI.objects.get(ordem = pos[indice] ) 
            vlr  =  getattr(resultFMA, item)
            for param in camposParametro:
                registro[param] = getattr(objKPI, param)

            limite = KPI_Nivel.objects.filter(KPI_FK_id = objKPI)
            for reg in limite:
                if  vlr >= reg.v1 and vlr <= reg.v2:
                    break

            if len(limite) > 0:
                registro['color'] = reg.cor
            else:
                registro['color'] = 'black'
            
            registro['valor'] = vlr

            indice +=1

            col.append(ObjectView(registro))

        return col

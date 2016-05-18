# -*- coding: utf-8 -*- 
#!/usr/bin/env python 

import requests
import json
from   toolbox.tools  import  ObjectView
from   datetime import datetime

def Previsao(codIBGE):

    mask = 'http://www.inmet.gov.br/portal/index.php?\
r=tempo2/previsaoDeTempo&code={0}'

    url = mask.format(codIBGE)

    req  = requests.get(url)
    saida = json.loads( req.content)

    col = []
    datas = []
    indice = 0

    for dia in saida[codIBGE]:
        if len(saida[codIBGE][dia]) == 3:
            campo = saida[codIBGE][dia]['tarde']
        else:
            campo = saida[codIBGE][dia]


        data = datetime.strptime(dia, '%d-%m-%Y')
        datas.append( (data.timetuple().tm_yday, indice) )
        indice += 1

        campo['data'] = dia
        obj = ObjectView(campo)
        col.append( obj )

    saida = []
    for item in  sorted(datas, key=lambda datas: datas[0]):
        key = item[1]
        saida.append(col[key])

    return saida 




# -*- coding: utf-8 -*-
#!/usr/bin/env python


from  param.models    import Param
from  projetos.models import PtoMonit, Medicao, Projeto, Campanha
from  toolbox.tools   import ObjectView
from  toolbox.tools   import lerDataExcel, convert_excel_time
import xlrd
from  toolbox.maillib import Email
from django.utils import timezone
from datetime import datetime
from xlwt import Workbook
import os
import time

PARAMETRO_DATA = 840

PATH_FERRAMENTA  = '/media/projeto_cemig/01_PROJETO SOFTWARE/converte.xls'


def converte(folha=0):

    """ Pontos de monitoramento """
    workbook = xlrd.open_workbook(PATH_FERRAMENTA)
    pontoConv = {}
    sheet = workbook.sheet_by_index(folha)
    for row in range(1, sheet.nrows):
       _de   = sheet.cell(row,0).value
       _de   = _de.strip()
       _para = sheet.cell(row,1).value
       _para = u'{0}'.format(_para).strip()

       pontoConv[_de] = _para

    return pontoConv


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


def isMedicao(_ponto, _param, _data):

    col = Medicao.objects.filter(data = _data,
                                PtoMonit_FK = _ponto,
                                Parametro_FK = _param )

    return len(col) == 0


def run():

    idProjeto = 1
    caminho = "/media/projeto_cemig/01_PROJETO SOFTWARE/DADOSDECAMPO.xls"
    erros = []
    errosParam = 0

    workbook = xlrd.open_workbook(caminho)
    sheet = workbook.sheet_by_index(0)
    inLancto = False

    pontoConv = converte()

    colPos = [5,6,7,8,9,10,11,12]
    colMedicao = []

    for row in range(0, sheet.nrows):


        if row == 0:
            for col in colPos:
                idParam =  int(sheet.cell(row, col).value)
                objparam = Param.objects.filter(id = idParam)
                if len(objparam) == 0:
                    erros.append({  'linha':row, \
                                    'valor' : idParam,\
                                    'msg':'Parametro nao encontrado'\
                                 })
            errosParam = len(erros)

        if row >= 2 and errosParam == 0 :
            codEstacao = sheet.cell(row, 1).value
            codEstacao = codEstacao.replace(' ','').replace('-','').strip()
            old = codEstacao

            if codEstacao in pontoConv:
                codEstacao = pontoConv[codEstacao].strip()
                codEstacao  = codEstacao.replace(' ','').replace('-','').strip()

            if codEstacao == u'excluir' or codEstacao == u'EXCLUIR' or codEstacao == u'Excluir' :
                return False

            objEstacao = PtoMonit.objects.filter(sigla= codEstacao)

            if len(objEstacao) == 0:
                erros.append({  'linha':row, \
                                'valor' : codEstacao,\
                                'msg':'Ponto nao existe'\
                            })
                continue

            try:
                data = lerDataExcel(sheet.cell(row,3).value)
                hr = sheet.cell(row,4).value
                hora = convert_excel_time(hr, False)
                mask = '{0} {1}'.format(data, hora)
            except:
                erros.append({  'linha' : row, \
                                'valor' : sheet.cell(row,3)  ,\
                                'msg'   : 'Data ou hora com formatos invalidos'\
                                 })
                continue


            dataHora1 = datetime.strptime(mask, '%d-%m-%Y %H:%M:%S')
            dataHora = timezone.make_aware(dataHora1, timezone.get_current_timezone())


            valores = []
            for col in colPos:
                vlr    = sheet.cell(row, col).value
                if vlr == '':
                    vlr = 0.0

                try:
                    vlrF = float(vlr)
                except:
                   erros.append({  'linha':row, \
                                    'valor' : vlr ,\
                                    'msg':'Campo valor formato invalido'\
                                     })
                   continue

                param  = sheet.cell(0, col).value
                valores.append( [param, vlrF] )

                """ Se for a primeira passagem do loop insere o parametro data para
                    exibir na planilha
                """
                if colPos.index(col) == 0:
                    param = valores.append( [PARAMETRO_DATA, 0] )

            registro = {'codEstacao' : codEstacao,               \
                        'data'       : dataHora,                 \
                        'controle'   : 'DADOS CPO:{0}'.format(row),  \
                        'valores'    : valores                   \
                       }
            item =ObjectView(registro)
            colMedicao.append(item)



    PATH_SAIDA  = '/media/projeto_cemig/01_SOFTWARE/'
    workbook = Workbook()
    sheet = workbook.add_sheet('Sheet1')

    y = 1
    for item in erros:
        sheet.write(y, 0, u'{0}'.format(item['linha']) )
        sheet.write(y, 1, u'{0}'.format(item['valor']) )
        sheet.write(y, 2, u'{0}'.format(item['msg']) )
        y +=1

    novodir = '{0}{1}/'.format(PATH_SAIDA, datetime.now() )
    os.makedirs(novodir)
    path_saida ='{0}{1}.xls'.format(novodir, 'DadosCampo_error')
    workbook.save(path_saida)
    print('Erros salvos')

    label = None
    for item in colMedicao:

        objEstacao = PtoMonit.objects.get(sigla= item.codEstacao)
        objCampanha = getCampanha(idProjeto, item.data.date())

        for param, valor in item.valores:
            objParam = Param.objects.get(id= param)

            if param == PARAMETRO_DATA:
                label =item.data.isoformat()
            else:
                label = str(valor)


            if isMedicao(objEstacao, objParam,  item.data):
                objMed = Medicao(Campanha_FK = objCampanha, \
                                PtoMonit_FK = objEstacao,  \
                                Parametro_FK = objParam,   \
                                controle = item.controle,  \
                                data = item.data,          \
                                vlr  = valor,         \
                                vlrLbl = label)
                objMed.save()



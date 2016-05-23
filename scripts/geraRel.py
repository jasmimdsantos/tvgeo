# -*- coding: utf-8 -*-
#!/usr/bin/env python

import django
from param.models import Unidade, Param
from projetos.models import Medicao, PtoMonit, Projeto, Campanha
from toolbox.tools import ObjectView, xlsDate_as_datetime
from projetos.regras import getCampanha
from xlwt import Workbook, XFStyle
import time

def run():

    col_label_param = {}
    for item in Param.objects.values('id','nome', 'vlrTeto', 'vlrPiso', 'unidade_FK__sigla').order_by('nome').all():
       col_label_param[ item['id'] ] = [ item['nome'],  item['vlrPiso'], item['vlrTeto'], item['unidade_FK__sigla'], ]

    col_label_ponto = {}
    for item in PtoMonit.objects.values('id','sigla').all():
       col_label_ponto[ item['id'] ]  = item['sigla']

    col_label_Ponto = PtoMonit.objects.all()

    col_param = []
    col_linha = []
    result = []
    colMedicao =  Medicao.objects.values('data', 'Parametro_FK_id',
                                         'PtoMonit_FK_id', 'Parametro_FK__nome',
                                         'vlrLbl', 'Campanha_FK__nome',
                                         'Parametro_FK__nome').order_by('Parametro_FK__nome', 'data',)
    linha = []
    for item in colMedicao:

        key_param = ( item['Parametro_FK_id'])
        try:
            indice_param = col_param.index(key_param)
        except ValueError:
            col_param.append(key_param)
            indice_param = col_param.index(key_param)


        key_linha = (item['data'].date(), item['PtoMonit_FK_id'], item['data'], item['Campanha_FK__nome'],)
        try:
            indice_linha = col_linha.index(key_linha)
        except ValueError:
            col_linha.append(key_linha)
            indice_linha = col_linha.index(key_linha)

        registro = (indice_linha, indice_param, item['vlrLbl'].replace('.',','))

        result.append(registro)


    workbook = Workbook()
    sheet = workbook.add_sheet('Sheet1')

    cabec = [u'Mês', 'Ponto', '-//-', 'Data Amostragem', 'Campanha', 'Ano', 'Hora Amostragem', 'Tempo', u'Última Chuva Antes', ]
    for item in cabec:
        sheet.write(0, cabec.index(item), item)


    for item in col_param:
        y = col_param.index(item)
        y += 9
        sheet.write(0, y, col_label_param[item][0])
        sheet.write(1, y, col_label_param[item][1])
        sheet.write(2, y, col_label_param[item][2])
        sheet.write(4, y, col_label_param[item][3])

    date_format = XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    time_format = XFStyle()
    time_format.num_format_str = 'h:mm:ss'

    for item in col_linha:
        x = col_linha.index(item)
        x += 5
        sheet.write(x, 1, col_label_ponto[item[1]] )
        dt = item[2]
        try:
            sheet.write(x, 0, '{0}/{1}'.format(dt.month, dt.year) )
            sheet.write(x, 3, dt.date(), date_format)
            sheet.write(x, 4, item[3] )
            sheet.write(x, 5, '{0}'.format(dt.year) )
            sheet.write(x, 6, dt.time(), time_format)
        except:
            print(dt )


    for item in result:
        x, y, z = item
        x += 5
        y += 9
        z = z
        try:
            sheet.write(x, y, z)
        except:
            pass

    path_saida = '/media/projeto_cemig/01_SOFTWARE/planilha_geral.xls'
    workbook.save(path_saida)



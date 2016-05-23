# -*- coding: utf-8 -*-
import os
import xlrd
import os
import sys
import xlwt
import datetime as dt
from types import *

arquivos = []
import datetime as dt


def Converte_Data(param):
    try:
        data_int = xlrd.xldate_as_tuple(int(param), 0)
        saida_1 = dt.date(data_int[0], data_int[1], data_int[2])
    except:
        saida_1 = dt.date(1900,1,1)
    return saida_1

errors = []

path = '/media/projeto_cemig/'

col = []
resultados = []

def cb(file):
    if file[-3:].lower() == 'xls':
        try:
            workbook = xlrd.open_workbook(file)
            sheet = workbook.sheet_by_index(0)
            data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
            if data[0][0] == 'Relatorio No:':
                resultados.append( (data, file ) )
        except:
            pass

class DirWalker(object):

    def walk(self,dir,meth):
        """ walks a directory, and executes a callback on each file """
        dir = os.path.abspath(dir)
        for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
            nfile = os.path.join(dir,file)
            meth(nfile)
            if os.path.isdir(nfile):
                self.walk(nfile,meth)

def run():

    dw = DirWalker()
    dw.walk(path, cb)

    metodos = {}
    unidades = []
    linhas = []
    saida = []

    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet("SAIDA")
    index = 0
    arq = "/media/projeto_cemig/01_SOFTWARE/procmedicao.xls"
    for planilha, arquivo in resultados:
        posVlr = - 1
        ponto = planilha[8][posVlr]
        data = planilha[9][posVlr]
        numrel = planilha[0][1]
        for item in planilha[10:]:
            metodo = item[0]
            if not metodo in metodos:
                metodos[metodo] = item[1]
            if not  item[1] in unidades:
                unidades.append(item[1])

            vlr = item[posVlr]
            numcol = 0
            dsc_metodo = u'{0}'.format(metodo)
            if dsc_metodo and   \
                dsc_metodo[:7] not in ['LEGENDA', '* VMP -'] and \
                dsc_metodo not in [u'Data Amostragem',u'Hora Amostragem',u'Ultima Chuva',u'Tempo'] and \
                ponto and \
                u'{0}'.format(vlr):
                arq_ = arquivo.decode('utf-8', 'ignore').replace('/','%')
                for elem in [numrel, Converte_Data(data), ponto,vlr,metodo, item[1],arq_ ]:
                    row = sheet1.row(index)
                    if type(elem) == type(""):
                        elem = u'{0}'.format(elem)
                    row.write(numcol, elem)
                    numcol += 1
                index +=1
    book.save(arq)


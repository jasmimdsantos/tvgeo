# -*- coding: utf-8 -*-
#!/usr/bin/env python

import xlrd
import datetime
import calendar
from dateutil import parser

def lerDataExcel(vlr):
    date = datetime.datetime(1899, 12, 30)
    get_ = datetime.timedelta(int(vlr))
    get_col2 = str(date + get_)[:10]
    d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
    return d.strftime('%d-%m-%Y')

def convert_excel_time(t, hour24=True):
    if t > 1:
        t = t%1
    seconds = round(t*86400)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hour24:
        if hours > 12:
            hours -= 12
            return "%d:%d:%d PM" % (hours, minutes, seconds)
        else:
            return "%d:%d:%d AM" % (hours, minutes, seconds)

    return "%d:%d:%d" % (hours, minutes, seconds)


def KelvinToCelcius(t):
    return t-273.15

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def xlsDate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    xldate = float('0' + str(xldate))
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
        )



class Struct(object):
    """Comment removed"""
    def __init__(self, data):
        for name, value in data.iteritems():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)): 
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


class ObjectView(object):
    def __init__(self, d):
        self.__dict__ = d

class PlanilhaExcel:

    def leituraPlanilha(self, param):

        base = {}

        book = xlrd.open_workbook(param['planilha'], formatting_info=True) 
        sheet = book.sheet_by_index(0)
        inicio = param['rowInic'] 
        rows, cols = sheet.nrows, sheet.ncols
   
        for row in range(inicio,rows):
            rg = {}

            for it in param['campos']:
                nomeCampo = it[0]
                col = it[2]


                vlr = sheet.cell(row, col).value

                if it[1] == 'N':
                    try:
                        valor =  float(vlr)
                    except:
                        valor = -99
                else:
                    valor =  u'{0}'.format(vlr).replace('.0','')

                rg[nomeCampo] = valor

            if str(param['key']).strip() == '':
                break

            chave = rg[ param['key']]
            base[chave] = rg

        return base



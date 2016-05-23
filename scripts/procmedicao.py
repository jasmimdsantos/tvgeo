# -*- coding: utf-8 -*-
#!/usr/bin/env python

import django
import datetime
import xlrd
import chardet
from param.models import Unidade, Param
from projetos.models import Medicao, PtoMonit, Projeto, Campanha
from toolbox.tools import ObjectView, xlsDate_as_datetime
from projetos.regras import getCampanha
from toolbox.maillib import Email
from operator import itemgetter
from django.utils import timezone
from xlwt import Workbook
import os
import time
from datetime import datetime as dt



PROCESSO_ANTIGO = True

PATH_ARQUIVO     = '/media/projeto_cemig/01_SOFTWARE/procmedicao.xls'
#PATH_ARQUIVO     = '/media/projeto_cemig/01_SOFTWARE/consolidado_bioagri.xls'
#PATH_ARQUIVO     = '/media/projeto_cemig/01_SOFTWARE/consolidado_sisagua.xls'
PATH_FERRAMENTA  = '/media/projeto_cemig/01_PROJETO SOFTWARE/converte.xls'


PATH_SAIDA  = '/media/projeto_cemig/01_SOFTWARE/'


ID_PROJETO       = 1
PARAMETRO_DATA   = 840
PARAMETRO_TURBIDEZ  = 708


class ProcMedicao:

    def __init__(self):
        self.result = []
        self.erros = []
        self.processados = 0
        self.pontoConv = {}
        self.paramConv = {}

        self.__converte(0) # Pontos
        self.__converte(1) # Parametros

        self.__procExcel()

        for item in  self.result:
            self.__processaItem(item)

        self.__planilha_erro()



    def __planilha_erro(self):

        workbook = Workbook()
        sheet = workbook.add_sheet('Sheet1')

        y = 1
        for item in self.erros:
            sheet.write(y, 0, u'{0}'.format(item['msg']) )
            sheet.write(y, 1, u'{0}'.format(item['valor']) )
            sheet.write(y, 2, u'{0}'.format(item['planilha']) )
            y +=1

        novodir = '{0}{1}/'.format(PATH_SAIDA, datetime.datetime.now() )
        os.makedirs(novodir)
        path_saida ='{0}{1}.xls'.format(novodir, 'Erros')
        workbook.save(path_saida)

        return path_saida


    def __adderro(self, msg, valor, planilha):

        erro = { 'msg'     : msg,     \
                 'valor'   : valor,   \
                 'planilha': planilha }

        #objerro = ObjectView(erro)
        self.erros.append(erro)

    def __procExcel(self):

        workbook = xlrd.open_workbook(PATH_ARQUIVO)
        sheet = workbook.sheet_by_index(0)
        for row in range(1, sheet.nrows):
            _laudo = sheet.cell(row,0).value
            _laudo = str(_laudo)
            _laudo = _laudo.replace('.0','')

            _data = xlsDate_as_datetime( sheet.cell(row,1).value, 0)

            _data = timezone.make_aware(_data, timezone.get_current_timezone())

            _ponto = sheet.cell(row,2).value
            _param = sheet.cell(row,4).value

            _caminho = ''
            try:
                _caminho =sheet.cell(row,6).value
            except:
                _caminho = ''

            if  '01_OUTROS MONITORAMENTOS' in  _caminho:
                continue

            try:
                _valor = sheet.cell(row,3).value
            except:
                continue

            registro = { 'controle' : _laudo.strip(),
                         'ponto' : _ponto.strip(),
                         'data'  : _data,
                         'chave' : _laudo.strip(),
                         'param' : _param.strip(),
                         'valor' : _valor,
                         'caminho' : _caminho.strip() }

            reg = ObjectView(registro)

            self.result.append(reg)


    def __converte(self, folha):

        workbook = xlrd.open_workbook(PATH_FERRAMENTA)
        sheet = workbook.sheet_by_index(folha)
        for row in range(1, sheet.nrows):
            _de   = sheet.cell(row,0).value
            _de   = _de.strip()

            _para = sheet.cell(row,1).value
            _para = u'{0}'.format(_para).strip()

            if folha == 0:
                self.pontoConv[_de] = _para
            else:
                self.paramConv[_de] = _para


    def __processaItem(self, item):

        """
        Parametro
        """
        if item.param in self.paramConv:
            item.param = self.paramConv[item.param].strip()

        if item.param == u'excluir' or item.param == u'EXCLUIR' or item.param == u'Excluir' :
            return False

        col = Param.objects.filter(nome = item.param)
        if len(col) == 0:
            self.__adderro(u'Parâmetro não existe',  item.param, item.caminho )
            return False
        else:
            objParametro = col[0]
        del col

        """
        Local
        """
        item.ponto  = item.ponto.replace(' ','').replace('-','').strip()

        old = item.ponto

        if item.ponto in self.pontoConv:
            item.ponto = self.pontoConv[item.ponto].strip()
            item.ponto  = item.ponto.replace(' ','').replace('-','').strip()

        if item.ponto == u'excluir' or item.ponto == u'EXCLUIR' or item.ponto == u'Excluir' :
            return False

        col = PtoMonit.objects.filter(sigla = item.ponto)
        if len(col) == 0:
            self.__adderro(u'Ponto de monitoramento não existe',
                            item.ponto,
                            item.caminho )
            return False
        else:
            objLocal = col[0]

        del col


        """
        Tratamento de valor
        """
        float_vlr = float(0)

        if type(item.valor) == type(float(0)):
            item.valor = u'{0}'.format(item.valor)

        _vl = item.valor.replace('<','').replace(',','.')
        try:
            float_vlr = float(_vl)
        except:
            float_vlr = 0


        """
        A data considerada é a data da planilha de dados em campoq
        Os dados da planilha só devem ser importados após os dados de campo
        """
        start_week = item.data - datetime.timedelta(item.data.weekday())
        end_week = start_week + datetime.timedelta(7)
        query = Medicao.objects.filter( PtoMonit_FK  = objLocal,
                                        Parametro_FK = PARAMETRO_DATA,
                                        data__range=[start_week, end_week]).values('data')
        if query:
            item.data =  query[0]['data']
            if len(query) > 1:
                self.__adderro(u'Foram encontrados mais de um parametro nesta faixa',
                    u'{0} {1}'.format(objLocal.sigla, item.data), item.caminho )
        else:
            if not PROCESSO_ANTIGO:
                self.__adderro(u'Não foi encontrado dados de campo para processar a planilha',
                        u'{0} {1}'.format(objLocal.sigla, item.data), item.caminho )
                return False

        """
        Medicao
        """
        col = Medicao.objects.filter( PtoMonit_FK  = objLocal,
                                      Parametro_FK = objParametro,
                                      data         = item.data)
        if len(col) > 0:
            reg = col[0]
            """ Se o controle for o mesmo é reprocessamento da informação"""
            if item.controle == reg.controle:
                return False

            """ Se o controle for diferente e o parametro for turbidez substitui pelo mais recente"""
            if objParametro.id == PARAMETRO_TURBIDEZ:
                reg.delete()
            else:
                """
                Controle diferente e não é turbiudez deve gerar erro
                """
                self.__adderro(u'Medição duplicada',
                                u'{0} {1} {2}'.format(objLocal.sigla, item.data, objParametro.nome), item.caminho )
                return False

        """
        Campanha
        """
        objCampanha = getCampanha(ID_PROJETO, item.data)

        registro = Medicao( Campanha_FK  = objCampanha,
                                PtoMonit_FK  = objLocal,
                                Parametro_FK = objParametro,
                                controle     = item.controle,
                                data         = item.data,
                                vlr          = float_vlr,
                                vlrLbl       = item.valor)
        registro.save()
        self.processados += 1

        return True



def run():
    print(dt.now())
    obj = ProcMedicao()
    print(dt.now())
    print('Fim')

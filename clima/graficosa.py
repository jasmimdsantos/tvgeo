
import psycopg2
from datetime import datetime, timedelta
import calendar


class GeraGraficos:

    def __init__(self):
        try:
            connstring = "host='10.3.0.26' dbname='clima' user='postgres' password='wilci5w7'"
            self.db  = psycopg2.connect(connstring)
        except:
             raise


    def defcategoria(self, _tipo, _data):

        if _tipo == 'D':
            faixa = [ int(dia) for dia in calendar.Calendar().itermonthdays(_data.year, _data.month) if dia >0]
        else:
            faixa = [ 'jan',  'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    
        faixa.insert(0,0)

        return faixa


    def defgrafico(self, _tipo):

        creditos =   {
                         'enabled': 'true',
                         'text'   : 'Fonte: INMET Powered by: Terravision'
                     }

        """
        Temperatura
        """
        sql = '' 
        if _tipo == 'temp_media_diaria':

            titulo = u'Temperatura Diária  (Máxima, Média, Mínima)'
            ytitle = 'Temperatura (°C)'
            campos = ['tempmed',  'tempmax',  'tempmin', ]
            tipo = 'line'
 
            sql = sql + 'SELECT "Data",                                 '
            sql = sql + 'avg("TempInst")     as tempmed, '
            sql = sql + 'avg("TempMax")      as tempmax, '
            sql = sql + 'avg("TempMin")      as tempmin  '

            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Temperatura Máxima'.encode('latin1'), 'color' : 'red', 'data' : [] }  ,
                        { 'name' : u'Temperatura Média'.encode('latin1') , 'color' : 'orange',    'data' : [] },  
                        { 'name' : u'Temperatura Mínima'.encode('latin1'), 'color' : 'blue',   'data' : [] }  
                      ]
        if _tipo == 'temp_media_mensal':
            titulo = u'Temperatura Mensal  (Máxima, Média, Mínima)'
            ytitle = 'Temperatura (°C)'
            campos = ['tempmed',  'tempmax',  'tempmin', ]
            tipo = 'line'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + 'avg("TempInst")     as tempmed, '
            sql = sql + 'avg("TempMax")      as tempmax, '
            sql = sql + 'avg("TempMin")      as tempmin  '

            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Temperatura Máxima'.encode('latin1'), 'color' : 'red', 'data' : [] }  ,
                        { 'name' : u'Temperatura Média'.encode('latin1') , 'color' : 'orange',    'data' : [] }  ,
                        { 'name' : u'Temperatura Mínima'.encode('latin1'), 'color' : 'blue',   'data' : [] }  
                      ]

        if _tipo == 'temp_absoluta_mensal':
            titulo = u'Temperatura Absoluta  Mensal  (Máxima Mínima)'
            ytitle = 'Temperatura (°C)'

            campos = ['tempmed',  'tempmin', ]
           
            tipo = 'line'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + 'max("TempMax")      as tempmax, '
            sql = sql + 'min("TempMin")      as tempmin  '

            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Temperatura Máxima'.encode('latin1'), 'color' : 'red', 'data' : [] }  ,
                        { 'name' : u'Temperatura Mínima'.encode('latin1'), 'color' : 'blue',   'data' : [] }  
                      ]




        """
        Umidade
        """
        if _tipo == 'umidade_media_diaria_inst':
            titulo = u'Umidade Diária Média'
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmed' ]
            tipo = 'column'
 
            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       avg( "UmidInst")     as umidmed '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Média'.encode('latin1') , 'color' : 'green',    'data' : [] }  ,
                      ]

        if _tipo == 'umidade_media_diaria_max':
            titulo = u'Umidade Diária Máxima'
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmax' ]
            tipo = 'column'
 
            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       avg( "UmidMax")     as umidimax '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Máxima'.encode('latin1') , 'color' : 'green',    'data' : [] }  ,
                      ]



        if _tipo == 'umidade_media_diaria_min':
            titulo = u'Umidade Diária Mínima '
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmin' ]
            tipo = 'column'
 
            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       avg( "UmidMin")      as umidmin '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Minima'.encode('latin1'), 'color' : 'green', 'data' : [] }  ,
                      ]



        if _tipo == 'umidade_media_mensal_inst':
            titulo = u'Umidade Mensal Média'
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmed' ]
            tipo = 'column'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       avg( "UmidInst")     as umidmed '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Média'.encode('latin1') , 'color' : 'green',    'data' : [] }  ,
                      ]

        if _tipo == 'umidade_media_mensal_max':
            titulo = u'Umidade Mensal Máxima'
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmax' ]
            tipo = 'column'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       avg( "UmidMax")     as umidimax '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Máxima'.encode('latin1') , 'color' : 'green',    'data' : [] }  ,
                      ]



        if _tipo == 'umidade_media_mensal_min':
            titulo = u'Umidade Mensal Mínima '
            ytitle = 'Umidade Relativa (%)'
            campos = ['umidmin' ]
            tipo = 'column'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       avg( "UmidMin")      as umidmin '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Umidade Minima'.encode('latin1'), 'color' : 'green', 'data' : [] }  ,
                      ]

        



        """
        Pressão
        """

        if _tipo == 'pressao_media_diaria':
            titulo = u'Pressão Média Diária'
            ytitle = 'Pressão (hpa)'
            campos = ['pressinst' ]
            tipo = 'line'
 
            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       avg( "PressInst")     as pressinst '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Pressão Média'.encode('latin1') , 'color' : 'blue',    'data' : [] }  ,
                      ]

        if _tipo == 'pressao_media_mensal':
            titulo = u'Pressão Média Mensal'
            ytitle = 'Pressão (hpa)'
            campos = ['pressinst' ]
            tipo = 'line'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       avg( "PressInst")     as pressinst '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Pressão Média'.encode('latin1') , 'color' : 'blue',    'data' : [] }  ,
                      ]




        """
        Vento
        """
        if _tipo == 'vento_media_diaria':
            titulo = u'Vento Diária'
            ytitle = 'Velocidade (m/s)'
            campos = ['vvelmed', 'vrajmax' ]
            tipo = 'line'

            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       avg("VentVel")      as vvelmed, '
            sql = sql + '       max("VentRaj")      as vrajmax '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Velocidade Média'.encode('latin1') , 'color' : 'cyan',    'data' : [] }  ,
                        { 'name' : u'Rajada Máxima'.encode('latin1')    , 'color' : 'blue',    'data' : [] }  ,
                      ]

        if _tipo == 'vento_media_mensal':
            titulo = u'Vento Mensal'
            ytitle = 'Velocidade (m/s)'
            campos = ['vvelmed', 'vrajmax' ]
            tipo = 'line'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       avg("VentVel")      as vvelmed, '
            sql = sql + '       max("VentRaj")      as vrajmax '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Velocidade Média'.encode('latin1') , 'color' : 'cyan',    'data' : [] }  ,
                        { 'name' : u'Rajada Máxima'.encode('latin1')    , 'color' : 'blue',    'data' : [] }  ,
                      ]






        """
        Radiação
        """
        if _tipo == 'radiacao_diaria':
            titulo = u'Radiação Diária'
            ytitle = 'horas'
            campos = ['radiacao' ]
            tipo = 'column'

            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       sum( CASE WHEN "Radiacao"  > 100 THEN 1 ELSE 0  END) as radiacao    '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Radiação Solar'.encode('latin1')    , 'color' : 'yellow',    'data' : [] }  ,
                      ]

        if _tipo  == 'radiacao_mensal':
            titulo = u'Radiação Mensal'
            ytitle = 'total de horas mensal'
            campos = ['radiacao' ]
            tipo = 'column'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       sum( CASE WHEN "Radiacao"  > 100 THEN 1 ELSE 0  END) as radiacao    '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Radiação Solar'.encode('latin1')    , 'color' : 'yellow',    'data' : [] }  ,
                      ]





        """
        Precipitação
        """

        if _tipo in ['precipitacao_diaria']:
            titulo = u'Precipitação Diária'
            ytitle = 'mm'
            campos = ['chuva' ]
            tipo = 'column'

            sql = sql + 'SELECT "Data",  '  
            sql = sql + '       sum("Chuva") as chuva  '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Precipitação'.encode('latin1')    , 'color' : 'blue',    'data' : [] }  ,
                      ]

        if _tipo == 'precipitacao_mensal':
            titulo = u'Precipitação Mensal'
            ytitle = 'mm'
            campos = ['chuva' ]
            tipo = 'column'
 
            sql = sql + 'SELECT date_trunc(\'month\', "Data") as data,  '  
            sql = sql + '       sum("Chuva") as  chuva    '
 
            group =   'GROUP BY "Data"' 

            series =  [ 
                        { 'name' : u'Precipitação'.encode('latin1')    , 'color' : 'blue',    'data' : [] }  ,
                      ]



        return {    'titulo'    : titulo,
                    'ytitle'    : ytitle, 
                    'campos'    : campos, 
                    'sql'       : sql, 
                    'group'     : group, 
                    'series'    : series, 
                    'type'      : tipo,
                    'creditos'  : creditos }


    def processa(self, _codestac,  _data, _nome,  _tipo, _nomeestac):

        categoria   = self.defcategoria(_tipo, _data ) 
        defgrafico  = self.defgrafico(_nome)


        if _tipo == 'D':
            subtitulo = u'{0}  -  {1}/{2}'.format(_nomeestac, _data.month, _data.year)
            lastcategoria =  categoria[-1:][0]
            dataini = datetime(_data.year, _data.month, 1)
            datafim = datetime(_data.year, _data.month, lastcategoria)
        else:
            subtitulo = u'{0}  -  {1}'.format(_nomeestac, _data.year)
            dataini = datetime(_data.year, 1, 1)
            datafim = datetime(_data.year, 12, 31)
 
        data       = [ [ 0 for  dia in categoria ]for i in defgrafico['series'] ]

        sql = ''
        sql = sql + defgrafico['sql']
        sql = sql + '       FROM "Clima_dadosestacao" d           '
        sql = sql + '              LEFT JOIN "Clima_estacoes" e ON d."codEstac" = e.codigo  '
        sql = sql + '       WHERE e.omm  = %s AND                                           '
        sql = sql + '             d."Data" BETWEEN %s AND %s                                '
        sql = sql + defgrafico['group']
        sql = sql + ';'
        

        try:
            cursor = self.db.cursor()
            dados = ( _codestac, dataini, datafim )
            cursor.execute(sql, dados)
            for item in  cursor.fetchall():
                indice = 0
                dia = item[0].day if _tipo  == 'D' else  item[0].month 
                for cpo in defgrafico['campos']:
                    data[indice][dia] = round( item[indice+1], 2)
                    indice += 1
        except:
            raise
    

        indice = 0 
        for item in defgrafico['series']:
            defgrafico['series'][indice]['data'] = data[indice][1:]           
            indice += 1
 
        grafico = { 
                    'type':         defgrafico['type'], 
                    'titulo':       defgrafico['titulo'],
                    'subtitulo':    subtitulo,
                    'categories':   categoria[1:],
                    'ytitle':       defgrafico['ytitle'] ,
                    'creditos' :    defgrafico['creditos'], 
                    'series':       defgrafico['series']
                  }
        
        return grafico



    def procRsVentos(self, _codestac,  _data, item, _tipo, _nomeestac):

        creditos =   {
                         'enabled': 'true',
                         'text'   : 'Fonte: INMET Powered by: Terravision'
                     }

        sql = 'SELECT '
        if _tipo == 'A':
            titulo = u'Direção Predominante do vendo (%)' 
            subtitulo = u'{0}  -  {1}'.format(_nomeestac, _data.year)
            dataini = datetime(_data.year, 1, 1)
            datafim = datetime(_data.year, 12, 31)
        else: 
            categoria   = self.defcategoria(_tipo, _data ) 
            titulo = u'Rosa dos Ventos Diaria'
            subtitulo = u'{0}  -  {1}/{2}'.format(_nomeestac, _data.month, _data.year)
            lastcategoria =  categoria[-1:][0]

            dataini = datetime(_data.year, _data.month, 1)
            datafim = datetime(_data.year, _data.month, lastcategoria)
     
 
        sql = sql + '       sum( CASE WHEN "VentDir"  > 340  or "VentDir" <  21 THEN 1 ELSE 0 END ) as N,    '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 22  and "VentDir" <  69 THEN 1 ELSE 0 END) as NE,   '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 70  and "VentDir" < 114 THEN 1 ELSE 0 END) as E,    '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 115 and "VentDir" < 159 THEN 1 ELSE 0 END) as SE,   '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 160 and "VentDir" < 203 THEN 1 ELSE 0 END) as S,    '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 204 and "VentDir" < 248 THEN 1 ELSE 0 END) as SW,   '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 249 and "VentDir" < 293 THEN 1 ELSE 0 END) as W,    '
        sql = sql + '       sum( CASE WHEN "VentDir"  > 294 and "VentDir" < 339 THEN 1 ELSE 0 END) as NW,   '
        sql = sql + '       sum( 1) as total   '
        sql = sql + '       FROM "Clima_dadosestacao" d           '
        sql = sql + '              LEFT JOIN "Clima_estacoes" e ON d."codEstac" = e.codigo  '
        sql = sql + '       WHERE e.omm  = %s AND                                           '
        sql = sql + '             d."Data" BETWEEN %s AND %s                                '
        sql = sql + ';'
         
        try:
            cursor = self.db.cursor()
            dados = ( _codestac, dataini, datafim )
            cursor.execute(sql, dados)
            data = []
            for item in  cursor.fetchall():
                total = float(item[8])
                indice = 0
                for cpo in range(7):
                    vlr = (float(item[indice])/total)*100
                    vlr = round(vlr,2)
                    data.append(vlr)
                    indice += 1
        except:
            raise
 
        series =  [
	              	{   'type'  : 'area',
                        'name'  : '%', 
                        'data'  : data 
                    }  
                  ]


        grafico = { 
                    'type':         'rosa', 
                    'titulo':       titulo,
                    'subtitulo':    _nomeestac,
                    'creditos' :    creditos, 
                    'series':       series
                  }
 
        return grafico

    def pool(self, _codstac, _data, _tipo, _nomeestac):
        
        if _tipo == 'D':
            col =  ['temp_media_diaria',        
                    'umidade_media_diaria_inst',
                    'umidade_media_diaria_min', 
                    'pressao_media_diaria',     
                    'vento_media_diaria',       
                    'radiacao_diaria',          
                    'precipitacao_diaria',
                    'umidade_media_diaria_max'
                   ]
        else:
            col =  ['temp_media_mensal',          'temp_absoluta_mensal', 
                    'umidade_media_mensal_inst',  'umidade_media_mensal_max',
                    'umidade_media_mensal_min',   'pressao_media_mensal', 
                    'vento_media_mensal',         'radiacao_mensal',      
                    'precipitacao_mensal']

        retorno = []
        indice = 0
        for item in col:
            result = self.processa( _codstac,  _data, item, _tipo, _nomeestac) 
            result['id'] = indice
            retorno.append(result)
        indice += 1

        result = self.procRsVentos( _codstac,  _data, '', _tipo, _nomeestac) 
        retorno.append(result)
        self.db.close()
        return retorno





import psycopg2
from datetime import datetime, timedelta
import time

class Estacao:

    class Registro:

        def __init__(self, rec):
            self.codigo = rec[1]
            self.nome   = rec[2]
            self.altitude = rec[3]
            self.ponto    = rec[4]
            self.abertura = rec[5]
            self.omm      = rec[6]


    def __init__(self):
        try:
            connstring = "host='10.3.0.26' dbname='Clima' user='postgres' password='wilci5w7'"
            self.db  = psycopg2.connect(connstring)
        except:
             raise


    def getDados(self):
        colec = []
        try:
            cursor = self.db.cursor()
            sql = 'SELECT * FROM "Clima_estacoes" ORDER BY sigla;'
            cursor.execute(sql)
            for record in cursor.fetchall():
                colec.append(self.Registro(record))
        except:
            raise

        return colec

    def getDados(self, codigo):

        saida = ''
        try:
            cursor = self.db.cursor()
            sql = 'SELECT codigo FROM "Clima_estacoes" WHERE omm = \'{0}\';'.format(codigo)
            cursor.execute(sql)
            saida = cursor.fetchone()
        except:
            raise

        return saida



    def __del(self):
        self.db.close()



class Medicao:


    class RosaVentos:

        class ItemRosaVentos:
            def __init__(self, _direcao, _fxInicial, _fxFinal ):
                self.direcao = _direcao
                self.fxInicial = _fxInicial
                self.fxFinal = _fxFinal
                self.qtd = 0
                self.pct = 0

        def __init__(self):
            self.qtdtotal = 0
            self.itens = []
            self.itens.append( self.ItemRosaVentos('N',  0,    21) )
            self.itens.append( self.ItemRosaVentos('N', 340,  360) )
            self.itens.append( self.ItemRosaVentos('NE', 22,   69) )
            self.itens.append( self.ItemRosaVentos('E',  70,  114) )
            self.itens.append( self.ItemRosaVentos('SE',115,  159) )
            self.itens.append( self.ItemRosaVentos('S', 160,  203) )
            self.itens.append( self.ItemRosaVentos('SW',204,  248) )
            self.itens.append( self.ItemRosaVentos('W', 249,  293) )
            self.itens.append( self.ItemRosaVentos('NW',294,  339) )


        def total(self):
            indice = 0
            resultado = {}
            for item in self.itens:
                item.pct = float(item.qtd) / float(self.qtdtotal)
                self.itens[indice] = item
                indice +=1
                if item.direcao in resultado:
                    valor = resultado[item.direcao]
                else:
                    valor = 0
                resultado[item.direcao] = valor + item.pct

            return [    resultado['N'],
                        resultado['NE'],
                        resultado['E'],
                        resultado['SE'],
                        resultado['S'],
                        resultado['SW'],
                        resultado['W'],
                        resultado['NW']
                   ]


        def acumula(self, _graus):
            achou = False
            indice = 0
            for item in self.itens:
                if _graus >= item.fxInicial and _graus <= item.fxFinal:
                    achou = True
                    break
                else:
                    indice +=1

            if achou :
                obj = self.itens[indice]
                obj.qtd += 1
                self.itens[indice] = obj
                self.qtdtotal += 1



    class MaxMin:
        def __init__(self, _max, _min, _inst):
            self.vlrmax = _max
            self.vlrmin = _min
            self.vlrinst = _inst

    class Vent:
        def __init__(self, _vel, _dir, _raj):
            self.vlrvel = _vel
            self.vlrdir = _dir
            self.vlrraj = _raj

    class Registro(Vent, MaxMin):
        def __init__(self, rec):
            self.estac   = rec[2]
            self.data    = rec[3]
            self.hora    = rec[4]
            self.temp    = Medicao.MaxMin(rec[5], rec[6], rec[7])
            self.umidade = Medicao.MaxMin(rec[8], rec[9], rec[10])
            self.orvalho = Medicao.MaxMin(rec[11], rec[12], rec[13])
            self.pressao = Medicao.MaxMin(rec[14], rec[15], rec[16])
            self.vento   = Medicao.Vent(rec[17], rec[18], rec[19])
            self.radiac  = rec[20]
            self.Precipt = rec[21]


    def __init__(self):
        try:
            connstring = "host='10.3.0.26' dbname='clima' user='postgres' password='wilci5w7'"
            self.db  = psycopg2.connect(connstring)
        except:
            raise

    def getRosaVentos(self, codEstac):

        obj = self.RosaVentos()
        for rec in self.getDados(codEstac):
            obj.acumula(rec.vento.vlrdir)
        return obj.total()


    def getDados(self, _chave):
        colec = []
        try:
            cursor = self.db.cursor()
            sql = 'SELECT * FROM "Clima_dadosestacao" WHERE chave LIKE %s ;'
            dados = (_chave, )
            cursor.execute(sql, dados)
            for record in cursor.fetchall():
                colec.append(self.Registro(record))
        except:
            raise

        return colec

    def getMedicaoHoraria(self, codEstac, _datainic = datetime(1900,1,1),  _datafim = datetime(2099,12,31)):


        datainic = _datainic if _datainic else datetime(1900,1,1)
        datafim  = _datafim  if _datafim  else datetime.today()

        d = datainic - timedelta(days=-1)


        campos = [  'data',     'hora',
                    'tempmed',  'tempmax',  'tempmin',
                    'umidmed',  'umidmax',  'umidmin',
                    'pomed',    'pomax',    'pominin',
                    'pmed',     'pmaax',    'pmin',
                    'vvelmed',  'vrajmax',
                    'radiacao', 'vdirmed',
                    'chuva',  # 'datachuva',
                    'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW',
                    'vtot']


        colec = []

        sql = ''
        sql = sql + 'SELECT "Data"         as data,    '
        sql = sql + '       "Hora"         as hora, '
        sql = sql + '       "TempInst"     as tempmed, '
        sql = sql + '       "TempMax"      as tempmax, '
        sql = sql + '       "TempMin"      as tempmin, '
        sql = sql + '       "UmidInst"     as umidmed, '
        sql = sql + '       "UmidMax"      as umidmax, '
        sql = sql + '       "UmidMin"      as umidmin, '
        sql = sql + '       "PtoOrvInst"   as pomed,   '
        sql = sql + '       "PtoOrvMax"    as pomax,   '
        sql = sql + '       "PtoOrvMin"    as pomin,   '
        sql = sql + '       "PressInst"    as pmed,    '
        sql = sql + '       "PressMax"     as pmax,    '
        sql = sql + '       "PressMin"     as pmin,    '
        sql = sql + '       "VentVel"      as vvelmed, '
        sql = sql + '       "VentRaj"      as vrajmax, '
        sql = sql + '       "Radiacao"     as radiacao,'
        sql = sql + '       "VentDir"      as vdirmed, '
        sql = sql + '       "Chuva"        as chuva, '
#       sql = sql + '       "Data"         as datachuva,  '
        sql = sql + '       CASE WHEN "VentDir"  > 340  or "VentDir" <  21 THEN 1 ELSE NULL END as N,    '
        sql = sql + '       CASE WHEN "VentDir"  > 22  and "VentDir" <  69 THEN 1 ELSE NULL END as NE,   '
        sql = sql + '       CASE WHEN "VentDir"  > 70  and "VentDir" < 114 THEN 1 ELSE NULL END as E,    '
        sql = sql + '       CASE WHEN "VentDir"  > 115 and "VentDir" < 159 THEN 1 ELSE NULL END as SE,   '
        sql = sql + '       CASE WHEN "VentDir"  > 160 and "VentDir" < 203 THEN 1 ELSE NULL END as S,    '
        sql = sql + '       CASE WHEN "VentDir"  > 204 and "VentDir" < 248 THEN 1 ELSE NULL END as SW,   '
        sql = sql + '       CASE WHEN "VentDir"  > 249 and "VentDir" < 293 THEN 1 ELSE NULL END as W,    '
        sql = sql + '       CASE WHEN "VentDir"  > 294 and "VentDir" < 339 THEN 1 ELSE NULL END as NW,   '
        sql = sql + '       1                                                                   as vtot  '
        sql = sql + '       FROM "Clima_dadosestacao" d           '
        sql = sql + '              LEFT JOIN "Clima_estacoes" e ON d."codEstac" = e.codigo  '
        sql = sql + '       WHERE e.omm  = %s                                            '
#       sql = sql + '             d."Data" BETWEEN %s AND %s                                '
        sql = sql + '       ORDER BY "Data", "Hora";                                        '


        saida = []
        try:
            cursor = self.db.cursor()
            dados = ( codEstac,  )
            cursor.execute(sql, dados)
            for item in  cursor.fetchall():
                reg = {}
                indice = 0
                for cpo in campos:
                    reg[cpo] = item[indice]
                    indice += 1
                saida.append(reg)
        except:
            raise

        return saida




    def getMedicaoDiaria(self, codEstac, _datainic = datetime(2016,1,1), _datafim = datetime(2099,12,31)):


        datainic = _datainic if _datainic else datetime(1900,1,1)
        datafim  = _datafim  if _datafim  else datetime.today()

        campos = [  'data',
                    'tempmed',  'tempmax',  'tempmin',
                    'umidmed',  'umidmax',  'umidmin',
                    'pomed',    'pomax',    'pominin',
                    'pmed',     'pmaax',    'pmin',
                    'vvelmed',  'vrajmax',
                    'radiacao', 'vdirmed',
                    'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW',
                    'vtot']


        colec = []

        sql = ''
        sql = sql + 'SELECT "Data"              as data,    '
        sql = sql + '       avg("TempInst")     as tempmed, '
        sql = sql + '       max("TempMax")      as tempmax, '
        sql = sql + '       min("TempMin")      as tempmin, '
        sql = sql + '       avg("UmidInst")     as umidmed, '
        sql = sql + '       max("UmidMax")      as umidmax, '
        sql = sql + '       min("UmidMin")      as umidmin, '
        sql = sql + '       avg("PtoOrvInst")   as pomed,   '
        sql = sql + '       max("PtoOrvMax")    as pomax,   '
        sql = sql + '       min("PtoOrvMin")    as pomin,   '
        sql = sql + '       avg("PressInst")    as pmed,    '
        sql = sql + '       max("PressMax")     as pmax,    '
        sql = sql + '       min("PressMin")     as pmin,    '
        sql = sql + '       avg("VentVel")      as vvelmed, '
        sql = sql + '       max("VentRaj")      as vrajmax, '
        sql = sql + '       sum("Radiacao")     as radiacao,'
        sql = sql + '       avg("VentDir")      as vdirmed, '
        sql = sql + '       count( CASE WHEN "VentDir"  > 340  or "VentDir" <  21 THEN 1 ELSE NULL END) as N,    '
        sql = sql + '       count( CASE WHEN "VentDir"  > 22  and "VentDir" <  69 THEN 1 ELSE NULL END) as NE,   '
        sql = sql + '       count( CASE WHEN "VentDir"  > 70  and "VentDir" < 114 THEN 1 ELSE NULL END) as E,    '
        sql = sql + '       count( CASE WHEN "VentDir"  > 115 and "VentDir" < 159 THEN 1 ELSE NULL END) as SE,   '
        sql = sql + '       count( CASE WHEN "VentDir"  > 160 and "VentDir" < 203 THEN 1 ELSE NULL END) as S,    '
        sql = sql + '       count( CASE WHEN "VentDir"  > 204 and "VentDir" < 248 THEN 1 ELSE NULL END) as SW,   '
        sql = sql + '       count( CASE WHEN "VentDir"  > 249 and "VentDir" < 293 THEN 1 ELSE NULL END) as W,    '
        sql = sql + '       count( CASE WHEN "VentDir"  > 294 and "VentDir" < 339 THEN 1 ELSE NULL END) as NW,   '
        sql = sql + '       count(*)            as vtot  '
        sql = sql + '       FROM "Clima_dadosestacao" d           '
        sql = sql + '              LEFT JOIN "Clima_estacoes" e ON d."codEstac" = e.codigo '
        sql = sql + '       WHERE e.omm  = %s AND"                                          '
        sql = sql + '             d."Data" BETWEEN %s AND %s                                '
        sql = sql + '       GROUP BY "Data"'
        sql = sql + '       ORDER BY "Data";'


        saida = []
        try:
            cursor = self.db.cursor()
            dados = ( codEstac, )
            cursor.execute(sql, dados)
            for item in  cursor.fetchall():
                reg = {}
                indice = 0
                for cpo in campos:
                    reg[cpo] = item[indice]
                    indice += 1
                saida.append(reg)
        except:
            raise
        return saida


    def graficos(self, codEstac):

        dados_temp = []
        dados_umi =  []
        dados_po =   []
        dados_pres = []
        dados_rad =  []
        dados_pre =  []
        dados_vdd =  []
        dados_vvel = []

        objDados = self.getMedicaoHoraria(codEstac)
        for item in objDados:
            dt1  = item['data']

            hora = datetime(dt1.year, dt1.month, dt1.day, int( item['hora']), 0, 0, 0)

            dt  = int(time.mktime(hora.timetuple()))
            dt += (hora.microsecond / 1000000.0)
            dt *= 1000

            dados_temp.append(    [ dt, item['tempmed'] ])
            dados_umi.append(     [ dt, item['umidmed']])
            dados_po.append(      [ dt, item['pomed'] ])
            dados_pres.append(    [ dt, item['pmed']  ])
            dados_rad.append(     [ dt, item['radiacao']])
            dados_pre.append(     [ dt, item['chuva'] ] )
            dados_vdd.append(     [ dt, item['vdirmed']])
            dados_vvel.append(    [ dt, item['vvelmed']])

    	saida = {
    		'dados_temp' :  dados_temp,
    		'dados_umi'  :  dados_umi,
    		'dados_po'   :  dados_po,
    		'dados_pres' :  dados_pres,
    		'dados_rad'  :  dados_rad,
    		'dados_pre'  :  dados_pre,
    		'dados_vdd'  :  dados_vdd,
    		'dados_vvel' :  dados_vvel
    		}

	return saida



    def __del(self):
        self.db.close()

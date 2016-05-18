
from django.contrib.gis.geos import GEOSGeometry
from  clima.models import Station
import psycopg2

def automatica_proxima(ponto, _tipo):
    colStation = Station.objects.filter(tipo=_tipo).distance(ponto).order_by('distance')
    return colStation[0]

def get_ibge(p1, p2):

    try:
            conn = psycopg2.connect("dbname='geonode_data' user='postgres' host='10.2.8.85' password='wilci5w7'")
    except:
            print("I am unable to connect to the database")

    query = """SELECT "CD_GEOCODM", "NM_MUNICIP", "UF" FROM municipios WHERE ST_CONTAINS(the_geom, ST_GeometryFromText('POINT({0} {1})' )) = true;"""
    sql = query.format(p2,p1)

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    if rows:
        reg = rows[0]
        cidade = { "ibge": reg[0],  "nome": reg[1] + ' - ' + reg[2] }
    else:
        cidade = { "ibge": '' ,  "nome": '' }
    return cidade


def processa(p1,p2):

    cidade = get_ibge(p1, p2)

    str_ponto = 'POINT({0} {1})'.format(p2,p1)
    pt = GEOSGeometry(str_ponto)
    pt.srid = 4326

    normal = automatica_proxima(pt, 'N')
    automatica = automatica_proxima(pt, 'A')

    result = { 'normal' : { 'estacao' : normal.Nome,
                            'dist' : str(round(normal.distance.km,2)),
                            'id' : str(normal.id)
                          } ,
               'automatica' : { 'estacao' : automatica.Nome,
                                'dist' : str(round(automatica.distance.km,2)),
                                'id' : str(automatica.id),
                                'codigo' : automatica.Codigo
                               },
               'cidade' : cidade,
            }
    return result

def run():

    p1 = -19.96964
    p2 = -44.08796
    value = processa(p1, p2)
    print(value)



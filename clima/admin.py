# Register your models here.

from django.contrib.gis import admin


from .models import Station, Parametro, Resultado, Classe

class StationAdmin(admin.ModelAdmin):
    list_filter = ('Codigo','Nome', 'Estado', 'UF', 'Altitude', 'LatLong',)
    list_display = ['Codigo','Nome', 'Estado', 'UF', 'Altitude', 'LatLong',]
    fieldsets = [
                    (None, {'fields': ['Codigo','Nome', 'Estado',\
                    'UF', 'Altitude', 'LatLong', ]}),
                ]
class ParametroAdmin(admin.ModelAdmin):

    list_filter = ('Nome','Classe_FK', 'unidade', )
    list_display = ['Nome','Classe_FK', 'unidade',  'codigo',  ]
    fieldsets = [
                    (None, {'fields': ['Nome','Classe_FK',\
                        'unidade', 'corGrafico', 'codigo' ]  })
                ]

class ResultAdmin(admin.ModelAdmin):
    list_filter = ('Station_FK','Parametro_FK',  )
    list_display = ['Station_FK', 'Parametro_FK',  ]
    fieldsets = [
                    (None, {'fields': ['Station_FK', 'Parametro_FK',\
                                            'jan', 'fev', 'mar',\
                                            'abr', 'mai', 'jun',\
                                            'jul', 'ago', 'stb', 'out',\
                                            'nov', 'dez', 'tot', ]  })
                ]

admin.site.register(Station, StationAdmin)
admin.site.register(Parametro, ParametroAdmin)
admin.site.register(Resultado, ResultAdmin)
admin.site.register(Classe)



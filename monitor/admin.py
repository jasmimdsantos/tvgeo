from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Unidade, Param
# Register your models here.

from .models import Projeto, Layer
from .models import PtoMonit, Medicao
from .models import Midia, Texto
from .models import Relatorio
from .models import Campanha


class RelatorioDetailInline(admin.TabularInline):
    model = Relatorio
    fields =  ['Parametro_FK', 'descricao', 'data',  ]
    show_change_link = True
    extra = 0

class ProjetoAdmin(admin.ModelAdmin):
    list_filter = ('codigo', 'nome')

    list_display = ('codigo', 'nome', )

    inlines = [RelatorioDetailInline, ]

class LayerAdmin(admin.ModelAdmin):
    list_filter = ('Projeto_FK__nome', 'nome')

    list_display = ('nome', 'Projeto_FK',  'url' )

class CampanhaAdmin(admin.ModelAdmin):
    list_filter = ('Projeto_FK__nome', 'nome', 'mes', 'ano',)

    list_display = ('nome', 'Projeto_FK', 'mes', 'ano', )

class PtoMonitAdmin(DjangoMpttAdmin):
    list_filter = ('Projeto_FK__nome',  'ObjectID', )

    list_display = ('Projeto_FK', 'nome', 'ObjectID',  )


class MidiaDetailInline(admin.TabularInline):
    model = Midia
    fields =  ['nome', 'url',  'data', 'docfile', ]
    show_change_link = True
    extra = 0

class TextoDetailInline(admin.TabularInline):
    model = Texto
    fields =  ['descricao', 'data',  ]
    show_change_link = True
    extra = 0

class MedicaoAdmin(admin.ModelAdmin):
    list_filter = ('Campanha_FK__Projeto_FK__nome', 'Campanha_FK__nome', 'Parametro_FK__nome', 'PtoMonit_FK__sigla',   )

    list_display = ('Campanha_FK', 'PtoMonit_FK', 'Parametro_FK', 'data', 'vlr',   )

    inlines = [MidiaDetailInline, TextoDetailInline,]

class ParamAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Campanha, CampanhaAdmin)
admin.site.register(PtoMonit,PtoMonitAdmin)
admin.site.register(Medicao, MedicaoAdmin)
admin.site.register(Unidade)
admin.site.register(Param, ParamAdmin)

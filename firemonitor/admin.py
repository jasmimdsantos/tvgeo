from django.contrib import admin
from .models import Projeto, Camada, Equipe,KPI, KPI_Nivel


# Register your models here.
class EquipeDetailInline(admin.TabularInline):        
    model = Equipe
    fields = ['nome','email', 'foneFixo', 'foneCel', ]    
    show_change_link = True           
    extra = 0

class KPI_NivelDetailInline(admin.TabularInline):        
    model = KPI_Nivel
    fields = ['texto','cor', 'v1', 'v2', ]    
    show_change_link = True           
    extra = 0


class CamadaDetailInline(admin.TabularInline):        
    model = Camada
    fields = ['nome','url', 'isExtent', ]    
    show_change_link = True           
    extra = 0


class ProjetoAdmin(admin.ModelAdmin):
    list_filter = ('codigo', 'nome', 'wmo_normais', 'wmo_automatica',)

    list_display = ('codigo', 'nome', 'wmo_normais', 'wmo_automatica',)
	
    inlines = [EquipeDetailInline, CamadaDetailInline, ]


class KPIAdmin(admin.ModelAdmin):
    list_filter = ( 'nome', 'unidade', 'ordem',)

    list_display = ('nome','ordem',  'unidade', 'icone', 'msg',)
	
    inlines = [KPI_NivelDetailInline, ]


admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(KPI, KPIAdmin)



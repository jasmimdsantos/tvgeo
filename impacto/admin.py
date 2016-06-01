from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import (Empresa, Meio, TipoArea, Projeto,
                     Status_Projeto, Pessoa, Impacto,
                    Quadro, QuadroItem, Questao, QuestaoItem,
                     Questionario, FaseProjeto)

class QuestaoItemDetailInline(admin.TabularInline):
    model = QuestaoItem
    fields =  ['descricao', ]
    show_change_link = True
    extra = 0

class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields': ['questionario_FK','descricao', 'tipo', ]}),
                ]
    inlines = [ QuestaoItemDetailInline, ]




class QuadroItemDetailInline(admin.TabularInline):
    model = QuadroItem
    fields =  ['classe', 'descricao', ]
    show_change_link = True
    extra = 0

class QuadroAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields': ['ordem','descricao', ]}),
                ]
    inlines = [ QuadroItemDetailInline, ]


admin.site.register(Questionario)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Quadro, QuadroAdmin)
admin.site.register(Meio)
admin.site.register(TipoArea)
admin.site.register(Status_Projeto)
admin.site.register(Pessoa)
admin.site.register(Projeto)
admin.site.register(FaseProjeto)
admin.site.register(Impacto)
admin.site.register(Empresa)
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from paintstore.fields import ColorPickerField
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime
from django.utils import timezone



class Unidade(models.Model):

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['descricao',]

    sigla     = models.CharField(max_length=20)
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return u'{0}'.format(self.sigla)


class Param(MPTTModel):

    class Meta:
        verbose_name = u'Parâmetro'
        verbose_name_plural = u'Parâmetros'
        ordering = ['nome',]

    TipoParam  = ( ('0','valor'),
                   ('1','texto'),
                   ('2','imagem'),
                   ('3','classe'),
                   ('4','calculado'),
              )

    MONITORADO  = ( ('0','NAO'),
                    ('1','SIM'),
              )


    nome            = models.CharField(max_length=300, unique=True, verbose_name='Parametro')
    unidade_FK      = models.ForeignKey(Unidade, verbose_name='Unidade')
    monitorado      = models.CharField(max_length=1, choices=MONITORADO)
    vlrTeto         = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    vlrPiso         = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    decimais        = models.IntegerField(default=0)
    intervalo       = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    tipoParametro   = models.CharField(max_length=1, choices=TipoParam)
    parent          = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    created         = models.DateTimeField(auto_now_add=True)
    texto           = models.TextField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['nome']

    def __str__(self):
        return u'{0}'.format(self.nome)


class Legislacao(models.Model):

    class Meta:
        verbose_name = u'Legislação'
        verbose_name_plural = u'Legislação'

    descricao = models.CharField(max_length=50)

    def __str__(self):
        return u'{0}'.format(self.descricao)

class Classe(models.Model):

    class Meta:
        verbose_name = u'Classe VMP'
        verbose_name_plural = u'Classe VMP'

    descricao = models.CharField(max_length=50)

    def __str__(self):
        return u'{0}'.format(self.descricao)

class Limites(models.Model):
    class Meta:
        verbose_name = u'Limites'
        verbose_name_plural = u'Limites'

    parametro_FK  = models.ForeignKey(Param, verbose_name='Parametro')
    legislacao_FK = models.ForeignKey(Legislacao, verbose_name=u'Legislacão')
    classe_FK  = models.ForeignKey(Classe, verbose_name=u'Classe')
    vlr_max  = models.DecimalField(default=0, decimal_places=4, max_digits=16)
    vlr_min  = models.DecimalField(default=0, decimal_places=4, max_digits=16)


class Projeto(models.Model):

    codigo = models.CharField(max_length=6)
    nome = models.CharField(max_length=100, verbose_name='Projeto')

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['nome',]

    def __str__(self):
        return u'{0}'.format(self.nome)


class Layer(models.Model):

    Projeto_FK  = models.ForeignKey(Projeto, verbose_name="Projeto" )
    nome        = models.CharField(max_length=100, verbose_name='Layer')
    url         = models.URLField(max_length=300, verbose_name='URL Layer'),

    class Meta:
        verbose_name = 'Camada'
        verbose_name_plural = 'Camadas'
        ordering = ['nome',]

    def __str__(self):
        return u'{0}'.format(self.nome)



class PtoMonit(MPTTModel):

    Projeto_FK  = models.ForeignKey(Projeto, verbose_name="Projeto" )
    Layer_FK    = models.ForeignKey(Layer, verbose_name="Layer" )
    sigla       = models.CharField(max_length=15, default='', verbose_name='Codigo do Ponto.', unique=True, db_index=True)
    nome        = models.CharField(max_length=2200, default='', verbose_name='Pto.Monit.')
    ObjectID    = models.IntegerField(default=0)
    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    created     = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['sigla']
        verbose_name = 'Ponto de Monitoramento'
        verbose_name_plural = 'Pontos de Monitoramento'
        ordering = ['sigla',]

    def __str__(self):
        return u'{0}-{1}'.format(self.sigla, self.nome)


class Campanha(models.Model):

    Projeto_FK  = models.ForeignKey(Projeto, verbose_name="Projeto" )
    nome        = models.CharField(max_length=100,  verbose_name='Campanha')
    mes         = models.IntegerField(default=0)
    ano         = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Campanha'
        verbose_name_plural = 'Campanhas'
        ordering = ['ano','mes',]

    def __str__(self):
        return u'{0}'.format(self.nome)


class Medicao(models.Model):

    Campanha_FK = models.ForeignKey(Campanha, verbose_name="Campanha" )
    PtoMonit_FK  = models.ForeignKey(PtoMonit, verbose_name="Ponto Monit." )
    Parametro_FK= models.ForeignKey(Param, verbose_name="Parametro" )
    controle    = models.CharField(max_length=20, blank=True)
    data        = models.DateTimeField()
    dataInc     = models.DateTimeField(default=timezone.now, blank=True)
    vlr         = models.DecimalField(default=0, decimal_places=4, max_digits=16)
    vlrLbl      = models.CharField(default='',  max_length=36, blank=True)

    class Meta:
        verbose_name = u'Medicao'
        verbose_name_plural = u'Medicoes'
        ordering = ['data',]

    def __str__(self):
        return u'{0}'.format(self.controle)


class Midia(models.Model):

    Medicao_FK  = models.ForeignKey(Medicao, verbose_name="Medicao" )
    nome        = models.CharField(max_length=100, default='')
    url         = models.CharField(max_length=300)
    data        = models.DateField()
    docfile     = models.FileField(max_length=300,null=True, upload_to='midia')

    class Meta:
        verbose_name = u'Midia'
        verbose_name_plural = u'Midia'
        ordering = ['nome',]

    def __str__(self):
        return u'{0}'.format(self.nome)


class Texto(models.Model):

    Medicao_FK  = models.ForeignKey(Medicao, verbose_name="Medicao" )
    descricao   = models.TextField(default='')
    data        = models.DateField()

    class Meta:
        ordering = ['descricao',]

    def __str__(self):
        return u'{0}'.format(self.descricao)


class Relatorio(models.Model):

    Projeto_FK  = models.ForeignKey(Projeto, verbose_name="Projeto" )
    Parametro_FK= models.ForeignKey(Param, verbose_name="Parametro" )
    descricao   = models.TextField(default='')
    data        = models.DateField()
    class Meta:
        ordering = ['descricao',]

    def __str__(self):
        return u'{0}'.format(self.descricao)





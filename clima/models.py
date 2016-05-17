# -*- coding: utf-8 -*-
#!/usr/bin/env python

#from django.db import models
from django.contrib.gis.db import models
from paintstore.fields import ColorPickerField
# Create your models. here.

class Station(models.Model):
    tipo = models.CharField(max_length=1, default='N')
    Codigo = models.CharField(max_length=6)
    Nome = models.CharField(max_length=100)
    Estado = models.CharField(max_length=50)
    UF = models.CharField(max_length=2)
    Altitude = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    LatLong = models.CharField(max_length=100)
    posicao = models.PointField()

    objects = models.GeoManager()


    @property
    def geom(self):
        return self.posicao

    class Meta:
        ordering = ['Nome',]

    def __str__(self):
        return u'{0}'.format(self.Nome)

class Foco(models.Model):

    dataUTC     = models.DateTimeField()
    dataregUTC  = models.DateTimeField()
    arquivo     = models.CharField(max_length=100)

    class Meta:
        ordering = ['dataUTC',]

    def __unicode__(self):
        return u'{0}'.format(self.dataUTC)

class FocoItem(models.Model):

    foco_FK     = models.ForeignKey(Foco, verbose_name="Foco" )
    posicao     = models.PointField()
    Satzen      = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    PixSize     = models.DecimalField(default=0, decimal_places=4, max_digits=16)
    T4          = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    T11         = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    FireSize    = models.DecimalField(default=0, decimal_places=4, max_digits=16)
    Temp        = models.IntegerField(default=0)
    FRP         = models.IntegerField(default=0)
    Ecosystem   = models.IntegerField(default=0)
    FireFlag    = models.IntegerField(default=0)
    objects = models.GeoManager()

    @property
    def geom(self):
        return self.posicao

    def __unicode__(self):
        return u'{0}'.format(self.T4)



class Classe(models.Model):
    Nome = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0}'.format(self.Nome)

class Parametro(models.Model):
    codigo =  models.IntegerField(default=0)
    Nome = models.CharField(max_length=100)
    Classe_FK = models.ForeignKey(Classe, null=True, blank=True, default = None, verbose_name="Classe" )
    Planilha = models.CharField(max_length=200, default='')
    jan = models.IntegerField(default=0)
    fev = models.IntegerField(default=0)
    mar = models.IntegerField(default=0)
    abr = models.IntegerField(default=0)
    mai = models.IntegerField(default=0)
    jun = models.IntegerField(default=0)
    jul = models.IntegerField(default=0)
    ago = models.IntegerField(default=0)
    stb = models.IntegerField(default=0)
    out = models.IntegerField(default=0)
    nov = models.IntegerField(default=0)
    dez = models.IntegerField(default=0)
    tot = models.IntegerField(default=0)
    unidade = models.CharField(max_length=15, blank=True, default = '')
    corGrafico = ColorPickerField(help_text="Clique no campo para abrir o colorpicker.", max_length=7)

    class Meta:
        ordering = ['Nome',]

    def __unicode__(self):
        return u'{0}'.format(self.Nome)

class ResultStr(models.Model):

    Station_FK  = models.ForeignKey(Station, verbose_name="Estação" )
    Parametro_FK  = models.ForeignKey(Parametro, verbose_name="Parâmetro" )
    jan = models.CharField(max_length=20, default='')
    fev = models.CharField(max_length=20, default='')
    mar = models.CharField(max_length=20, default='')
    abr = models.CharField(max_length=20, default='')
    mai = models.CharField(max_length=20, default='')
    jun = models.CharField(max_length=20, default='')
    jul = models.CharField(max_length=20, default='')
    ago = models.CharField(max_length=20, default='')
    stb = models.CharField(max_length=20, default='')
    out = models.CharField(max_length=20, default='')
    nov = models.CharField(max_length=20, default='')
    dez = models.CharField(max_length=20, default='')
    tot = models.CharField(max_length=20, default='')


    def __unicode__(self):
        return u'{0}'.format(self.Parametro_FK)

class Resultado(models.Model):

    Station_FK  = models.ForeignKey(Station, verbose_name="Estação" )
    Parametro_FK  = models.ForeignKey(Parametro, verbose_name="Parâmetro" )
    jan = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    fev = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    mar = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    abr = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    mai = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    jun = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    jul = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    ago = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    stb = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    out = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    nov = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    dez = models.DecimalField(default=0, decimal_places=2, max_digits=16)
    tot = models.DecimalField(default=0, decimal_places=2, max_digits=16)


    def __unicode__(self):
        return u'{0}'.format(self.Parametro_FK)



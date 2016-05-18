# -*- coding: utf-8 -*- 
#!/usr/bin/env python 

from django.db import models

class DeteccaoChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Deteccao')

class CausaacidenteChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Acidente')


class ExtratacidenteChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Extrativismo')


class AtivagracidenteChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Atividade Agropecuaria')


class OutrasacidenteChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Outras Causas')


class CausadorChoices(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Causador')


class DanosVegetacoChoices(models.Model):
    descricao = models.CharField(max_length=100)


    def __unicode__(self):              
        return u'{0}'.format(self.descricao) 
    
    class Meta:
         verbose_name = (u'Danos Vegetacao')



class ROI(models.Model):


    AREAS_PROT_CHOICES = (
        ('TI', u'Terras Indigenas'),
        ('UC', u'Unidade de Conservacao'),      
    )

    TIPO_AREA_CHOICES = (
        ('FD', u'Federal'),
        ('ES', u'Estadual'),        
        ('MN', u'Municipal'),       
        ('RP', u'RPPN'),        
    )

    POSICAO_AREA_CHOICES = (
        ('DE',  u'Dentro'),
        ('EN',  u'Entorno'),            
    )
    
    AREAPUBPART_CHOICES = (
        ('CT',  u'Comunidade Tradicional'),
        ('AF',  u'Area Florestal'),         
        ('PR',  u'Propriedade Rural'),          
        ('FP',  u'Floresta Publica'),           
        ('AU',  u'Area Urbana'),            
        ('PA',  u'Projeto de Assentamento'),            
        
    )
    
    FORMA_EXT_CHOICES = (
        ('CT',  u'Combate Direto'),
        ('AF',  u'Combate Indireto'),           
        ('PR',  u'Extincao Natural'),                   
    )
    

   


    ROIID              = models.CharField(u'ROI',max_length=20, default= '', blank=True)
    
    municip            = models.CharField(u'Municipio', max_length=100, default= '', blank=True)
    distrito           = models.CharField(u'Distrito', max_length=100, default= '', blank=True)
    uf                 = models.CharField(u'UF', max_length=2, default= '', blank=True)
    
    local              = models.CharField(u'Local', max_length=100, default= '', blank=True)
    
    areasprot          = models.CharField(u'Area de Protevvcao', max_length=2, choices=AREAS_PROT_CHOICES, default= '  ')
    tipoarea           = models.CharField(u'Tipo de area', max_length=2, choices=TIPO_AREA_CHOICES, default= '  ')   
    posicaoarea        = models.CharField(u'Entorno?', max_length=2, choices=POSICAO_AREA_CHOICES, default= '  ')
    
    areapubpart        = models.CharField(u'Area publica ou Particular', max_length=2, choices=AREAPUBPART_CHOICES, default= '  ')
    areapubparttxt     = models.CharField(u'Outros:', max_length=100, default= '', blank=True)
    
    poslat             = models.CharField(u'Latitude', max_length=30, default= '', blank=True)
    poslong            = models.CharField(u'Longitude', max_length=30, default= '', blank=True)
    
    deteccao           = models.ManyToManyField(DeteccaoChoices, verbose_name=u'Deteccao')
    deteccaotxt        = models.CharField(u'Outros', max_length=300, default= '', blank=True)
    
    etapadatainic      = models.DateTimeField(u'Data Inicio')
    etapadatadetec     = models.DateTimeField(u'Data Deteccao')
    etapadataatac      = models.DateTimeField(u'Data Primeiro Ataque')
    etapadatacontr     = models.DateTimeField(u'Data Controle')
    etapadataext       = models.DateTimeField(u'Data Extincao')
    
    formaext           = models.CharField(u'Forma de Extincao', max_length=2, choices=FORMA_EXT_CHOICES, default= '  ')
    
    dificultcombate    = models.CharField(u'Dificuldade de combate:', max_length=300, default= '', blank=True)
    
    causaacidente      = models.ManyToManyField(CausaacidenteChoices,  verbose_name='Acidente')
    extratacidente     = models.ManyToManyField(ExtratacidenteChoices, verbose_name='Extrativismo')
    ativagracidente    = models.ManyToManyField(AtivagracidenteChoices,verbose_name='Atividade Agropecuaria')
    outrasacidente     = models.ManyToManyField(OutrasacidenteChoices, verbose_name='Outras Causas')
    
    outrasacidentedesc = models.CharField(u'Outros',max_length=300, default= '', blank=True)
    
    causador           = models.ManyToManyField(CausadorChoices)
    
    causadordesc       = models.CharField(u'Outros', max_length=300, default= '', blank=True)
    
    danosarea          = models.CharField(u'Estimativa area queimada', max_length=50, default= '', blank=True)
    
    danosestrutura     = models.CharField(u'Estruturas Atingidas', max_length=300, default= '', blank=True)
    
    danosanimais       = models.CharField(u'Animais mortos', max_length=300, default= '', blank=True)
    
    danosvegetacao     = models.ManyToManyField(DanosVegetacoChoices, verbose_name='Vegetacao Atingida')
    outdanosveget      = models.CharField(u'Outros:', max_length=300, default= '', blank=True)
    
    observaoces        = models.TextField(u'Observacoes', default='', blank=True)
    
    responsavel        = models.CharField(u'Responsavel', max_length=300, default= '', blank=True)
    data               = models.DateTimeField(u'Data')
    


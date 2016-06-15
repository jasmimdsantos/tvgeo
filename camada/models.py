from django.contrib.gis.db import models

class Local(models.Model):
    descricao = models.TextField()

    def __str__(self):
        return self.descricao

class Poligono(models.Model):
    local_FK = models.ForeignKey(Local)
    campo = models.MultiPolygonField()

    objects = models.GeoManager()

class Linha(models.Model):
    local_FK = models.ForeignKey(Local)
    campo = models.MultiLineStringField()

    objects = models.GeoManager()

class Ponto(models.Model):
    local_FK = models.ForeignKey(Local)
    campo = models.PointField()

    objects = models.GeoManager()

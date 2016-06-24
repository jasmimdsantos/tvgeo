from django.contrib.gis.db import models


class CampoLocalManager(models.Manager):
    def auto_get(self, instance):
        instance_FK = super(CampoLocalManager, self).get_queryset().get(pk=instance)
        if instance_FK.poligono:
            geometria = "poligono"
            campo = instance_FK.poligono.wkt
        elif instance_FK.ponto:
            geometria = "ponto"
            campo = instance_FK.ponto.wkt
        elif instance_FK.linha:
            geometria = "linha"
            campo= instance_FK.linha.wkt

        return geometria, campo


class Local(models.Model):
    descricao = models.TextField()
    poligono = models.MultiPolygonField(blank=True, null=True)
    ponto = models.PointField(blank=True, null=True)
    linha = models.MultiLineStringField(blank=True, null=True)
    objects = models.GeoManager()
    campo = CampoLocalManager()

    def __str__(self):
        return self.descricao
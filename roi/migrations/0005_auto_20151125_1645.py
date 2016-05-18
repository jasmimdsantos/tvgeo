# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0004_roi_deteccaotxt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roi',
            name='ROIID',
            field=models.CharField(default=b'', max_length=20, verbose_name='ROI', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='areapubpart',
            field=models.CharField(default=b'  ', max_length=2, verbose_name='Area publica ou Particular', choices=[(b'CT', 'Comunidade Tradicional'), (b'AF', 'Area Florestal'), (b'PR', 'Propriedade Rural'), (b'FP', 'Floresta Publica'), (b'AU', 'Area Urbana'), (b'PA', 'Projeto de Assentamento')]),
        ),
        migrations.AlterField(
            model_name='roi',
            name='areapubparttxt',
            field=models.CharField(default=b'', max_length=100, verbose_name='Outros:', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='areasprot',
            field=models.CharField(default=b'  ', max_length=2, verbose_name='Area de Protevvcao', choices=[(b'TI', 'Terras Indigenas'), (b'UC', 'Unidade de Conservacao')]),
        ),
        migrations.AlterField(
            model_name='roi',
            name='causadordesc',
            field=models.CharField(default=b'', max_length=300, verbose_name='Outros', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='danosanimais',
            field=models.CharField(default=b'', max_length=300, verbose_name='Animais mortos', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='danosarea',
            field=models.CharField(default=b'', max_length=50, verbose_name='Estimativa area queimada', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='danosestrutura',
            field=models.CharField(default=b'', max_length=300, verbose_name='Estruturas Atingidas', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='data',
            field=models.DateTimeField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='deteccaotxt',
            field=models.CharField(default=b'', max_length=300, verbose_name='Outros', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='dificultcombate',
            field=models.CharField(default=b'', max_length=300, verbose_name='Dificuldade de combate:', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='distrito',
            field=models.CharField(default=b'', max_length=100, verbose_name='Distrito', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapadataatac',
            field=models.DateTimeField(verbose_name='Data Primeiro Ataque'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapadatacontr',
            field=models.DateTimeField(verbose_name='Data Controle'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapadatadetec',
            field=models.DateTimeField(verbose_name='Data Deteccao'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapadataext',
            field=models.DateTimeField(verbose_name='Data Extincao'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapadatainic',
            field=models.DateTimeField(verbose_name='Data Inicio'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapahoraatac',
            field=models.CharField(default=b'', max_length=10, verbose_name='Hora Primeiro Ataque', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapahoracontr',
            field=models.CharField(default=b'', max_length=10, verbose_name='Hora Controle', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapahoradetec',
            field=models.CharField(default=b'', max_length=10, verbose_name='Hora Deteccao', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapahoraext',
            field=models.CharField(default=b'', max_length=10, verbose_name='Hora Extincao', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='etapahorainic',
            field=models.CharField(default=b'', max_length=10, verbose_name='Hora Inicio', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='formaext',
            field=models.CharField(default=b'  ', max_length=2, verbose_name='Forma de Extincao', choices=[(b'CT', 'Combate Direto'), (b'AF', 'Combate Indireto'), (b'PR', 'Extincao Natural')]),
        ),
        migrations.AlterField(
            model_name='roi',
            name='local',
            field=models.CharField(default=b'', max_length=100, verbose_name='Local', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='municip',
            field=models.CharField(default=b'', max_length=100, verbose_name='Municipio', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='observaoces',
            field=models.TextField(default=b'', verbose_name='Observacoes', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='outdanosveget',
            field=models.CharField(default=b'', max_length=300, verbose_name='Outros:', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='outrasacidentedesc',
            field=models.CharField(default=b'', max_length=300, verbose_name='Outros', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='posicaoarea',
            field=models.CharField(default=b'  ', max_length=2, verbose_name='Entorno?', choices=[(b'DE', 'Dentro'), (b'EN', 'Entorno')]),
        ),
        migrations.AlterField(
            model_name='roi',
            name='poslat',
            field=models.CharField(default=b'', max_length=30, verbose_name='Latitude', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='poslong',
            field=models.CharField(default=b'', max_length=30, verbose_name='Longitude', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='responsavel',
            field=models.CharField(default=b'', max_length=300, verbose_name='Responsavel', blank=True),
        ),
        migrations.AlterField(
            model_name='roi',
            name='tipoarea',
            field=models.CharField(default=b'  ', max_length=2, verbose_name='Tipo de area', choices=[(b'FD', 'Federal'), (b'ES', 'Estadual'), (b'MN', 'Municipal'), (b'RP', 'RPPN')]),
        ),
        migrations.AlterField(
            model_name='roi',
            name='uf',
            field=models.CharField(default=b'', max_length=2, verbose_name='UF', blank=True),
        ),
    ]

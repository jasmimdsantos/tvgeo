# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtivagracidenteChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CausaacidenteChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CausadorChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DanosVegetacoChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeteccaoChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExtratacidenteChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OutrasacidenteChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ROI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ROIID', models.CharField(default=b'', max_length=20, blank=True)),
                ('municip', models.CharField(default=b'', max_length=100, blank=True)),
                ('distrito', models.CharField(default=b'', max_length=100, blank=True)),
                ('uf', models.CharField(default=b'', max_length=2, blank=True)),
                ('local', models.CharField(default=b'', max_length=100, blank=True)),
                ('areasprot', models.CharField(default=b'  ', max_length=2, choices=[(b'TI', 'Terras Indigenas'), (b'UC', 'Unidade de Conservacao')])),
                ('tipoarea', models.CharField(default=b'  ', max_length=2, choices=[(b'FD', 'Federal'), (b'ES', 'Estadual'), (b'MN', 'Municipal'), (b'RP', 'RPPN')])),
                ('posicaoarea', models.CharField(default=b'  ', max_length=2, choices=[(b'DE', 'Dentro'), (b'EN', 'Entorno')])),
                ('areapubpart', models.CharField(default=b'  ', max_length=2, choices=[(b'CT', 'Comunidade Tradicional'), (b'AF', 'Area Florestal'), (b'PR', 'Propriedade Rural'), (b'FP', 'Floresta Publica'), (b'AU', 'Area Urbana'), (b'PA', 'Projeto de Assentamento')])),
                ('areapubparttxt', models.CharField(default=b'', max_length=100, blank=True)),
                ('poslat', models.CharField(default=b'', max_length=30, blank=True)),
                ('poslong', models.CharField(default=b'', max_length=30, blank=True)),
                ('etapadatainic', models.DateTimeField()),
                ('etapahorainic', models.CharField(default=b'', max_length=10, blank=True)),
                ('etapadatadetec', models.DateTimeField()),
                ('etapahoradetec', models.CharField(default=b'', max_length=10, blank=True)),
                ('etapadataatac', models.DateTimeField()),
                ('etapahoraatac', models.CharField(default=b'', max_length=10, blank=True)),
                ('etapadatacontr', models.DateTimeField()),
                ('etapahoracontr', models.CharField(default=b'', max_length=10, blank=True)),
                ('etapadataext', models.DateTimeField()),
                ('etapahoraext', models.CharField(default=b'', max_length=10, blank=True)),
                ('formaext', models.CharField(default=b'  ', max_length=2, choices=[(b'CT', 'Combate Direto'), (b'AF', 'Combate Indireto'), (b'PR', 'Extincao Natural')])),
                ('dificultcombate', models.CharField(default=b'', max_length=300, blank=True)),
                ('outrasacidentedesc', models.CharField(default=b'', max_length=300, blank=True)),
                ('causadordesc', models.CharField(default=b'', max_length=300, blank=True)),
                ('danosarea', models.CharField(default=b'', max_length=50, blank=True)),
                ('danosestrutura', models.CharField(default=b'', max_length=300, blank=True)),
                ('danosanimais', models.CharField(default=b'', max_length=300, blank=True)),
                ('outdanosveget', models.CharField(default=b'', max_length=300, blank=True)),
                ('observaoces', models.TextField(default=b'', blank=True)),
                ('responsavel', models.CharField(default=b'', max_length=300, blank=True)),
                ('data', models.DateTimeField()),
                ('ativagracidente', models.ManyToManyField(to='roi.AtivagracidenteChoices', null=True, blank=True)),
                ('causaacidente', models.ManyToManyField(to='roi.CausaacidenteChoices', null=True, blank=True)),
                ('causador', models.ManyToManyField(to='roi.CausadorChoices', null=True, blank=True)),
                ('danosvegetacao', models.ManyToManyField(to='roi.DanosVegetacoChoices', null=True, blank=True)),
                ('deteccao', models.ManyToManyField(to='roi.DeteccaoChoices', null=True, blank=True)),
                ('extratacidente', models.ManyToManyField(to='roi.ExtratacidenteChoices', null=True, blank=True)),
                ('outrasacidente', models.ManyToManyField(to='roi.OutrasacidenteChoices', null=True, blank=True)),
            ],
        ),
    ]

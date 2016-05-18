# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0005_auto_20151125_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ativagracidentechoices',
            options={'verbose_name': 'Atividade Agropecuaria'},
        ),
        migrations.AlterModelOptions(
            name='causaacidentechoices',
            options={'verbose_name': 'Acidente'},
        ),
        migrations.AlterModelOptions(
            name='causadorchoices',
            options={'verbose_name': 'Causador'},
        ),
        migrations.AlterModelOptions(
            name='danosvegetacochoices',
            options={'verbose_name': 'Danos Vegetacao'},
        ),
        migrations.AlterModelOptions(
            name='deteccaochoices',
            options={'verbose_name': 'Deteccao'},
        ),
        migrations.AlterModelOptions(
            name='extratacidentechoices',
            options={'verbose_name': 'Extrativismo'},
        ),
        migrations.AlterModelOptions(
            name='outrasacidentechoices',
            options={'verbose_name': 'Outras Causas'},
        ),
        migrations.RemoveField(
            model_name='roi',
            name='etapahoraatac',
        ),
        migrations.RemoveField(
            model_name='roi',
            name='etapahoracontr',
        ),
        migrations.RemoveField(
            model_name='roi',
            name='etapahoradetec',
        ),
        migrations.RemoveField(
            model_name='roi',
            name='etapahoraext',
        ),
        migrations.RemoveField(
            model_name='roi',
            name='etapahorainic',
        ),
        migrations.AlterField(
            model_name='roi',
            name='ativagracidente',
            field=models.ManyToManyField(to='roi.AtivagracidenteChoices', verbose_name=b'Atividade Agropecuaria'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='causaacidente',
            field=models.ManyToManyField(to='roi.CausaacidenteChoices', verbose_name=b'Acidente'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='danosvegetacao',
            field=models.ManyToManyField(to='roi.DanosVegetacoChoices', verbose_name=b'Vegetacao Atingida'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='deteccao',
            field=models.ManyToManyField(to='roi.DeteccaoChoices', verbose_name='Deteccao'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='extratacidente',
            field=models.ManyToManyField(to='roi.ExtratacidenteChoices', verbose_name=b'Extrativismo'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='outrasacidente',
            field=models.ManyToManyField(to='roi.OutrasacidenteChoices', verbose_name=b'Outras Causas'),
        ),
    ]

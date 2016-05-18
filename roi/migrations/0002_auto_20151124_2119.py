# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roi',
            name='ativagracidente',
            field=models.ManyToManyField(to='roi.AtivagracidenteChoices'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='causaacidente',
            field=models.ManyToManyField(to='roi.CausaacidenteChoices'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='danosvegetacao',
            field=models.ManyToManyField(to='roi.DanosVegetacoChoices'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='deteccao',
            field=models.ManyToManyField(to='roi.DeteccaoChoices'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='extratacidente',
            field=models.ManyToManyField(to='roi.ExtratacidenteChoices'),
        ),
        migrations.AlterField(
            model_name='roi',
            name='outrasacidente',
            field=models.ManyToManyField(to='roi.OutrasacidenteChoices'),
        ),
    ]

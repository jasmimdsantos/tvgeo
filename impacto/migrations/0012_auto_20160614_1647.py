# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impacto', '0011_auto_20160614_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quadro',
            name='descricao_curta',
            field=models.CharField(max_length=30, verbose_name='Descrição Curta *Máximo 30 caracteres'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impacto', '0008_quadro_descricao_curta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quadro',
            name='descricao_curta',
            field=models.CharField(max_length=20, verbose_name='Descrição Curta'),
        ),
    ]

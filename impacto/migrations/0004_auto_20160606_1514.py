# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impacto', '0003_auto_20160606_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faseprojeto',
            name='descricao',
            field=models.CharField(choices=[('P', 'Planejamento'), ('O', 'Operação'), ('I', 'Implantação'), ('F', 'Fechamento')], max_length=1, verbose_name='Descrição da Fase'),
        ),
    ]

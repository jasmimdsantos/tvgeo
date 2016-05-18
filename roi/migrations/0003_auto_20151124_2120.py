# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0002_auto_20151124_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roi',
            name='causador',
            field=models.ManyToManyField(to='roi.CausadorChoices'),
        ),
    ]

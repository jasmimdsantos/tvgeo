# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0003_auto_20151124_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='roi',
            name='deteccaotxt',
            field=models.CharField(default=b'', max_length=300, blank=True),
        ),
    ]

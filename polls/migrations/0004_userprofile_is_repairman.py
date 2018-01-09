# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20180103_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_repairman',
            field=models.BooleanField(default=False),
        ),
    ]

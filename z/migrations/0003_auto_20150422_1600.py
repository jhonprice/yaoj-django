# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('z', '0002_auto_20150421_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='join_at',
        ),
        migrations.AddField(
            model_name='problem',
            name='input_spec',
            field=models.TextField(default='s', verbose_name='input specification'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='output_spec',
            field=models.TextField(default='s', verbose_name='output specification'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='sample_input',
            field=models.TextField(default='ff'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='sample_output',
            field=models.TextField(default='ff'),
            preserve_default=False,
        ),
    ]

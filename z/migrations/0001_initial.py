# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('desc', models.TextField(verbose_name='Group description')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('join_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='z.Group')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('desc', models.TextField(verbose_name='problem description')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mem_limit', models.IntegerField(verbose_name='memory limit(in MB)', default=128)),
                ('time_limit', models.IntegerField(verbose_name='time limit(in ms)', default=1000)),
                ('test_input', models.TextField()),
                ('test_output', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slug', models.SlugField(max_length=32)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mem_consumed', models.IntegerField(verbose_name='memory consumed(in MB)')),
                ('time_consumed', models.IntegerField(verbose_name='time consumed(in ms)')),
                ('verdict', models.CharField(max_length=32)),
                ('source_code', models.TextField()),
                ('owner', models.ForeignKey(to='z.Member')),
                ('problem', models.ForeignKey(to='z.Problem')),
            ],
        ),
    ]

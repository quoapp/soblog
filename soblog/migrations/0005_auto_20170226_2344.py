# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soblog', '0004_auto_20170224_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.AddField(
            model_name='blog',
            name='comment_times',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='互动次数'),
        ),
    ]

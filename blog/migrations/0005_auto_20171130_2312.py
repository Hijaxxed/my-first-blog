# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-30 23:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171130_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorytopost',
            name='category',
        ),
        migrations.RemoveField(
            model_name='categorytopost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category'),
        ),
        migrations.DeleteModel(
            name='CategoryToPost',
        ),
    ]

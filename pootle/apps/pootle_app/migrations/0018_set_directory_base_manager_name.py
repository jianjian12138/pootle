# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 07:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_app', '0017_drop_stray_directories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='directory',
            options={'base_manager_name': 'objects', 'default_permissions': (), 'ordering': ['name']},
        ),
    ]

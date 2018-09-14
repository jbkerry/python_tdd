# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-14 16:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_shareduser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareduser',
            name='user',
        ),
        migrations.AlterField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(related_name='list_shared_with', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='SharedUser',
        ),
    ]

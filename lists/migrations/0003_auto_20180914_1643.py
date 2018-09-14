# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-14 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_list_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(to='lists.SharedUser'),
        ),
    ]

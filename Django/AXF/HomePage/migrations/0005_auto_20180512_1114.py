# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-12 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0004_usermodel_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good', to='HomePage.Goods'),
        ),
    ]

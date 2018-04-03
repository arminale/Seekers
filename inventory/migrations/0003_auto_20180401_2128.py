# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-02 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_book_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(default=0),
        ),
    ]

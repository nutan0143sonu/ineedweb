# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-01 04:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0018_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='sender',
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notifcation', to=settings.AUTH_USER_MODEL),
        ),
    ]

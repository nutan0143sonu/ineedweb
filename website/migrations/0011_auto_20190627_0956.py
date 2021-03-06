# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-27 09:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0010_auto_20190627_0704'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Employer or Job_seeker Message')),
                ('is_attachment', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Chat',
            },
        ),
        migrations.AddField(
            model_name='userapplyjob',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatmodel',
            name='accepted_applied_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_applied_job', to='website.UserApplyJob'),
        ),
        migrations.AddField(
            model_name='chatmodel',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatmodel',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]

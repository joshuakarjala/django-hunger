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
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('used', models.DateTimeField(null=True, verbose_name='Used', blank=True)),
                ('invited', models.DateTimeField(null=True, verbose_name='Invited', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvitationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=30, verbose_name='Invitation code')),
                ('private', models.BooleanField(default=True)),
                ('max_invites', models.PositiveIntegerField(default=1, verbose_name='Max number of invitations')),
                ('num_invites', models.PositiveIntegerField(default=1, verbose_name='Remaining invitations')),
                ('invited_users', models.ManyToManyField(related_name='invitations', through='hunger.Invitation', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='created_invitations', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invitation',
            name='code',
            field=models.ForeignKey(blank=True, to='hunger.InvitationCode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('user', 'code')]),
        ),
    ]

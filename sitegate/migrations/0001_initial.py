# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import etc.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(unique=True, max_length=253, verbose_name='Domain name')),
                ('enabled', models.BooleanField(default=True, help_text="If enabled visitors won't be able to sign up with this domain name in e-mail.", db_index=True, verbose_name='Enabled')),
            ],
            options={
                'verbose_name': 'Blacklisted domain',
                'verbose_name_plural': 'Blacklisted domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(verbose_name=b'dummy', unique=True, max_length=128, editable=False)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('time_accepted', models.DateTimeField(verbose_name='Date accepted', null=True, editable=False)),
                ('expired', models.BooleanField(default=False, help_text="Expired codes couldn't be used for repeated account activations.", db_index=True, verbose_name='Expired')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Activation code',
                'verbose_name_plural': 'Activation codes',
            },
            bases=(etc.models.InheritedModel, models.Model),
        ),
        migrations.CreateModel(
            name='InvitationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(verbose_name=b'dummy', unique=True, max_length=128, editable=False)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('time_accepted', models.DateTimeField(verbose_name='Date accepted', null=True, editable=False)),
                ('expired', models.BooleanField(default=False, help_text="Visitors won't be able to sign up with an expired code.", db_index=True, verbose_name='Expired')),
                ('acceptor', models.ForeignKey(related_name=b'acceptors', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Acceptor')),
                ('creator', models.ForeignKey(related_name=b'creators', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invitation code',
                'verbose_name_plural': 'Invitation codes',
            },
            bases=(etc.models.InheritedModel, models.Model),
        ),
    ]

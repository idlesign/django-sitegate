# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitegate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfirmation',
            name='new_email',
            field=models.EmailField(default=None, max_length=254, null=True, verbose_name='email address', blank=True),
        ),
    ]

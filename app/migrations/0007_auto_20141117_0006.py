# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_location_slug_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='slug_url',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from=[b'name', b'architecture'], blank=True, null=True, overwrite=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MakeGroups(apps, schema_editor):
    Location = apps.get_model("app", "location")
    Landscape = apps.get_model("app","landscapes")
    Hardscape = apps.get_model("app","hardscapes")

    for loc in Location.objects.all():
        if (loc.architecture == "L"):
            L = Landscape()
            L.name = loc.name
            L.slug_url = loc.slug_url
            L.detail = loc.detail
            L.save()
        if (loc.architecture == "H"):
            H = Hardscape()
            H.name = loc.name
            H.slug_url = loc.slug_url
            H.detail = loc.detail
            H.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_hardscapes_landscapes_photogroup'),
    ]

    operations = [
    migrations.RunPython(MakeGroups),
    ]
    

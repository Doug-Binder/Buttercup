from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.functional import cached_property


def upload_to_s3(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'photos/%s%s%s' % (instance.name,
        filename_base,
        filename_ext.lower(),
    )
def upload_to_media(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'photos/%s%s%s' % (instance.title,
        filename_base,
        filename_ext.lower(),
    )


class photogroup(models.Model):

        name = models.CharField(max_length=255, null=True, blank=True)
        slug_url = AutoSlugField(populate_from=['name'],
                         overwrite=True, null=True, blank=True)
        detail = models.CharField(max_length=512, null=True, blank=True)

        @cached_property
        def get_hero(self):
            r  = self.pictures.get(hero=True)
            if r:
                return r
            return None
            
        def __str__(self):
            return self.name

class landscape(photogroup):
        ARCHITECTURE_TYPES = (
            ('L', 'LandScapes'),
            ('H', 'HardScapes'),
            )
        architecture = models.CharField(max_length=1, choices=ARCHITECTURE_TYPES, default = 'L')

class hardscape(photogroup):
        ARCHITECTURE_TYPES = (
            ('L', 'LandScapes'),
            ('H', 'HardScapes'),
            )
        architecture = models.CharField(max_length=1, choices=ARCHITECTURE_TYPES, default = 'L')    

# Create your models here.
class location(models.Model):
        ARCHITECTURE_TYPES = (
        ('L', 'LandScapes'),
        ('H', 'HardScapes'),
        )
        name = models.CharField(max_length=255, null=True, blank=True)
        architecture = models.CharField(max_length=1, choices=ARCHITECTURE_TYPES)
        slug_url = AutoSlugField(populate_from=['name'],
                         overwrite=True, null=True, blank=True)
        detail = models.CharField(max_length=512, null=True, blank=True)
        @cached_property
        def get_hero(self):
            r  = self.pictures.get(hero=True)
            if r:
                return r
            return None

        def __str__(self):
            return self.name

class photo(models.Model):
        slug_url = AutoSlugField(populate_from=['name', 'display'],
                         overwrite=True, null=True, blank=True)
        name = models.CharField(max_length=255)
        display = models.ImageField(upload_to=upload_to_s3, blank=True,null=True)
        order = models.IntegerField(null=True, blank=True)
        location = models.ForeignKey(location, null=True, blank=True, related_name='pictures')
        detail = models.CharField(max_length=512, null=True, blank=True)
        hero = models.BooleanField(default=False)
        landscape = models.ForeignKey(landscape, null=True, blank=True, related_name='pictures')
        hardscape = models.ForeignKey(hardscape, null=True, blank=True, related_name='pictures')

        @property
        def location_slug(self):
            if self.landscape:
                return self.landscape.slug_url
            elif self.hardscape:
                return self.hardscape.slug_url
            else: 
                return None
        @property
        def next_photo_hardscape(self):
            next = self.order
            next = next + 1
            return photo.objects.filter(order=next, hardscape=self.hardscape).get()

        @property
        def next_photo_landscape(self):
            next = self.order
            next = next + 1
            p = photo.objects.filter(order=next, landscape=self.landscape)
            if p:
                return p.get()
            else: 
                return False 

        @property
        def prev_photo_hardscape(self):
            next = self.order
            next = next - 1
            p = photo.objects.filter(order=next, hardscape=self.hardscape)
            if p:
                return p.get()
            else: 
                return False 

        @property
        def prev_photo_landscape(self):
            next = self.order
            next = next - 1
            p = photo.objects.filter(order=next, landscape=self.landscape)
            if p:
                return p.get()
            else: 
                return False 

        class Meta:
            ordering = ["order"]

class media(models.Model):
        url = models.URLField(max_length=255, null=True, blank=True)
        title = models.CharField(max_length=255, null=True, blank=True)
        display = models.ImageField(upload_to=upload_to_media, blank=True,null=True)
        order = models.IntegerField(null=True, blank=True)

        class Meta: 
            ordering = ["order"]

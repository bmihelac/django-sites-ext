from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    site = models.ForeignKey(Site, verbose_name=_('site'))

    def __unicode__(self):
        return "%s %s" % (self.site.name, self.name)

    def get_absolute_url(self):
        return ('view_or_url_name', [str(self.id)])


class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    site = models.ForeignKey(Site, verbose_name=_('site'))
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))

    def __unicode__(self):
        return "%s %s" % (self.site.name, self.name)


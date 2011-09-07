Django Sites Ext
================

ChangeSiteMixin is a helper mixin aimed to make editing of objects in 
multi site environment easier.

Current functionality in ``ChangeSiteAdmin`` works like this:

1. When creating new object, administrator is offered to choose site to which
   object will be associated

2. In change_form view, ``site`` is restricted to selected site and cannot be 
   changed. Also, choices for fields specified in ``filter_by_site_fields`` 
   are limited only to selected site.

3. When editing existing object, "Change site" button allows to change site
   this object belongs to. If model has ``changesite`` method, it would be
   called to allow further work to be performed when site is changing.

Requirements
------------

* Django 1.3 or later

Configuration
-------------

1. Put ``sites_ext`` into your INSTALLED_APPS at settings module::

        INSTALLED_APPS = (
           ...
           'sites_ext',
        )

Usage
-----

Replace `admin.ModelAdmin`` with ``ChangeSiteAdmin`` for those models
which should have support for changing language::

    from django.contrib import admin
    from sites_ext.admin import ChangeSiteAdmin

    from models import Product

    class ProductAdmin(ChangeSiteAdmin):
        filter_by_site_fields = ('categories', )

    admin.site.register(Product, ProductAdmin)

Example application
-------------------

Example app is bundled, username and password for admin are: admin:password.


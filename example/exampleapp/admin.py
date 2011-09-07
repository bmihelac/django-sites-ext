from django.contrib import admin

from sites_ext.admin import ChangeSiteAdmin

from models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(ChangeSiteAdmin):
    filter_by_site_fields = ('categories', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


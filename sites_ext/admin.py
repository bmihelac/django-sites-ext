from django.contrib import admin
from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, url
from django.utils.encoding import force_unicode
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext


class ChooseSiteForm(forms.Form):
    site = forms.ModelChoiceField(
            queryset=Site.objects.all(),
            empty_label=None,
            widget=forms.RadioSelect()
            )


class ChangeSiteAdmin(admin.ModelAdmin):
    """
    Extends ``django.contrib.admin.ModelAdmin`` class. Provides some extra
    views for change site management at admin panel. It also changes
    default ``change_form_template`` option to
    ``'admin/sites_ext/model/change_form.html'`` which is required for
    adding ``changesite`` object action.

    **Extra options**

    ``filter_by_site_fields`` - list of fields to filter to selected site.
    Can be field name or tuple consisting of field name and lookup field.
    """
    change_form_template = 'admin/sites_ext/model/change_form.html'

    def get_site_id(self, request, obj=None):
        if obj:
            return obj.site.id
        else:
            return int(request.GET.get('site', 0))

    def get_urls(self):
        urls = super(ChangeSiteAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        my_urls = patterns('',
            url(r'^(?P<object_id>\d+)/changesite/$',
                self.admin_site.admin_view(self.changesite),
                name='%s_%s_changesite' % info),
        )
        return my_urls + urls

    def add_view(self, request, *args, **kwargs):
        site_id = self.get_site_id(request)
        if not site_id:
            return self.selectsite(request)
        return super(ChangeSiteAdmin, self).add_view(request, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(
                ChangeSiteAdmin, self
                ).get_form(request, obj, **kwargs)
        site_id = self.get_site_id(request, obj)
        # disable adding new site in this form
        field = form.base_fields['site']
        field.widget.can_add_related = False
        # restrict site choices to selected site
        field.choices = [c for c in field.choices if c[0] == site_id]
        # restrict additional ForeignKey and ManyToManyField fields
        for opts in getattr(self, 'filter_by_site_fields', []):
            if type(opts) is str:
                field = opts
                kwargs = {'site__id': site_id}
            else:
                field = opts[0]
                kwargs = {opts[1]: site_id}
            field = form.base_fields[field]
            field.queryset = field.queryset.filter(**kwargs)
        return form

    def selectsite(self, request):
        model = self.model
        opts = model._meta
        form = ChooseSiteForm()
        context = {
                'form': form,
                'title': _('Select site for new %s') % force_unicode(opts.verbose_name),
                }
        template = 'admin/sites_ext/model/selectsite.html'
        return render_to_response(template, context)

    def changesite(self, request, object_id, **kwargs):
        original = self.get_object(request, object_id)
        if request.POST:
            form = ChooseSiteForm(request.POST)
            if form.is_valid():
                site = form.cleaned_data['site']
                if (hasattr(original, 'changesite')):
                    original.changesite(site)
                else:
                    original.site = site
                    original.save()
                msg = _("Site has been changed to %s") % (site)
                request.user.message_set.create(message=unicode(msg))
                info = self.model._meta.app_label, self.model._meta.module_name
                return redirect('admin:%s_%s_change' % info, original.id)
        else:
            form = ChooseSiteForm(initial={'site': original.site})

        model = self.model
        opts = model._meta
        context = RequestContext(request, {
                'form': form,
                'title': _('Change site for %s') % force_unicode(opts.verbose_name),
                })
        template = 'admin/sites_ext/model/changesite.html'
        return render_to_response(template, context)



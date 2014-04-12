# -*- coding: utf-8 -*-

from django.contrib import admin

from serpent.models import Serpent, Repas, Mue, Mensuration, Maintenance, OperationMaintenance
from serpent.admin import SerpentAdmin, RepasAdmin, MueAdmin, MensurationAdmin, MaintenanceAdmin


class Site(admin.sites.AdminSite):
    """ Administration personnalisée du site """
    
    def get_urls(self):
        """ Ajout d'URL personnalisées """
        from django.conf.urls.defaults import patterns
        from serpent.admin import select_serpent
        
        urls = super(Site, self).get_urls()
        site_urls = patterns('',
            (r'^serpent/select/(\d+)$', select_serpent)
        )
        return site_urls + urls
    
    def index(self, request):
        """ Affiche les serpents de l'utilisateur sur la page d'accueil """
        from django.template.context import RequestContext
        from django.shortcuts import render_to_response

        return render_to_response('admin/selecteur.html', {
            'serpents': Serpent.objects.filter(proprietaire=request.user)
            }, context_instance=RequestContext(request)
        )

    def app_index(self, request, app_label, extra_context=None):
        """ Change quelques éléments graphiques sur la page du serpent """
        extra_context = extra_context or {}
        extra_context['title'] = request.session.get('serpent')
        extra_context['request'] = request
        
        return super(self.__class__, self).app_index(request, app_label, extra_context)

        
site = Site()
admin.site = site
admin.autodiscover()

site.register(Serpent, SerpentAdmin)
site.register(Repas, RepasAdmin)
site.register(Mue, MueAdmin)
site.register(Mensuration, MensurationAdmin)
site.register(Maintenance, MaintenanceAdmin)
site.register(OperationMaintenance)

# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Serpent, Repas


def select_serpent(request, id):
    """ Met le serpent de l'utilisateur en session """
    from django.shortcuts import get_object_or_404, redirect
    
    serpent = get_object_or_404(Serpent, pk=id, proprietaire=request.user)
    request.session['serpent'] = serpent
    return redirect('/serpent/')

    
class SerpentAdmin(admin.ModelAdmin):
    """ Opérations d'administration sur un serpent """
    
    list_display = ('miniature', 'nom', 'espece', 'sexe', 'age')
    list_filter = ('ajoute_le','sexe')
    exclude = ('proprietaire',)
    fieldsets = [
        (None, {'fields': ('nom', 'espece', 'sexe', 'date_de_naissance', 'localite', 'phase', 'image',)}),
        ('Acquisition', {'fields': ('date_acquisition', 'lieu_acquisition', 'type_acquisition', 'cites_acquisition',), 'classes': ('collapse',)}),
        ('Sortie', {'fields': ('sortie', 'date_sortie', 'motif_sortie', 'acquereur_sortie',), 'classes': ('collapse',)}),
    ]
    
    def queryset(self, request):
        """ Ne récupère que les serpents de l'utilisateur connecté """
        return Serpent.objects.filter(proprietaire=request.user)

    def save_model(self, request, obj, form, change):
        """ Met l'utilisateur connecté comme propriétaire du nouveau serpent """
        
        if not change:
            obj.proprietaire = request.user
            request.session['serpent'] = obj
        obj.save()
        
    def delete_model(self, request, obj):
        """ Supprime également le serpent en session """
        
        if 'serpent' in request.session.keys() and request.session['serpent'] == obj:
            del(request.session['serpent'])
        obj.delete()

        
class SerpentRelatedAdmin(admin.ModelAdmin):
    """ Opérations sur tous ce qui est lié à un serpent (mue, repas ...) """
    exclude = ('serpent',)
    
    def has_add_permission(self, request):
        """ Uniquement si un serpent est sélectionné (en session) """
        
        has_class_permission = super(self.__class__, self).has_change_permission(request)
        if not has_class_permission:
            return False
        if 'serpent' not in request.session:
            return False
        return True
    
    def queryset(self, request):
        """" Récupère les objets du serpent sélectionné (en session) ou du propriétaire """
        
        qs = super(admin.ModelAdmin, self).queryset(request)
        if 'serpent' in request.session.keys():
            return qs.filter(serpent=request.session['serpent'])
        else:
            return qs.filter(serpent__proprietaire=request.user)

    def save_model(self, request, obj, form, change):
        """ Charge le nouveau serpent en session """
        
        if not change:
            obj.serpent = request.session['serpent']
        obj.save()

        
class RepasAdmin(SerpentRelatedAdmin):
    list_display = ('date', 'proie', 'etat', 'quantite', 'commentaire',)
    list_filter = ('date', 'proie', 'etat',)

    
class MueAdmin(SerpentRelatedAdmin):
    list_display = ('date', 'etat',)
    list_filter = ('date',)

    
class MensurationAdmin(SerpentRelatedAdmin):
    list_display = ('date', 'taille_avec_unite', 'poids_avec_unite',)
    list_filter = ('date',)

    
class MaintenanceAdmin(SerpentRelatedAdmin):
    list_display = ('date', 'liste_operations')
    list_filter = ('date', 'operations')
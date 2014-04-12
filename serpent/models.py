# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from sorl import thumbnail

from django.contrib.auth.models import User


class Serpent(models.Model):
    SEXES = (
        (u'M', u'Mâle'),
        (u'F', u'Femelle'),
        (u'I', u'Indéterminé'),
    )
    
    TYPES_ACQUISITIONS = (
        (u'NC', u'NC'),
        (u'WC', u'WC'),
        (u'FRM', u'Farming'),
    )
    
    nom = models.CharField("Nom", max_length=50)
    espece = models.CharField("Espèce", max_length=100)
    sexe = models.CharField("Sexe", max_length=1, choices=SEXES)
    date_de_naissance = models.DateField("Date de naissance")
    localite = models.CharField("Localité", max_length=50, blank=True)
    phase = models.CharField("Phase", max_length=50, blank=True)
    date_acquisition = models.DateField("Date", null=True, blank=True)
    lieu_acquisition = models.CharField("Lieu", max_length=50, blank=True)
    type_acquisition = models.CharField("Type", max_length=10, choices=TYPES_ACQUISITIONS, blank=True)
    cites_acquisition = models.CharField("CITES", max_length=25, blank=True)
    sortie = models.BooleanField("Sortie")
    date_sortie = models.DateField("Date", null=True, blank=True)
    motif_sortie = models.TextField("Motif", blank=True)
    acquereur_sortie = models.CharField("Acquéreur", max_length=50, blank=True)
    image = thumbnail.ImageField("Image", upload_to='images/galerie', null=True, blank=True)
    ajoute_le = models.DateField("Ajouté le", auto_now_add=True)
    modifie_le = models.DateField("Modifié le", auto_now=True)
    proprietaire = models.ForeignKey(User, verbose_name="Propriétaire")
        
    def age(self):
        from datetime import date
        days_in_year = 365.25
        
        age = int((date.today() - self.date_de_naissance).days/days_in_year)
        jours = int((date.today() - self.date_de_naissance).days%days_in_year)
        return "{0} ans et {1} jours".format(age, jours)
        
    def miniature(self):
        from sorl.thumbnail import get_thumbnail
        from settings import STATIC_URL
        
        if self.image:
            img = get_thumbnail(self.image, '75x75', crop='center')
            url = img.url
        else:
            url =  STATIC_URL + 'images/serpent_defaut.png'
        return '<img src="{0}" alt="{0}" width="75" height="75" />'.format(url, self.nom)
    miniature.allow_tags = True

    def __unicode__(self):
        return self.nom.capitalize()
    
    class Meta:
        verbose_name = u"Serpent"
        verbose_name_plural = u"Serpents"
        ordering = ('-modifie_le',)

@receiver(models.signals.pre_delete, sender=Serpent)
def delete_photo(sender, instance, *args, **kargs):
    from sorl import thumbnail
    if instance.image:
        thumbnail.delete(instance.image)

        
class Repas(models.Model):
    TYPES_PROIES = (
        (u'S-R', u'Souris - rosé'),
        (u'S-B', u'Souris - blanchon'),
        (u'S-S', u'Souris - sauteuse'),
        (u'S-A', u'Souris - adulte'),
        (u'R-R', u'Rat - rosé'),
        (u'R-0', u'Rat - jeune inf 100g'),
        (u'R-100', u'Rat - jeune 100-200g'),
        (u'R-A', u'Rat - adulte'),
    )
    
    ETATS = (
        (u'C', u'Congelé'),
        (u'V', u'Vivant'),
        (u'F', u'Fraîchement tué'),
    )
    
    date = models.DateField("Date")
    proie = models.CharField("Proie", max_length=5, choices=TYPES_PROIES)
    etat = models.CharField("État", max_length=1, choices=ETATS)
    quantite = models.PositiveIntegerField("Quantité", default=1)
    commentaire = models.TextField("Commentaire", blank=True)
    serpent = models.ForeignKey(Serpent, verbose_name="Serpent")
    
    def __unicode__(self):
        return u"Repas du {0} : {1} {2} {3}".format(self.date, self.quantite, self.get_proie_display(), self.get_etat_display())
    
    class Meta:
        verbose_name = u"Repas"
        verbose_name_plural = u"Repas"
        ordering = ('-date',)

        
class Mue(models.Model):    
    date = models.DateField("Date")
    etat = models.CharField("État", max_length=100, blank=True)
    serpent = models.ForeignKey(Serpent, verbose_name="Serpent")
    
    def __unicode__(self):
        return u"Mue du {0}".format(self.date)
    
    class Meta:
        verbose_name = u"Mue"
        verbose_name_plural = u"Mues"
        ordering = ('-date',)

        
class Mensuration(models.Model):    
    date = models.DateField("Date")
    taille = models.PositiveIntegerField("Taille", help_text="en centimètres", blank=True, null=True)
    poids = models.PositiveIntegerField("Poids", help_text="en grammes", blank=True, null=True)
    serpent = models.ForeignKey(Serpent, verbose_name="Serpent")
    
    def __unicode__(self):
        taille = self.taille or '_'
        poids = self.poids or '_'
        return u"Mensuration du {0} : {1}cm pour {2}g".format(self.date, taille, poids)

    def taille_avec_unite(self):
        if self.taille:
            return "{0} cm".format(self.taille)
        return "(aucun-e)"
    taille_avec_unite.short_description = 'Taille'

    def poids_avec_unite(self):
        if self.poids:
            return "{0} g".format(self.poids)
        return "(aucun-e)"
    poids_avec_unite.short_description = 'Poids'
        
    class Meta:
        verbose_name = u"Mensuration"
        verbose_name_plural = u"Mensurations"
        ordering = ('-date',)

        
class OperationMaintenance(models.Model):    
    nom = models.CharField("Nom", max_length=100, unique=True)
    
    def __unicode__(self):
        return self.nom
    
    class Meta:
        verbose_name = u"Opération"
        verbose_name_plural = u"Opérations"
        ordering = ('-nom',)

        
class Maintenance(models.Model):
    date = models.DateField("Date")
    operations = models.ManyToManyField(OperationMaintenance, verbose_name="opérations")
    serpent = models.ForeignKey(Serpent, verbose_name="Serpent")
    
    def liste_operations(self):
        return ', '.join([op.nom for op in self.operations.all()])
            
    def __unicode__(self):
        return u"Maintenance du {0} : {1}".format(self.date, self.liste_operations())
    
    class Meta:
        verbose_name = u"Maintenance"
        verbose_name_plural = u"Maintenance"
        ordering = ('-date',)
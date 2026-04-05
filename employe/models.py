from django.db import models

# Create your models here.
# classe employer

class Employe(models.Model):
    SEXE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]
    ETAT_CIVIL_CHOICES = [
        ('Célibataire', 'Célibataire'),
        ('Marié(e)', 'Marié(e)'),
        ('Divorcé(e)', 'Divorcé(e)'),
        ('Veuf(ve)', 'Veuf(ve)'),
    ]
    FONCTION_CHOICES = [
        ('Directeur', 'Directeur'),
        ('Manager', 'Manager'),
        ('Employé', 'Employé'),
        ('Stagiaire', 'Stagiaire'),
        ('Autre', 'Autre'),
    ]
    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    sexe = models.CharField(max_length=5, choices=SEXE_CHOICES, verbose_name="Sexe")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    etat_civil = models.CharField(max_length=12, choices=ETAT_CIVIL_CHOICES, verbose_name="État civil")
    telephone = models.CharField(max_length=10, blank=True, null=True, verbose_name="Téléphone")
    fonction = models.CharField(max_length=50, choices=FONCTION_CHOICES, verbose_name="Fonction")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Photo")
    def __str__(self):
        return f"{self.nom} {self.prenom}"
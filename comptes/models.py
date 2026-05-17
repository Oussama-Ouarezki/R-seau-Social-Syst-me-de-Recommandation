"""
Modèles pour la gestion des comptes utilisateurs et profils.

Analyse des Réseaux Sociaux - Master 2
--------------------------------------
Ce module définit les modèles Profile et Interest qui représentent
les NOEUDS du graphe social. Chaque utilisateur est un noeud, et
ses centres d'intérêt permettent de calculer la similarité entre profils.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Interest(models.Model):
    """
    Représente un centre d'intérêt (tag/thématique).
    
    Utilisé pour:
    - Personnaliser les profils utilisateurs
    - Calculer la similarité entre profils (recommandation d'amis)
    - Catégoriser les posts (recommandation de contenus)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    
    class Meta:
        verbose_name = "Centre d'intérêt"
        verbose_name_plural = "Centres d'intérêt"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Extension du modèle User de Django avec informations supplémentaires.
    
    Dans le graphe social:
    - Chaque Profile représente un NOEUD
    - Les relations d'amitié (app 'amis') représentent les ARÊTES
    
    La similarité entre deux profils est calculée via:
    - Les centres d'intérêt communs (Jaccard similarity)
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="Utilisateur"
    )
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name="Biographie"
    )
    photo = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        verbose_name="Photo de profil"
    )
    interests = models.ManyToManyField(
        Interest, 
        blank=True,
        related_name='profiles',
        verbose_name="Centres d'intérêt"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def get_interests_set(self):
        """Retourne un set des IDs des centres d'intérêt pour calcul de similarité."""
        return set(self.interests.values_list('id', flat=True))
    
    def calculate_similarity(self, other_profile):
        """
        Calcule la similarité de Jaccard entre deux profils basée sur les intérêts.
        
        Formule: |A ∩ B| / |A ∪ B|
        Retourne un score entre 0 (aucun intérêt commun) et 1 (intérêts identiques).
        """
        my_interests = self.get_interests_set()
        other_interests = other_profile.get_interests_set()
        
        if not my_interests and not other_interests:
            return 0.0
        
        intersection = len(my_interests & other_interests)
        union = len(my_interests | other_interests)
        
        return intersection / union if union > 0 else 0.0


# Signal pour créer automatiquement un profil lors de la création d'un utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil quand un utilisateur est créé."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand l'utilisateur est sauvegardé."""
    instance.profile.save()

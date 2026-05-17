"""
Modèles pour le système d'amitié.

Analyse des Réseaux Sociaux - Master 2
--------------------------------------
Ce module définit les ARÊTES du graphe social.
Chaque amitié acceptée représente une arête non-orientée entre deux noeuds (utilisateurs).

Le graphe social ainsi formé est utilisé pour:
- Recommander des amis via les "amis d'amis" (common neighbors)
- Prioriser les contenus des utilisateurs proches dans le graphe
"""

from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    """
    Représente une relation d'amitié entre deux utilisateurs.
    
    Dans le graphe social:
    - from_user et to_user sont des noeuds
    - Une Friendship avec status='accepted' représente une ARÊTE
    
    Le système gère les demandes d'amitié avec un statut:
    - 'pending': demande envoyée, en attente de réponse
    - 'accepted': amitié confirmée (arête créée)
    - 'rejected': demande refusée
    """
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]
    
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friendships_sent',
        verbose_name="Expéditeur"
    )
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friendships_received',
        verbose_name="Destinataire"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Amitié"
        verbose_name_plural = "Amitiés"
        # Empêche les demandes d'amitié en double
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.get_status_display()})"
    
    def accept(self):
        """Accepte la demande d'amitié."""
        self.status = 'accepted'
        self.save()
    
    def reject(self):
        """Refuse la demande d'amitié."""
        self.status = 'rejected'
        self.save()
    
    @classmethod
    def are_friends(cls, user1, user2):
        """
        Vérifie si deux utilisateurs sont amis.
        
        Une amitié est bidirectionnelle si l'une des deux directions
        a un statut 'accepted'.
        """
        return cls.objects.filter(
            models.Q(from_user=user1, to_user=user2, status='accepted') |
            models.Q(from_user=user2, to_user=user1, status='accepted')
        ).exists()
    
    @classmethod
    def get_friends(cls, user):
        """
        Retourne la liste des amis d'un utilisateur.
        
        Correspond aux VOISINS DIRECTS dans le graphe social.
        """
        # Amitiés où l'utilisateur est l'expéditeur
        sent_accepted = cls.objects.filter(
            from_user=user, 
            status='accepted'
        ).values_list('to_user', flat=True)
        
        # Amitiés où l'utilisateur est le destinataire
        received_accepted = cls.objects.filter(
            to_user=user, 
            status='accepted'
        ).values_list('from_user', flat=True)
        
        # Union des deux ensembles
        friend_ids = set(sent_accepted) | set(received_accepted)
        return User.objects.filter(id__in=friend_ids)
    
    @classmethod
    def get_friends_of_friends(cls, user):
        """
        Retourne les amis des amis d'un utilisateur.
        
        Correspond aux VOISINS À DISTANCE 2 dans le graphe social.
        Ces utilisateurs sont les candidats potentiels pour les recommandations d'amis.
        """
        friends = cls.get_friends(user)
        friends_of_friends = set()
        
        for friend in friends:
            fof = cls.get_friends(friend)
            for f in fof:
                # Exclure l'utilisateur lui-même et ses amis actuels
                if f.id != user.id and f not in friends:
                    friends_of_friends.add(f)
        
        return list(friends_of_friends)
    
    @classmethod
    def count_common_friends(cls, user1, user2):
        """
        Compte le nombre d'amis en commun entre deux utilisateurs.
        
        C'est la métrique "Common Neighbors" utilisée pour prédire
        la probabilité de formation d'une nouvelle arête dans le graphe.
        """
        friends1 = set(cls.get_friends(user1).values_list('id', flat=True))
        friends2 = set(cls.get_friends(user2).values_list('id', flat=True))
        return len(friends1 & friends2)
    
    @classmethod
    def has_pending_request(cls, from_user, to_user):
        """Vérifie s'il y a une demande d'amitié en attente."""
        return cls.objects.filter(
            from_user=from_user, 
            to_user=to_user, 
            status='pending'
        ).exists()

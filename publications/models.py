"""
Modèles pour les publications (posts), likes et commentaires.

Analyse des Réseaux Sociaux - Master 2
--------------------------------------
Ce module gère les interactions sociales sur le réseau.
Les likes sont utilisés pour construire le profil d'intérêt de l'utilisateur
et alimenter le système de recommandation de contenus.
"""

from django.db import models
from django.contrib.auth.models import User
from comptes.models import Interest


class Post(models.Model):
    """
    Représente une publication créée par un utilisateur.
    
    Les posts peuvent être tagués avec des centres d'intérêt,
    ce qui permet de recommander des contenus similaires aux utilisateurs.
    """
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name="Auteur"
    )
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(
        upload_to='posts/', 
        blank=True, 
        null=True,
        verbose_name="Image"
    )
    interests = models.ManyToManyField(
        Interest, 
        blank=True,
        related_name='posts',
        verbose_name="Tags/Intérêts",
        help_text="Catégorisez votre post pour améliorer les recommandations"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-created_at']  # Posts les plus récents en premier
    
    def __str__(self):
        return f"Post de {self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_likes_count(self):
        """Retourne le nombre de likes sur ce post."""
        return self.likes.count()
    
    def get_comments_count(self):
        """Retourne le nombre de commentaires sur ce post."""
        return self.comments.count()
    
    def is_liked_by(self, user):
        """Vérifie si un utilisateur a liké ce post."""
        return self.likes.filter(user=user).exists()


class Like(models.Model):
    """
    Représente un like sur un post.
    
    Les likes sont essentiels pour le système de recommandation:
    - Ils révèlent les préférences implicites de l'utilisateur
    - Ils permettent de déduire les centres d'intérêt dominants
    - Ils influencent la popularité des posts (score de recommandation)
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name="Utilisateur"
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name="Publication"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date du like")
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        # Un utilisateur ne peut liker un post qu'une seule fois
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} aime {self.post}"


class Comment(models.Model):
    """
    Représente un commentaire sur un post.
    """
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Auteur"
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Publication"
    )
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['created_at']  # Commentaires chronologiques
    
    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.post}"

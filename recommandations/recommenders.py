"""
Algorithmes de recommandation pour le réseau social.

Analyse des Réseaux Sociaux - Master 2
--------------------------------------
Ce module contient les classes de recommandation basées sur:
1. La structure du graphe social (common neighbors)
2. La similarité des profils (centres d'intérêt communs)
3. Les interactions utilisateur (likes)

Concepts clés de la théorie des graphes utilisés:
- Common Neighbors: nombre de voisins communs entre deux noeuds
- Jaccard Similarity: |A ∩ B| / |A ∪ B| pour les ensembles d'intérêts
- Distance dans le graphe: les amis d'amis sont à distance 2
"""

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class FriendRecommender:
    """
    Système de recommandation d'amis basé sur le graphe social.
    
    Métriques utilisées:
    1. Common Neighbors: Plus deux utilisateurs ont d'amis en commun,
       plus il est probable qu'ils deviennent amis (triadic closure).
    2. Interest Similarity: Similarité de Jaccard basée sur les centres d'intérêt.
    
    Score final = α × common_neighbors_normalized + β × interest_similarity
    où α = 0.6 et β = 0.4 (pondération ajustable)
    """
    
    def __init__(self, alpha=0.6, beta=0.4):
        """
        Initialise le recommandeur avec les poids des métriques.
        
        Args:
            alpha: Poids du score "common neighbors" (0-1)
            beta: Poids du score "interest similarity" (0-1)
        """
        self.alpha = alpha
        self.beta = beta
    
    def get_recommendations(self, user, limit=10):
        """
        Génère des recommandations d'amis pour un utilisateur.
        
        Algorithme:
        1. Récupérer les amis de l'utilisateur (voisins directs, distance 1)
        2. Pour chaque ami, récupérer leurs amis (distance 2)
        3. Filtrer: exclure l'utilisateur et ses amis actuels
        4. Calculer le score pour chaque candidat
        5. Trier par score décroissant
        
        Returns:
            Liste de tuples (user, score, common_friends_count, similarity)
        """
        from amis.models import Friendship
        
        # Récupérer les amis actuels de l'utilisateur
        current_friends = set(Friendship.get_friends(user).values_list('id', flat=True))
        current_friends.add(user.id)  # Exclure l'utilisateur lui-même
        
        # Récupérer les demandes d'amitié en cours (pour ne pas les recommander)
        pending_sent = set(Friendship.objects.filter(
            from_user=user, status='pending'
        ).values_list('to_user_id', flat=True))
        
        pending_received = set(Friendship.objects.filter(
            to_user=user, status='pending'
        ).values_list('from_user_id', flat=True))
        
        excluded = current_friends | pending_sent | pending_received
        
        # Récupérer les amis d'amis (candidats potentiels)
        candidates = Friendship.get_friends_of_friends(user)
        
        # Calculer les scores pour chaque candidat
        recommendations = []
        max_common = 1  # Pour éviter division par zéro
        
        # Première passe: calculer le max pour normalisation
        for candidate in candidates:
            if candidate.id in excluded:
                continue
            common_count = Friendship.count_common_friends(user, candidate)
            if common_count > max_common:
                max_common = common_count
        
        # Deuxième passe: calculer les scores normalisés
        for candidate in candidates:
            if candidate.id in excluded:
                continue
            
            # Métrique 1: Common Neighbors (normalisé)
            common_count = Friendship.count_common_friends(user, candidate)
            common_score = common_count / max_common if max_common > 0 else 0
            
            # Métrique 2: Similarité des intérêts
            try:
                interest_similarity = user.profile.calculate_similarity(candidate.profile)
            except:
                interest_similarity = 0.0
            
            # Score combiné
            final_score = (self.alpha * common_score) + (self.beta * interest_similarity)
            
            recommendations.append({
                'user': candidate,
                'score': round(final_score, 3),
                'common_friends_count': common_count,
                'interest_similarity': round(interest_similarity, 3)
            })
        
        # Trier par score décroissant
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]
    
    def get_recommendations_simple(self, user, limit=10):
        """
        Version simplifiée pour les utilisateurs sans beaucoup d'amis.
        Recommande des utilisateurs avec des intérêts similaires.
        """
        from amis.models import Friendship
        
        # Exclure l'utilisateur et ses amis
        current_friends = set(Friendship.get_friends(user).values_list('id', flat=True))
        current_friends.add(user.id)
        
        # Récupérer tous les autres utilisateurs
        candidates = User.objects.exclude(id__in=current_friends)
        
        recommendations = []
        for candidate in candidates:
            try:
                similarity = user.profile.calculate_similarity(candidate.profile)
                if similarity > 0:
                    recommendations.append({
                        'user': candidate,
                        'score': round(similarity, 3),
                        'common_friends_count': 0,
                        'interest_similarity': round(similarity, 3)
                    })
            except:
                continue
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]


class ContentRecommender:
    """
    Système de recommandation de contenus (posts) basé sur:
    1. Les posts likés par l'utilisateur (préférences implicites)
    2. Les centres d'intérêt du profil (préférences explicites)
    3. La popularité des posts (nombre de likes)
    4. La fraîcheur (posts récents)
    
    Score = w1 × interest_match + w2 × popularity + w3 × recency + w4 × social_proximity
    """
    
    def __init__(self, interest_weight=0.4, popularity_weight=0.2, 
                 recency_weight=0.2, social_weight=0.2):
        self.interest_weight = interest_weight
        self.popularity_weight = popularity_weight
        self.recency_weight = recency_weight
        self.social_weight = social_weight
    
    def get_user_interest_profile(self, user):
        """
        Construit le profil d'intérêt de l'utilisateur basé sur:
        1. Les centres d'intérêt déclarés dans le profil
        2. Les intérêts des posts likés
        
        Retourne un dict {interest_id: weight}
        """
        from publications.models import Like
        
        interest_weights = {}
        
        # Intérêts déclarés (poids de base = 1.0)
        try:
            for interest in user.profile.interests.all():
                interest_weights[interest.id] = 1.0
        except:
            pass
        
        # Intérêts des posts likés (accumulation des poids)
        liked_posts = Like.objects.filter(user=user).select_related('post')
        for like in liked_posts:
            for interest in like.post.interests.all():
                interest_weights[interest.id] = interest_weights.get(interest.id, 0) + 0.5
        
        return interest_weights
    
    def get_recommendations(self, user, limit=20, days_back=30):
        """
        Génère des recommandations de posts pour un utilisateur.
        
        Algorithme:
        1. Construire le profil d'intérêt de l'utilisateur
        2. Récupérer les posts récents non likés par l'utilisateur
        3. Calculer le score pour chaque post
        4. Trier par score décroissant
        
        Returns:
            Liste de posts avec leurs scores
        """
        from publications.models import Post, Like
        from amis.models import Friendship
        
        # Construire le profil d'intérêt
        user_interests = self.get_user_interest_profile(user)
        
        # Récupérer les IDs des posts déjà likés
        liked_post_ids = set(Like.objects.filter(user=user).values_list('post_id', flat=True))
        
        # Récupérer les amis et amis d'amis
        friends = set(Friendship.get_friends(user).values_list('id', flat=True))
        friends_of_friends = set(f.id for f in Friendship.get_friends_of_friends(user))
        
        # Récupérer les posts récents (excluant ceux de l'utilisateur et déjà likés)
        cutoff_date = timezone.now() - timedelta(days=days_back)
        posts = Post.objects.filter(
            created_at__gte=cutoff_date
        ).exclude(
            author=user
        ).exclude(
            id__in=liked_post_ids
        ).annotate(
            likes_count=Count('likes')
        ).prefetch_related('interests', 'author')
        
        # Calculer les scores
        recommendations = []
        max_likes = max([p.likes_count for p in posts], default=1)
        now = timezone.now()
        
        for post in posts:
            # Score d'intérêt
            post_interests = set(post.interests.values_list('id', flat=True))
            if user_interests and post_interests:
                interest_score = sum(
                    user_interests.get(i, 0) for i in post_interests
                ) / len(post_interests)
                # Normaliser
                max_weight = max(user_interests.values()) if user_interests else 1
                interest_score = min(interest_score / max_weight, 1.0)
            else:
                interest_score = 0.0
            
            # Score de popularité (normalisé)
            popularity_score = post.likes_count / max_likes if max_likes > 0 else 0
            
            # Score de fraîcheur (decay exponentiel)
            age_hours = (now - post.created_at).total_seconds() / 3600
            recency_score = max(0, 1 - (age_hours / (days_back * 24)))
            
            # Score de proximité sociale
            if post.author.id in friends:
                social_score = 1.0
            elif post.author.id in friends_of_friends:
                social_score = 0.5
            else:
                social_score = 0.1
            
            # Score final
            final_score = (
                self.interest_weight * interest_score +
                self.popularity_weight * popularity_score +
                self.recency_weight * recency_score +
                self.social_weight * social_score
            )
            
            recommendations.append({
                'post': post,
                'score': round(final_score, 3),
                'interest_score': round(interest_score, 3),
                'popularity_score': round(popularity_score, 3),
                'recency_score': round(recency_score, 3),
                'social_score': round(social_score, 3)
            })
        
        # Trier par score décroissant
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]

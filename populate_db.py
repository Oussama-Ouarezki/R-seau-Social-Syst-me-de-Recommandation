
import os
import django
import sys
import random

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reseau_social.settings')
django.setup()

from django.contrib.auth.models import User
from comptes.models import Profile, Interest
from publications.models import Post, Like, Comment
from amis.models import Friendship

# --- CONFIGURATION ---
# Utilisateurs de démonstration (Membres du groupe)
SPECIFIC_USERS = [
    {"first_name": "Mohamed", "last_name": "Benabdous", "username": "m.ben", "bio": "Développeur Backend & Architecture."},
    {"first_name": "Sadek", "last_name": "Chettouh", "username": "s.chettouh", "bio": "Spécialiste Frontend & UI/UX."},
    {"first_name": "Oussama", "last_name": "Ouarezki", "username": "o.ouarezki", "bio": "Passionné par l'IA et le développement Web."},
    {"first_name": "Youcef", "last_name": "Mechkak", "username": "y.mechkak", "bio": "Expert en réseaux et sécurité informatique."}
]

NB_RANDOM_USERS = 8
NB_POSTS = 30
NB_LIKES = 120

# Données fictives (Fallback sans Faker)
FIRST_NAMES = ["Amine", "Sarah", "Yasmine", "Karim", "Lina", "Walid", "Rania", "Ahmed", "Sofia", "Bilal"]
LAST_NAMES = ["Benali", "Saidi", "Dahmane", "Mansouri", "Abdi", "Cherif", "Hamdi", "Belkacem"]
BIOS = [
    "Étudiant en informatique.", "Développeur Full Stack.", "Amateur de photographie et d'art.", 
    "Fan de football et de sport.", "Passionné par les technologies.", "J'aime voyager et découvrir le monde.",
    "Musique et Cinéma avant tout.", "Geek et fier de l'être.", "Architecture et Design."
]
POST_CONTENTS = [
    "Je viens de terminer mon projet Django ! Trop content.",
    "Quelqu'un a vu le dernier match hier soir ? Incroyable performance !",
    "La nouvelle mise à jour de Python est vraiment super.",
    "Je cherche des recommandations pour un bon livre sur le Machine Learning.",
    "Superbe journée pour coder en terrasse ☀️",
    "Est-ce que vous préférez React ou Vue.js ? Le débat est ouvert.",
    "J'ai enfin réussi à configurer mon serveur Linux !",
    "Besoin de vacances... qui a des idées de destination ?",
    "L'intelligence artificielle avance à une vitesse folle.",
    "Déjeuner avec l'équipe aujourd'hui, c'était top !",
    "Le café, c'est la vie d'un développeur. ☕"
]

def run_population():
    print("--- Démarrage du script de peuplement (Demo Data) ---")

    # 1. Intérêts (Initialisation)
    INTERESTS_LIST = ["Sport", "Musique", "Cinéma", "Voyage", "Lecture", "Technologie", "Cuisine", "Jeux Vidéo", "Art", "Science"]
    print(f"Création de {len(INTERESTS_LIST)} centres d'intérêt...")
    db_interests = []
    for name in INTERESTS_LIST:
        obj, created = Interest.objects.get_or_create(name=name)
        db_interests.append(obj)

    # 2. Utilisateurs Spécifiques
    print("Création des membres du groupe...")
    all_users = []
    for u_data in SPECIFIC_USERS:
        if not User.objects.filter(username=u_data['username']).exists():
            u = User.objects.create_user(username=u_data['username'], password="password123", first_name=u_data['first_name'], last_name=u_data['last_name'])
            u.profile.bio = u_data['bio']
            u.profile.save()
            # Assign Random Interests
            u.profile.interests.set(random.sample(db_interests, k=random.randint(3, 5)))
            print(f" -> Créé: {u.username}")
        else:
            u = User.objects.get(username=u_data['username'])
            print(f" -> Existant: {u.username}")
        all_users.append(u)

    # 3. Utilisateurs Aléatoires
    print(f"Création de {NB_RANDOM_USERS} utilisateurs aléatoires...")
    for _ in range(NB_RANDOM_USERS):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        username = f"{fname.lower()}.{lname.lower()}{random.randint(1,99)}"
        
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(username=username, password="password123", first_name=fname, last_name=lname)
            u.profile.bio = random.choice(BIOS)
            u.profile.save()
            u.profile.interests.set(random.sample(db_interests, k=random.randint(2, 4)))
            all_users.append(u)

    # 4. Amitiés (Graph Generation)
    print("Génération du graphe social (Amitiés)...")
    for user in all_users:
        # Chaque user ajoute 2-4 amis au hasard
        targets = random.sample(all_users, k=min(len(all_users), 4))
        for target in targets:
            if user != target:
                # Créer une amitié connectée
                if not Friendship.are_friends(user, target):
                    Friendship.objects.get_or_create(from_user=user, to_user=target, status='accepted')

    # 5. Posts
    print(f"Création de {NB_POSTS} posts...")
    all_posts = []
    for _ in range(NB_POSTS):
        author = random.choice(all_users)
        content = random.choice(POST_CONTENTS)
        post = Post.objects.create(author=author, content=content)
        # Tag avec un intérêt
        post.interests.add(random.choice(db_interests))
        all_posts.append(post)

    # 6. Likes
    print(f"Génération de {NB_LIKES} likes pour l'algo de recommandation...")
    for _ in range(NB_LIKES):
        user = random.choice(all_users)
        post = random.choice(all_posts)
        Like.objects.get_or_create(user=user, post=post)

    print("\n--- TERMINE ! ---")
    print("La base de données est prête.")
    print("Comptes Groupe : password123")

if __name__ == "__main__":
    run_population()

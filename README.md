# Réseau Social avec Système de Recommandation (Django)

Ce projet est une application de réseau social développée avec Django dans le cadre d'un module académique "Analyse des Réseaux Sociaux". Il implémente des fonctionnalités sociales classiques (posts, amis, likes) et intègre un moteur de recommandation basé sur la théorie des graphes.

## 🚀 Fonctionnalités

### 👤 Utilisateurs & Profils (App: `comptes`)
*   Inscription et Authentification sécurisée
*   Profils personnalisables (Photo, Bio, Centres d'intérêt)
*   Système d'intérêts (Tags) pour le matching

### 📰 Fil d'Actualité (App: `publications`)
*   Publication de Posts (Texte + Image)
*   Système de Like asynchrone (AJAX)
*   Commentaires interactifs (Modal)
*   Affichage "riche" avec cartes modernes

### 🤝 Réseau Social (App: `amis`)
*   Gestion des demandes d'amis (Envoyer, Accepter, Refuser)
*   Modèle de graphe non-orienté
*   Liste d'amis dynamique

### 🧠 Recommandations Intelligentes (App: `recommandations`)
Deux algorithmes distincts implémentés :
1.  **Recommandation d'Amis (Link Prediction)** :
    *   Basée sur les **Voisins Communs** (Common Neighbors) dans le graphe social.
    *   Pondérée par la similarité des centres d'intérêt (Coefficient de Jaccard).
2.  **Recommandation de Contenu** :
    *   Basée sur les préférences implicites (Likes précédents) et explicites (Intérêts du profil).
    *   Score hybride incluant : Popularité, Récence, et Proximité sociale.

## 🛠️ Stack Technique

*   **Backend** : Python 3, Django 5.x
*   **Frontend** : HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
*   **Base de données** : SQLite (Dev)
*   **Algorithmes** : Implémentation custom en Python (Graph Theory)

## 📦 Installation

1.  Cloner le repo :
    ```bash
    git clone https://github.com/votre-username/reseau-social-django.git
    ```
2.  Installer les dépendances :
    ```bash
    pip install django pillow
    ```
3.  Lancer les migrations :
    ```bash
    python manage.py migrate
    ```
4.  **(Optionnel) Peupler la base de données avec des données de test** :
    ```bash
    python populate_db.py
    ```
5.  Lancer le serveur :
    ```bash
    python manage.py runserver
    ```

[Full Documentation]([(https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation/blob/main/RAPPORT-DE-PROJET-_-R%C3%89SEAU-SOCIAL-SYST%C3%88MES-DE-RECOMMANDATION.pdf.pdf)])

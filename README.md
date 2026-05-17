# Analyse des Réseaux Sociaux — Projets M1 ASD

> Deux projets réalisés dans le cadre du module **Analyse des Réseaux Sociaux (ARS)**, M1 ASD — Université d'Alger 1 – Benyoucef Benkhedda, 2024/2025.


---

## Table des matières

- [ARS 1 — Analyse du Réseau Karate Club](#ars-1--analyse-du-réseau-karate-club)
- [Réseau Social avec Système de Recommandation (Django)](#réseau-social-avec-système-de-recommandation-django)

---

# ARS 1 — Analyse du Réseau Karate Club

Le réseau Karate Club de Zachary est un jeu de données classique en analyse des réseaux sociaux : 34 membres d'un club de sport, 75 relations d'amitié. Ce mini-projet analyse sa structure à travers les outils fondamentaux de la théorie des graphes et montre comment des métriques mathématiques révèlent des dynamiques sociales concrètes.

- **Centralité de degré** → les membres les plus connectés (nœuds 0 et 33) correspondent aux deux leaders réels du club : l'instructeur et le président.
- **Betweenness centrality** → identifie les ponts entre groupes — les membres dont la suppression isolerait des sous-communautés entières.
- **Coefficient de clustering (0.573)** → les membres forment des cercles d'amis soudés, reflétant la structure typique des groupes d'intérêt sur tout réseau social.
- **k-core = 4** → un noyau dense d'utilisateurs hyper-connectés autour duquel gravitent des membres plus périphériques.
- **Bridge nodes** → leur identification a permis de prédire la scission historique du club en deux factions.

![Graphe du réseau Karate Club](https://github.com/user-attachments/assets/5aa71362-4417-4048-9330-8cfa559d814d)

*Structure du réseau — les nœuds 0 et 33 apparaissent naturellement comme les hubs centraux.*

![Centralité des nœuds principaux](https://github.com/user-attachments/assets/5c5d5e1f-aa97-4247-ab15-087d059ee227)

*Comparaison des quatre mesures de centralité (degré, betweenness, closeness, eigenvector) pour les nœuds les plus influents.*

▶️ [Video explicative dans youtube](https://youtu.be/ZE2fBwU4ajM)  
📄 [Rapport Complet](https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation/blob/main/ARS%201/Report.pdf)

---

# Réseau Social avec Système de Recommandation (Django)

Application de réseau social développée avec Django dans le cadre du module "Analyse des Réseaux Sociaux". Elle implémente des fonctionnalités sociales classiques (posts, amis, likes) et intègre un moteur de recommandation basé sur la théorie des graphes.

![Page d'inscription](https://github.com/user-attachments/assets/a3966a33-accd-4293-b6f8-c615b16a6f5d)

*Page d'inscription*

![Interface principale](https://github.com/user-attachments/assets/545a4894-fb51-4b14-a62e-2e192f049404)

*Interface principale*

![Système de suggestions](https://github.com/user-attachments/assets/5c5d5e1f-aa97-4247-ab15-087d059ee227)

*Système de recommandations d'amis*

![Structure du projet Django](https://github.com/user-attachments/assets/36b3b174-8edc-4dd3-bc33-6c4df869942c)

*Structure du projet Django*

## 🚀 Fonctionnalités

### 👤 Utilisateurs & Profils — app `comptes`
- Inscription et authentification sécurisée
- Profils personnalisables (photo, bio, centres d'intérêt)
- Système d'intérêts (tags) pour le matching

### 📰 Fil d'Actualité — app `publications`
- Publication de posts (texte + image)
- Système de like asynchrone (AJAX)
- Commentaires interactifs (modal)
- Affichage riche avec cartes modernes

### 🤝 Réseau Social — app `amis`
- Gestion des demandes d'amis (envoyer, accepter, refuser)
- Modèle de graphe non-orienté
- Liste d'amis dynamique

### 🧠 Recommandations Intelligentes — app `recommandations`

Deux algorithmes distincts implémentés :

1. **Recommandation d'amis (Link Prediction)**
   - Basée sur les **voisins communs** (Common Neighbors) dans le graphe social
   - Pondérée par la similarité des centres d'intérêt (coefficient de Jaccard)

2. **Recommandation de contenu**
   - Basée sur les préférences implicites (likes précédents) et explicites (intérêts du profil)
   - Score hybride : popularité + récence + proximité sociale

## 🛠️ Stack Technique

- **Backend** : Python 3, Django 5.x
- **Frontend** : HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
- **Base de données** : SQLite (dev)
- **Algorithmes** : Implémentation custom Python (Graph Theory)

## 📦 Installation

1. Cloner le repo :
   ```bash
   git clone https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation.git
   ```

2. Installer les dépendances :
   ```bash
   pip install django pillow
   ```

3. Lancer les migrations :
   ```bash
   python manage.py migrate
   ```

4. **(Optionnel) Peupler la base de données avec des données de test** :
   ```bash
   python populate_db.py
   ```

5. Lancer le serveur :
   ```bash
   python manage.py runserver
   ```

📄 [Documentation complète (PDF)](https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation/blob/main/RAPPORT-DE-PROJET-_-R%C3%89SEAU-SOCIAL-SYST%C3%88MES-DE-RECOMMANDATION.pdf.pdf)

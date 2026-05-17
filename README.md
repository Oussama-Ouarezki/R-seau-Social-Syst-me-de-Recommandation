# Analyse des Réseaux Sociaux — Projets M1 ASD

> Deux projets réalisés dans le cadre du module **Analyse des Réseaux Sociaux (ARS)**, M1 ASD — Université d'Alger 1 – Benyoucef Benkhedda, 2024/2025.

**OUAREZKI Oussama Abderahim** — Groupe 03

---

## Table des matières

- [Projet 1 — Analyse du Réseau Karate Club](#projet-1--analyse-du-réseau-karate-club)
- [Projet 2 — Réseau Social avec Système de Recommandation (Django)](#projet-2--réseau-social-avec-système-de-recommandation-django)

---

# Projet 1 — Analyse du Réseau Karate Club

Le réseau Karate Club de Zachary est un jeu de données classique en analyse des réseaux sociaux : 34 membres d'un club de sport, 75 relations d'amitié. Simple en apparence, il illustre des phénomènes que l'on retrouve dans tout réseau social réel.

Ce mini-projet analyse sa structure à travers les outils fondamentaux de la théorie des graphes et montre comment des métriques mathématiques révèlent des dynamiques sociales concrètes.

### Ce que les chiffres révèlent

- **Centralité de degré élevée (nœuds 0 et 33)** → les membres les plus connectés correspondent exactement aux deux leaders réels du club : l'instructeur et le président. Sur un réseau social en ligne, ce sont les influenceurs ou animateurs de communauté.

- **Betweenness centrality** → les nœuds qui servent de pont entre groupes contrôlent le flux d'information. Leur suppression isolerait des sous-communautés entières — un mécanisme directement lié à la détection de communautés et à la vulnérabilité des réseaux.

- **Coefficient de clustering moyen (0.573)** → les membres forment des cercles d'amis soudés, avec 44 triangles et une clique maximale de 5 personnes. C'est la structure typique des groupes d'intérêt sur toute plateforme sociale.

- **k-core maximum = 4** → il existe un noyau dense d'utilisateurs hyper-connectés autour duquel gravitent des membres plus périphériques — la colonne vertébrale de toute communauté en ligne active.

- **Bridge nodes `{0, 1, 2, 5, 6, 8, 9, 13, 16, 19, 27, 28, 30, 31, 32, 33}`** → ces membres maintiennent la cohésion entre les deux factions. Leur identification a permis de prédire la scission historique du club.

### Visualisations

![Graphe du réseau Karate Club](https://github.com/user-attachments/assets/5aa71362-4417-4048-9330-8cfa559d814d)

*Structure du réseau — les deux leaders (nœuds 0 et 33) apparaissent naturellement comme les hubs centraux.*

![Centralité des nœuds principaux](https://github.com/user-attachments/assets/5c5d5e1f-aa97-4247-ab15-087d059ee227)

*Comparaison des quatre mesures de centralité — degré, betweenness, closeness, eigenvector.*

### Démo & Documentation

▶️ [Voir la démo sur YouTube](https://youtu.be/ZE2fBwU4ajM)  
📄 [Rapport complet (PDF)](https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation/blob/main/ARS%201/Report.pdf)

---

# Projet 2 — Réseau Social avec Système de Recommandation (Django)

Application web de réseau social fonctionnel développée avec Django. Chaque utilisateur est un nœud, chaque amitié une arête — et le moteur de recommandation exploite la structure du graphe social pour suggérer des amis et du contenu pertinent.

### Aperçu

| | |
|---|---|
| ![Inscription](https://github.com/user-attachments/assets/a3966a33-accd-4293-b6f8-c615b16a6f5d) | ![Interface principale](https://github.com/user-attachments/assets/545a4894-fb51-4b14-a62e-2e192f049404) |
| *Page d'inscription* | *Interface principale* |
| ![Suggestions](https://github.com/user-attachments/assets/5c5d5e1f-aa97-4247-ab15-087d059ee227) | ![Structure Django](https://github.com/user-attachments/assets/36b3b174-8edc-4dd3-bc33-6c4df869942c) |
| *Système de recommandations* | *Structure du projet Django* |

### Fonctionnalités

**👤 Utilisateurs & Profils** — app `comptes`
- Inscription et authentification sécurisée
- Profils personnalisables (photo, bio, centres d'intérêt)
- Système de tags pour le matching entre utilisateurs

**📰 Fil d'Actualité** — app `publications`
- Publication de posts (texte + image)
- Système de like asynchrone (AJAX)
- Commentaires interactifs via modal

**🤝 Réseau Social** — app `amis`
- Gestion des demandes d'amis (envoyer, accepter, refuser)
- Modèle de graphe non-orienté
- Liste d'amis dynamique

**🧠 Recommandations Intelligentes** — app `recommandations`

| Algorithme | Description |
|---|---|
| Recommandation d'amis | Voisins communs (Common Neighbors) + similarité Jaccard sur les centres d'intérêt |
| Recommandation de contenu | Score hybride : popularité + récence + proximité sociale |

### Stack Technique

| Couche | Technologie |
|---|---|
| Backend | Python 3, Django 5.x |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API) |
| Base de données | SQLite (dev) |
| Algorithmes | Implémentation custom Python (Graph Theory) |

### Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation.git
cd R-seau-Social-Syst-me-de-Recommandation

# 2. Installer les dépendances
pip install django pillow

# 3. Appliquer les migrations
python manage.py migrate

# 4. (Optionnel) Peupler la base avec des données de test
python populate_db.py

# 5. Lancer le serveur
python manage.py runserver
```

### Documentation

📄 [Rapport complet du projet (PDF)](https://github.com/Oussama-Ouarezki/R-seau-Social-Syst-me-de-Recommandation/blob/main/RAPPORT-DE-PROJET-_-R%C3%89SEAU-SOCIAL-SYST%C3%88MES-DE-RECOMMANDATION.pdf.pdf)

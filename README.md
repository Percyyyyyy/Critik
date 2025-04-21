
# Critik - Plateforme de Critiques de Restaurants

## Description

**Critik** est un projet Django développé dans le cadre de mes cours de PIW (Projet d'Intégration Web). L'objectif était de synthétiser l’ensemble des compétences acquises (modèles, vues, templates, formulaires, administration, logs, etc.) à travers un site de notation de restaurants.

Depuis la version initiale, j’ai repris ce projet pour l’améliorer, corriger des bugs, ajouter de nouvelles fonctionnalités (comme les logs d’administration ou le CAPTCHA à l’inscription), et l’amener à un niveau plus propre.

Le projet n’est pas encore totalement abouti, mais il est disponible publiquement car il représente mon niveau sur Django jusqu’ici. Je le mets de côté pour le moment, mais j’y reviendrai à mon rythme, quand j’en aurai envie ou pour tester de nouvelles choses.


## Fonctionnalités

- **Mode Utilisateur :**
  - Poster des commentaires sur les restaurants.
  - Lire les critiques laissées par les autres utilisateurs.
  - Noter les restaurants sur une échelle de 1 à 5 étoiles.
  
- **Mode Administrateur :**
  - Ajouter, modifier ou supprimer des restaurants.
  - Gérer les utilisateurs et les commentaires.
  - Accéder à un système de logs pour suivre les actions sur la plateforme.

## Installation

### 1. Cloner le projet
Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/Percyyyyyy/Critik.git
```

### 2. Créer un environnement virtuel
Créez un environnement virtuel pour installer les dépendances :

```bash
python -m venv env
source env/bin/activate  # Sous Windows : env\Scripts\activate
```

### 3. Installer les dépendances
Installez les dépendances du projet en utilisant `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
Appliquez les migrations de la base de données :

```bash
python manage.py migrate
```

### 5. Créer un superutilisateur
Si vous souhaitez accéder à l'interface d'administration, créez un superutilisateur :

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement
Démarrez le serveur de développement :

```bash
python manage.py runserver
```

Vous pouvez maintenant accéder au projet à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Technologies utilisées

- **Backend :**
  - Django 5.0.1
  - SQLite
  
- **Front-end :**
  - HTML/CSS
  - Bootstrap 5
  
- **Autres dépendances :**
  - `django-simple-captcha` (Pour la protection contre les bots)
  - `django-widget-tweaks` (Pour personnaliser les widgets de formulaire)
  - `pillow` (Pour la gestion des images)

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.


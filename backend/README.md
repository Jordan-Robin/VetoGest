# VetoGest — Backend

API REST pour la gestion de clinique vétérinaire, construite avec Django 6 et Django REST Framework.

## Stack

- Python 3.12+
- Django 6
- Django REST Framework
- PostgreSQL 16
- JWT (SimpleJWT)
- drf-spectacular (Swagger/OpenAPI)
- djangorestframework-camel-case (conversion snake_case ↔ camelCase)
- Poetry (gestion des dépendances)

## Setup local

### Prérequis

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL en cours d'exécution (ou via Docker : `docker compose up db`)

### Installation

```bash
cd backend

# Installer les dépendances (y compris dev)
poetry install --with dev

# Activer l'environnement virtuel
poetry shell
```

### Variables d'environnement

Créer un fichier `backend/.env` avec les clés suivantes :

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://vetogest:your_password@localhost:5432/vetogest
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

| Variable               | Description                                | Exemple                             |
| ---------------------- | ------------------------------------------ | ----------------------------------- |
| `SECRET_KEY`           | Clé secrète Django                         | `django-insecure-xxxx`              |
| `DEBUG`                | Mode debug                                 | `True`                              |
| `DATABASE_URL`         | URL de connexion PostgreSQL                | `postgres://user:pass@host:5432/db` |
| `ALLOWED_HOSTS`        | Hôtes autorisés (séparés par des virgules) | `127.0.0.1,localhost`               |
| `CORS_ALLOWED_ORIGINS` | Origines CORS autorisées                   | `http://localhost:5173`             |

### Base de données

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Lancer le serveur

```bash
python manage.py runserver
```

Le serveur est accessible sur http://localhost:8000.

## Documentation API

La documentation interactive est générée automatiquement via drf-spectacular :

| Ressource      | URL                               |
| -------------- | --------------------------------- |
| Swagger UI     | http://localhost:8000/api/docs/   |
| Schéma OpenAPI | http://localhost:8000/api/schema/ |

### Endpoints principaux

| Méthode | Endpoint              | Description                  |
| ------- | --------------------- | ---------------------------- |
| POST    | `/api/token/`         | Obtenir un token JWT         |
| POST    | `/api/token/refresh/` | Rafraîchir un token JWT      |
| GET     | `/api/users/`         | Lister les utilisateurs      |
| POST    | `/api/users/`         | Créer un utilisateur (admin) |
| GET     | `/api/customers/`     | Lister les clients           |
| POST    | `/api/customers/`     | Créer un client              |
| GET     | `/api/customers/:id/` | Détail d'un client           |
| PATCH   | `/api/customers/:id/` | Modifier un client           |
| DELETE  | `/api/customers/:id/` | Supprimer un client          |

> **Note** : L'API utilise la conversion automatique camelCase ↔ snake_case. Les requêtes et réponses JSON utilisent le format **camelCase**.

### Authentification

L'API utilise JWT (JSON Web Token). Toutes les routes (sauf `/api/token/`) nécessitent un header :

```
Authorization: Bearer <access_token>
```

### Rôles et permissions

| Rôle           | Droits                                                   |
| -------------- | -------------------------------------------------------- |
| `admin`        | Gestion des utilisateurs (CRUD), accès complet           |
| `veterinarian` | Lecture des utilisateurs, gestion des clients            |
| `secretary`    | Lecture des utilisateurs, gestion des clients            |
| `superuser`    | Tous les droits, y compris création/suppression d'admins |

## Tests

```bash
# Lancer tous les tests
pytest

# Lancer les tests avec le détail
pytest -v

# Lancer les tests d'une app spécifique
pytest users/
pytest customers/
```

## Structure du projet

```
backend/
├── config/             → Configuration Django (settings, urls, wsgi)
├── customers/          → App clients (models, views, serializers, tests)
├── users/              → App utilisateurs (models, views, serializers, permissions, tests)
├── manage.py
├── pyproject.toml      → Dépendances (Poetry)
└── pytest.ini          → Configuration pytest
```

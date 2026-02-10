# 🐾 VetoGest

Application web de gestion de clinique vétérinaire. VetoGest permet de gérer les clients, les utilisateurs (vétérinaires, secrétaires, administrateurs) et à terme les animaux, rendez-vous et dossiers médicaux.

## Architecture

Le projet est organisé en deux parties distinctes :

```
VetoGest/
├── backend/    → API REST (Django / DRF)
├── client/     → Interface web (React / TypeScript / Vite)
└── docker-compose.yml
```

- **Backend** : API REST construite avec Django 6 et Django REST Framework, authentification JWT, documentation Swagger.
- **Client** : SPA React avec TypeScript, bundlée par Vite.
- **Base de données** : PostgreSQL 16.

## Technologies

| Couche   | Stack                                                   |
| -------- | ------------------------------------------------------- |
| Backend  | Python 3.12+, Django 6, DRF, SimpleJWT, drf-spectacular |
| Frontend | React 19, TypeScript 5.9, Vite 7, Axios                 |
| BDD      | PostgreSQL 16                                           |
| Infra    | Docker, Docker Compose                                  |
| Tests    | pytest (backend), Vitest (frontend)                     |

## Démarrage rapide (Docker)

**Prérequis** : [Docker](https://docs.docker.com/get-docker/) et [Docker Compose](https://docs.docker.com/compose/install/) installés.

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/Jordan-Robin/VetoGest.git
   cd VetoGest
   ```

2. **Configurer les variables d'environnement**

   Créer les fichiers `.env` nécessaires :

   ```bash
   # .env (racine) — variables PostgreSQL
   POSTGRES_DB=vetogest
   POSTGRES_USER=vetogest
   POSTGRES_PASSWORD=your_password

   # backend/.env — voir backend/README.md pour le détail
   # client/.env  — voir client/README.md pour le détail
   ```

3. **Lancer l'ensemble des services**

   ```bash
   docker compose up --build
   ```

4. **Appliquer les migrations** (dans un autre terminal)

   ```bash
   docker exec -it vetogest-backend python manage.py migrate
   ```

5. **Accéder à l'application**

   | Service        | URL                             |
   | -------------- | ------------------------------- |
   | Frontend       | http://localhost:5173           |
   | API            | http://localhost:8000/api/      |
   | Swagger (docs) | http://localhost:8000/api/docs/ |
   | Admin Django   | http://localhost:8000/admin/    |

## Documentation

- [Backend README](backend/README.md) — setup, API, migrations, tests
- [Client README](client/README.md) — setup, scripts, structure

FROM python:3.12-slim

# Empêche Python de créer des fichiers .pyc et force l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système pour psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer poetry
RUN pip install poetry

# Copier les fichiers de dépendances
COPY pyproject.toml poetry.lock* ./

# Configurer poetry pour ne pas créer de virtualenv (inutile dans Docker)
RUN poetry config virtualenvs.create false

# Installer les dépendances
RUN poetry install --no-interaction --no-ansi --no-root

# Copier le reste du code
COPY . .

# Exposer le port Django
EXPOSE 8000

# Commande par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
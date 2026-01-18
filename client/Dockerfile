FROM node:20-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code
COPY . .

# Exposer le port Vite
EXPOSE 5173

# Commande pour lancer le dev server
CMD ["npm", "run", "dev", "--", "--host"]
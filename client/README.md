# VetoGest — Client

Interface web de l'application VetoGest, construite avec React, TypeScript et Vite.

## Stack

- React 19
- TypeScript 5.9
- Vite 7
- Axios
- Vitest + Testing Library (tests)
- ESLint

## Setup local

### Prérequis

- Node.js 20+
- npm (ou autre gestionnaire de paquets)

### Installation

```bash
cd client

# Installer les dépendances
npm install
```

### Variables d'environnement

Créer un fichier `client/.env` (ou utiliser les fichiers `.env.development` / `.env.production` existants) :

```env
VITE_API_URL=http://localhost:8000
```

| Variable       | Description                  | Exemple                 |
| -------------- | ---------------------------- | ----------------------- |
| `VITE_API_URL` | URL de base de l'API backend | `http://localhost:8000` |

> En développement, les appels `/api/*` sont automatiquement proxyfiés vers le backend via la configuration Vite.

## Scripts disponibles

| Commande          | Description                               |
| ----------------- | ----------------------------------------- |
| `npm run dev`     | Lance le serveur de développement (HMR)   |
| `npm run build`   | Compile TypeScript et build de production |
| `npm run preview` | Prévisualise le build de production       |
| `npm run test`    | Lance les tests avec Vitest               |
| `npm run lint`    | Analyse du code avec ESLint               |

### Développement

```bash
npm run dev
```

L'application est accessible sur http://localhost:5173.

### Tests

```bash
# Lancer les tests en mode watch
npm run test

# Lancer les tests une seule fois
npx vitest run
```

## Structure du projet

```
client/src/
├── components/         → Composants UI réutilisables
│   └── ui/
│       ├── FormField/          → Champ de formulaire générique
│       └── FormFieldError/     → Affichage d'erreur de champ
├── features/           → Modules métier
│   └── customers/
│       ├── components/         → Composants spécifiques aux clients
│       │   └── CreateCustomerForm/
│       ├── services/           → Appels API (customerService)
│       └── utils/              → Validation (customerValidator)
├── services/           → Configuration Axios (api.ts)
├── types/              → Types TypeScript (Customer, etc.)
├── utils/              → Utilitaires partagés (errors.ts)
├── App.tsx             → Composant racine
├── main.tsx            → Point d'entrée
└── setupTests.ts       → Configuration des tests
```

## Alias de chemin

L'alias `@/` est configuré pour pointer vers `src/` :

```typescript
import { FormField } from "@/components/ui/FormField/FormField";
import type { Customer } from "@/types/customer";
```

Cette configuration est définie dans [tsconfig.app.json](tsconfig.app.json) et [vite.config.ts](vite.config.ts).

## Proxy API

En mode développement, toutes les requêtes vers `/api/*` sont automatiquement redirigées vers le backend grâce à la configuration dans [vite.config.ts](vite.config.ts) :

```typescript
proxy: {
  "/api": {
    target: env.VITE_API_URL,
    changeOrigin: true,
  },
},
```

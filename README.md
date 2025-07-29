# 🚀 Scraper API Freelance – Free-Work

Une API FastAPI qui déclenche un scraping quotidien de la plateforme [Free-Work](https://www.free-work.com/fr/tech-it/jobs), stocke les offres dans une base PostgreSQL, et expose les résultats via une API REST.

---

## 📦 Fonctionnalités

- 🔎 Scraping des offres de missions via `Scrapy` à partir d'un mot-clé
- 🧠 Détection des offres déjà existantes pour éviter les doublons
- 🗓️ Historique des scrapes par date et mot-clé (table `scraping_logs`)
- 🌐 API REST pour consulter les offres (`/annonces/`) et lancer un scraping (`/run-scraper/`)
- 💾 Stockage PostgreSQL (local ou distant via Render)
- 📊 Intégration possible avec Metabase, NocoDB, etc.

---

## 🛠️ Stack Technique

- `FastAPI` – API REST
- `Scrapy` – Web scraping
- `PostgreSQL` – Base de données relationnelle
- `Docker` / `Docker Compose` – Conteneurisation
- `Render.com` – Hébergement PostgreSQL ou API
- `NocoDB`, `Metabase` – (optionnel) Visualisation no-code

---

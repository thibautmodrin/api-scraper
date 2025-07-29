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

## 🧱 Structure du projet

```
├── app/
│ ├── main.py # L’API FastAPI (endpoints)
│ ├── scraper.py # Spider Scrapy pour Free-Work
│ ├── database.py # Connexion et logique PostgreSQL
│ ├── Dockerfile # Dockerisation de l’API
├── README.md # Ce fichier
├── .env # Variables d’environnement (DATABASE_URL)
```
---

## ⚙️ Configuration

### 🔐 Variables d’environnement

Créer un fichier `.env` (non versionné) :

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
```

▶️ Lancer en local
1. Cloner le projet
git clone <lien_du_repo>
cd scraper_api

3. Installer les dépendances
pip install -r requirements.txt

5. Lancer l’API
uvicorn main:app --reload


🧪 Endpoints disponibles

Méthode	URL	Description
GET	/annonces/	Récupère toutes les offres en BDD
POST	/run-scraper/?keyword=data%20engineer	Lance le scraping pour un mot-clé donné

🕒 Déclencher automatiquement chaque jour (cron)
Linux crontab -e :
0 9 * * * curl -X POST "https://api-scraper-6js4.onrender.com/run-scraper/?keyword=data%20engineer"

🐳 Docker
Lancer avec Docker
docker build -t scraper-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... scraper-api

🗃️ Base de données (tables attendues)
```
-- Table des offres
CREATE TABLE offres (
  id SERIAL PRIMARY KEY,
  type TEXT,
  titre TEXT,
  entreprise TEXT,
  technos TEXT[],
  duree TEXT,
  salaire TEXT,
  tjm TEXT,
  teletravail TEXT,
  lieu TEXT,
  date_extraction DATE,
  keyword TEXT
);

-- Table des logs de scraping
CREATE TABLE scraping_logs (
  id SERIAL PRIMARY KEY,
  keyword TEXT,
  date DATE
);

```

📈 Visualisation No-code (optionnel)
Tu peux connecter ta base PostgreSQL à :

Metabase

NocoDB

Budibase

📄 Licence
Ce projet est sous licence MIT.

🙌 Auteur
Développé par @burgovida21 — Data Engineer / Freelance / Android Developer.



Souhaites-tu que je te le mette directement dans un fichier `README.md` prêt à télécharger ?

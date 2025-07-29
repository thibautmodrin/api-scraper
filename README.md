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

```bash
├── app/
│   ├── main.py            # L’API FastAPI (endpoints)
│   ├── scraper.py         # Spider Scrapy pour Free-Work
│   ├── database.py        # Connexion et logique PostgreSQL
│   ├── Dockerfile         # Dockerisation de l’API
├── README.md              # Ce fichier
├── .env                   # Variables d’environnement (DATABASE_URL)
```

---

## ⚙️ Configuration

### 🔐 Variables d’environnement

Créer un fichier `.env` :

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
```

---

## ▶️ Lancer en local

1. **Cloner le projet**

```bash
git clone <lien_du_repo>
cd scraper_api
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Lancer l’API**

```bash
uvicorn main:app --reload
```

---

## 🧪 Endpoints disponibles

| Méthode | URL                                                   | Description                              |
|---------|--------------------------------------------------------|------------------------------------------|
| GET     | `/annonces/`                                          | Récupère toutes les offres en BDD        |
| POST    | `/run-scraper/?keyword=data%20engineer`               | Lance le scraping pour un mot-clé donné  |

---

## 🕒 Déclenchement automatique (cron)

Ajoute cette ligne à ton `crontab` (`crontab -e`) pour déclencher tous les jours à 9h :

```bash
0 9 * * * curl -X POST "https://api-scraper-6js4.onrender.com/run-scraper/?keyword=data%20engineer"
```

---

## 🐳 Lancer avec Docker

```bash
docker build -t scraper-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... scraper-api
```

---

## 🗃️ Base de données (tables attendues)

```sql
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

---

## 📈 Visualisation No-code (optionnel)

Tu peux connecter ta base PostgreSQL à des outils comme :

- [Metabase](https://www.metabase.com/)
- [NocoDB](https://www.nocodb.com/)


---

## 📄 Licence

Ce projet est sous licence **MIT**.

---

## 🙌 Auteur

Développé par **[@burgovida21](https://github.com/ton-profil)**  
Data Engineer / Freelance / Android Developer.
```

---

Souhaites-tu que je t’envoie ce contenu dans un fichier `README.md` à télécharger directement ?

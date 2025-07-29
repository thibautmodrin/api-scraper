# init_db.py
import psycopg2
from database import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offres (
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
        date_extraction DATE DEFAULT CURRENT_DATE,
        keyword TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraping_logs (
        id SERIAL PRIMARY KEY,
        keyword TEXT,
        date DATE DEFAULT CURRENT_DATE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables PostgreSQL créées avec succès.")

if __name__ == "__main__":
    init_db()

import os
import psycopg2
from datetime import date

def get_db_connection():
    # Utilise directement la chaîne de connexion DATABASE_URL (format PostgreSQL standard)
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def has_already_scraped_today(keyword: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM scraping_logs WHERE keyword = %s AND date = CURRENT_DATE",
        (keyword,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def log_scraping(keyword: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scraping_logs (keyword, date) VALUES (%s, %s)",
        (keyword, date.today())
    )
    conn.commit()  # ⬅️ Ajoute cette ligne !!
    cursor.close()
    conn.close()


def is_offer_already_exists(titre: str, entreprise: str, lieu: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM offres
        WHERE titre = %s AND entreprise = %s AND lieu = %s
    """, (titre, entreprise, lieu))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def insert_offer(offer: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO offres (type, titre, entreprise, technos, duree, salaire, tjm, teletravail, lieu, date_extraction, keyword)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        offer["type"],
        offer["titre"],
        offer["entreprise"],
        offer["technos"],
        offer["duree"],
        offer["salaire"],
        offer["tjm"],
        offer["teletravail"],
        offer["lieu"],
        offer["date_extraction"],
        offer["keyword"],
    ))
    conn.commit()
    cursor.close()
    conn.close()

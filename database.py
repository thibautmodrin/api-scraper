import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_to_db():
    return psycopg2.connect(DATABASE_URL)

def is_offer_already_exists(titre, entreprise, lieu):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM offres WHERE titre = %s AND entreprise = %s AND lieu = %s
    """, (titre, entreprise, lieu))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    conn.close()
    return exists

def insert_offer(offer):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO offres (type, titre, entreprise, technos, duree, salaire, tjm,
                            teletravail, lieu, date_extraction, keyword)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        offer["type"], offer["titre"], offer["entreprise"], offer["technos"], offer["duree"],
        offer["salaire"], offer["tjm"], offer["teletravail"], offer["lieu"],
        offer["date_extraction"], offer["keyword"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

def log_scraping(keyword):
    conn = connect_to_db()
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute(
        "INSERT INTO scraping_logs (keyword, date_scraped) VALUES (%s, %s)",
        (keyword, today)
    )
    conn.commit()
    cursor.close()
    conn.close()

def has_already_scraped_today(keyword):
    conn = connect_to_db()
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute(
        "SELECT COUNT(*) FROM scraping_logs WHERE keyword = %s AND date_scraped = %s",
        (keyword, today)
    )
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    conn.close()
    return exists

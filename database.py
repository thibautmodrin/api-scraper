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
    conn.commit()
    cursor.close()
    conn.close()

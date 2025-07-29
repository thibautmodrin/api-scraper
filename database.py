import os
import psycopg2
from datetime import date


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


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
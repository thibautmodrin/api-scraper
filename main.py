from fastapi import FastAPI, HTTPException
from database import get_db_connection, has_already_scraped_today, log_scraping
from scrapy.crawler import CrawlerProcess
from scraper import FreeWorkSpider
from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.get("/annonces/")
def get_all_annonces():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM offres ORDER BY date_extraction DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.post("/run-scraper/")
def run_scraper(keyword: str):
    if has_already_scraped_today(keyword):
        raise HTTPException(status_code=400, detail="Scraping déjà effectué aujourd'hui")

    try:
        process = CrawlerProcess(
            settings={
                "LOG_LEVEL": "DEBUG",
                "TELNETCONSOLE_ENABLED": False,
                "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "AUTOTHROTTLE_ENABLED": True,
                "AUTOTHROTTLE_START_DELAY": 1,
                "AUTOTHROTTLE_MAX_DELAY": 60
                })  # DEBUG pour plus de détails
        process.crawl(FreeWorkSpider, keyword=keyword.replace(" ", "%20"))
        process.start()
        log_scraping(keyword)
        return {"status": "ok", "message": f"Scraping terminé pour '{keyword}'"}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}


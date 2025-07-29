from fastapi import FastAPI, HTTPException
from database import connect_to_db, has_already_scraped_today, log_scraping
from scrapy.crawler import CrawlerProcess
from scraper import FreeWorkSpider
from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.get("/annonces/")
def get_all_annonces():
    conn = connect_to_db()
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
        process = CrawlerProcess(settings={"LOG_LEVEL": "INFO"})
        process.crawl(FreeWorkSpider, keyword=keyword.replace(" ", "%20"))
        process.start()
        log_scraping(keyword)
        return {"status": "ok", "message": f"Scraping terminé pour '{keyword}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

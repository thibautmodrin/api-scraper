import scrapy
from datetime import datetime
from database import is_offer_already_exists, insert_offer

class FreeWorkSpider(scrapy.Spider):
    name = "free_work"

    def __init__(self, keyword, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.start_urls = [f"https://www.free-work.com/fr/tech-it/jobs?query={self.keyword}"]

    def parse(self, response):
        cards = response.xpath("//div[@class='relative group']")
        for card in cards:
            titre = card.xpath(".//h2/a/@href").get()
            entreprise = card.xpath('.//div[contains(@class, "font-bold")]/text()').get()
            lieu = card.xpath('.//span[contains(text(), "Lieu")]/following-sibling::span//text()').get()

            if titre and not is_offer_already_exists(titre.strip(), entreprise or "", lieu or ""):
                technos = card.xpath('.//a[contains(@class, "tag")]/div/span/text()').getall()
                duree = card.xpath('.//span[contains(text(), "Durée")]/following-sibling::span//text()').get()
                salaire = card.xpath('.//span[contains(text(), "Salaire")]/following-sibling::span//text()').get()
                tjm = card.xpath('.//span[contains(text(), "TJM")]/following-sibling::span//text()').get()
                teletravail = card.xpath('.//span[contains(text(), "Télétravail")]/following-sibling::span//text()').get()

                insert_offer({
                    "type": "Freelance",
                    "titre": titre.strip(),
                    "entreprise": entreprise.strip() if entreprise else "",
                    "technos": technos,
                    "duree": duree.strip() if duree else "",
                    "salaire": salaire.strip() if salaire else "",
                    "tjm": tjm.strip() if tjm else "",
                    "teletravail": teletravail.strip() if teletravail else "",
                    "lieu": lieu.strip() if lieu else "",
                    "date_extraction": datetime.now().date(),
                    "keyword": self.keyword.replace("%20", " "),
                })

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
        # 🔍 Cartes d'offres
        cards = response.xpath("//div[contains(@class, 'relative') and .//h2/a]")
        for card in cards:
            titre = card.xpath(".//div[1]/div/h2/a/@href").get()
            type1 = card.xpath(".//div[1]/div/div[1]/div/span[1]/div/text()").get()
            type2 = card.xpath(".//div[1]/div/div[1]/div/span[2]/div/text()").get()
            entreprise = card.xpath('.//div[contains(@class, "font-bold")]/text()').get()
            technos = card.xpath('.//a[contains(@class, "tag") and contains(@class, "bg-brand-75") and contains(@class, "text-brand-500")]/div/span[@class="fw-text-highlight"]/text()').getall()
            technos = [t.strip() for t in technos if t.strip()]
            duree = card.xpath('.//span[contains(text(), "Durée")]/following-sibling::span//span[contains(@class, "text-sm")]/text()').get()
            salaire = card.xpath('.//span[contains(text(), "Salaire")]/following-sibling::span//span[contains(@class, "text-sm")]/text()').get()
            tjm = card.xpath('.//span[contains(text(), "TJM")]/following-sibling::span//span[contains(@class, "text-sm")]/text()').get()
            teletravail = card.xpath('.//span[contains(text(), "Télétravail")]/following-sibling::span//span[contains(@class, "text-sm")]/text()').get()
            lieu = card.xpath('.//span[contains(text(), "Lieu")]/following-sibling::span//span[contains(@class, "text-sm")]/text()').get()

            if titre:
                titre_format = " ".join(map(str.capitalize, titre.split("/")[-1].split("-")))
                type1_clean = type1.replace(" ", "").replace("\n", "").replace("\r", "") if type1 else ""
                type2_clean = type2.replace(" ", "").replace("\n", "").replace("\r", "") if type2 else ""

                if not is_offer_already_exists(titre_format, entreprise or "", lieu or ""):
                    try:
                        insert_offer({
                            "type": f"{type1_clean} {type2_clean}".strip(),
                            "titre": titre_format,
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
                        self.logger.info(f"[✓] Offre insérée : {titre_format}")
                    except Exception as e:
                        self.logger.warning(f"[!] Erreur insertion : {e}")

        # 🔁 Pagination
        button_next_end = response.xpath("/html/body/div[1]/div/div/div/div[1]/div[2]/div/div/div[1]/div/div[8]/div[1]/button[2][contains(@class, 'bg-gray-200')]")
        page = response.xpath("/html/body/div/div/div/div/div[1]/div[2]/div/div/div[1]/div/div[18]/div[1]/button[2]").attrib.get("data-page")
        if not button_next_end and page:
            next_page = f"https://www.free-work.com/fr/tech-it/jobs?query={self.keyword}&page={page}"
            self.logger.info(f"→ Page suivante : {next_page}")
            yield response.follow(next_page, callback=self.parse)

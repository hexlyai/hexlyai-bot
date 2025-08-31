from scraper.tiktok_scraper import TikTokScraper
from scraper.meta_scraper import MetaScraper
from db import insert_ads

def run_all():
    t = TikTokScraper().run()
    insert_ads("tiktok", t)
    m = MetaScraper().run()
    insert_ads("meta", m)

if __name__ == "__main__":
    run_all()

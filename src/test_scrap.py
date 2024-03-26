from scraper.santander_scraper import SantanderScraper

if __name__ == "__main__":
    scrapper = SantanderScraper("200719913", "46@8sA5uqV", headles=False)
    scrapper.scrap()

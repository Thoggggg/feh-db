from scraper.abstract_scraper import Scraper
from scraper.heroes.from_template import extract_all_stats
from urls import FEH_FANDOM_HEROES


class HeroScraper(Scraper):
    def __init__(self, skip_download=False):
        super().__init__(FEH_FANDOM_HEROES, skip_download)

    def extract_class(self, html: str):
        """ Create a hero Class based on the given data

        Returns:
            Hero: a hero
        """
        hero = extract_all_stats(str(html))

        return hero

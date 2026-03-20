""" Define the Scraper that takes html and turns it into a hero """

from src.scraper.abstract_scraper import Scraper
from src.scraper.heroes.from_template import extract_all_stats
from src.urls import FEH_FANDOM_HEROES


class HeroScraper(Scraper):
    """ Scrap the heroes from FANDOM """
    def __init__(self, skip_download=False):
        super().__init__(FEH_FANDOM_HEROES, skip_download)

    def extract_class(self, html: str):
        """ Create a hero Class based on the given data

        Args:
            html (str): html string representing ONE hero

        Returns:
            Hero: One hero
        """
        hero = extract_all_stats(str(html))

        return hero

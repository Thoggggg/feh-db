""" Definition of the global FEH Scraper """

from src.scraper.heroes.scrap_hero import HeroScraper
from src.scraper.stats.scrap_stat import StatsScraper
from src.urls import FEH_FANDOM_GROWTH_RATE, FEH_FANDOM_LVL1, FEH_FANDOM_LVL40


class FehScraper:
    """ Scrap the fire emblem data from FANDOM """

    def __init__(self):
        skip_download = True  # TODO Dev attribute, don't put it in the final file
        self.heroes = HeroScraper(skip_download)
        self.scraper_gr = StatsScraper(FEH_FANDOM_GROWTH_RATE, skip_download)
        self.scraper_gr.set_offset_extractor(3)
        self.scraper_lvl1 = StatsScraper(FEH_FANDOM_LVL1, skip_download)
        self.scraper_lvl40 = StatsScraper(FEH_FANDOM_LVL40, skip_download)

from scraper.abstract_scraper import Scraper
from scraper.stats.from_template import extract_all_stats


class StatsScraper(Scraper):
    def __init__(self, url, skip_download=False):
        super().__init__(url, skip_download=skip_download)
        self.offset_table = 0

    def extract_class(self, html: str):
        """ Create a Stat Class based on the given data

        Returns:
            Hero: a hero
        """
        stats = extract_all_stats(str(html), offset=self.offset_table)

        return stats

    def set_offset_extractor(self, offset):
        self.offset_table = offset

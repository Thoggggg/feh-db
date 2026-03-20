""" Defines the scraper that get the stats of heroes"""

from src.scraper.abstract_scraper import Scraper
from src.scraper.stats.from_template import extract_all_stats


class StatsScraper(Scraper):
    """ Scraper for all the 5 stats """
    def __init__(self, url, skip_download=False):
        super().__init__(url, skip_download=skip_download)
        self.offset_table = 0

    def extract_class(self, html: str):
        """ Extract soem html info into a Stat class

        Args:
            html (str): the html representation of one hero's stat

        Returns:
            Stat: the stats
        """
        stats = extract_all_stats(str(html), offset=self.offset_table)

        return stats

    def set_offset_extractor(self, offset: int):
        """ Set an offset in the extacrtion
        The html uses an array to represent the data
        The important data might not always be the first given

        Args:
            offset (int): The id of the column we are interested in
        """
        self.offset_table = offset

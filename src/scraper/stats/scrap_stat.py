""" Defines the scraper that get the stats of heroes"""
import logging

from src.scraper.abstract_scraper import Scraper
from src.scraper.stats.from_template import extract_all_stats
from src.scraper.stats.stat_class import Stat


class StatsScraper(Scraper):
    """ Scraper for all the 5 stats """
    def __init__(self, url, skip_download=False):
        super().__init__(url, skip_download=skip_download)
        self.offset_table = 0

    def extract_class(self, soup: str):
        """ Extract soem html info into a Stat class

        Args:
            html (str): the html representation of one hero's stat

        Returns:
            Stat: the stats
        """

        hp = 0
        atk = 0
        spd = 0
        dfs = 0
        res = 0

        try:
            match = soup.select("td")
            if len(match) < 1:
                logging.warning(
                    f"The page layout might have changed. "
                    f"(Expected {self.CSS_SELECTOR.NB_A_EXPECTED} <a> "
                    f"paragraph, got {len(match)})"
                )
            else:
                hp = match[5 + self.offset_table].contents[0].replace("%", "").strip()
                atk = match[6 + self.offset_table].contents[0].replace("%", "").strip()
                spd = match[7 + self.offset_table].contents[0].replace("%", "").strip()
                dfs = match[8 + self.offset_table].contents[0].replace("%", "").strip()
                res = match[9 + self.offset_table].contents[0].replace("%", "").strip()
        except IndexError as err:
            logging.error("There is an issue with the format of the stats table. More info : ")
            logging.error(f"{err}. \n{soup}")
        except Exception as err:
            logging.error(f"{err}. \n{soup}")

        return Stat(hp, atk, spd, dfs, res)

    def set_offset_extractor(self, offset: int):
        """ Set an offset in the extacrtion
        The html uses an array to represent the data
        The important data might not always be the first given

        Args:
            offset (int): The id of the column we are interested in
        """
        self.offset_table = offset

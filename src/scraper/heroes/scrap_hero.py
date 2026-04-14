""" Define the Scraper that takes html and turns it into a hero """

from bs4 import BeautifulSoup
import logging

from src.scraper.heroes.hero_class import Hero
from src.scraper.abstract_scraper import Scraper
from src.urls import FEH_FANDOM_HEROES


class HeroScraper(Scraper):
    """ Scrap the heroes from FANDOM """
    class CSS_SELECTOR:
        """
        The CSS Selector constant values
        This value might change at the same time of the fandom
        """
        NB_A_EXPECTED = 2
        NB_TD_EXPECTED = 8
        NB_TR_EXPECTED = 1

    def __init__(self, skip_download=False):
        super().__init__(FEH_FANDOM_HEROES, skip_download)

    def extract_class(self, soup: BeautifulSoup) -> Hero:
        """ Create a hero Class based on the given data

        Args:
            html (str): html string representing ONE hero

        Returns:
            Hero: One hero
        """

        name = ""
        title = ""
        game = ""
        move = ""
        weapon = ""
        attributes = []
        release = "0001-01-01"

        try:
            # Extracting every high level text
            match = soup.select("a")
            if len(match) < self.CSS_SELECTOR.NB_A_EXPECTED:
                logging.warning(
                    f"The page layout might have changed. "
                    f"(Expected {self.CSS_SELECTOR.NB_A_EXPECTED} <a> "
                    f"paragraph, got {len(match)})"
                )
            else:
                name = str(match[1].contents[0]).strip().split(":")[0]
                title = str(match[1].contents[0]).strip().split(":")[1]

            # Using the fact that the columns might never change
            match = soup.select("td")
            if len(match) != self.CSS_SELECTOR.NB_TD_EXPECTED:
                logging.warning(
                    f"The page layout might have changed. "
                    f"(Expected {self.CSS_SELECTOR.NB_TD_EXPECTED} <td> "
                    f"paragraph, got {len(match)})"
                )
            else:
                sub_soup = BeautifulSoup(str(match[2].contents[1]), 'html.parser')
                sub_match = sub_soup.select("a")
                game = [m.contents[0].strip() for m in sub_match]

                sub_soup = BeautifulSoup(
                    str(match[4].contents[1]) + str(match[5].contents[1]),
                    'html.parser'
                )
                sub_match = sub_soup.select("[alt]")
                move = sub_match[0]["alt"]
                weapon = sub_match[1]["alt"]

                release = match[-1].contents[0].strip()

            match = soup.select("tr")
            if len(match) != self.CSS_SELECTOR.NB_TR_EXPECTED:
                logging.warning(
                    f"The page layout might have changed. "
                    f"(Expected {self.CSS_SELECTOR.NB_TR_EXPECTED} <tr> "
                    f"paragraph, got {len(match)})"
                )
            else:
                attributes = match[0].attrs["data-weapon-props"].split(';')
                attributes += match[0].attrs["data-availability-classes"].split(';')
        except IndexError as err:
            logging.error("There is an issue with the format of the hero table. More info : ")
            logging.error(f"Was able to get : {name=} {title=} {game=} {move=} {weapon=} {attributes=} {release=}")
            logging.error(f"{err}. \n{soup}")
        except Exception as err:
            logging.error(f"{err}. \n{soup}")

        return Hero(name, title, game, move, weapon, attributes, release)

        # return Hero("", "", "", "", "", [], "0001-01-01")

import logging
from bs4 import BeautifulSoup

from src.scraper.heroes.hero_class import Hero


def extract_all_stats(soup: BeautifulSoup) -> Hero:
    try:
        # Extracting every high level text
        match = soup.select("a")
        if len(match) != 6:
            logging.warning("The page layout might have changed. Exp")

        name = str(match[1].contents[0]).strip().split(":")[0]
        title = str(match[1].contents[0]).strip().split(":")[1]

        # Using the fact that the columns might never change
        match = soup.select("td")
        if len(match) != 8:
            logging.warning("The page layout might have changed")

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
        attributes = match[0].attrs["data-weapon-props"].split(';')
        attributes += match[0].attrs["data-availability-classes"].split(';')
        return Hero(name, title, game, "",
                    move, weapon, attributes, release)
    except Exception as err:
        logging.error(f"{err}. \n{soup}")
        return Hero("", "", "", "", "", "", "", "", [], "0001-01-01")

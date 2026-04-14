""" Define the default scraper """

from abc import abstractmethod
import os
import time
from bs4 import BeautifulSoup
from bs4.element import Tag
import httpx
import logging


class Scraper:
    """ Default scrapper """

    def __init__(self, url, skip_download=False):
        self.skip_download = skip_download
        self.fandom_url = url
        self.headers = {'user-agent': 'feh-db/0.0.1'}
        self.last_fetch = time.time()
        if url is not None:
            logging.info(f"Scraper is using this url : {url}")
            page_name = url.split("page=")[1].split("&prop")[0]
            self.html_output = f"html/base_{page_name}.html"

    def scrap(self):
        """ Get a soup representation of a URL

        Returns:
            BeautifulSoup: a soup of the html
        """

        if not self.skip_download or not os.path.exists(self.html_output):
            # Scrape from the Fandom wiki
            soup = self._get_html()
        else:
            # Read the base.html file instead
            logging.info("Decided to not download the html file")
            with open(self.html_output, 'r', encoding='utf-8') as file:
                html_cont = file.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_cont, 'html.parser')

        # Get a list of all the characters
        soup_list = self._extract_array(soup)
        return soup_list

    def _get_html(self) -> BeautifulSoup:
        """get the HTML of a given web page

        Returns:
            BeautifulSoup: A soup object with the content of the web page
        """
        # Politeness check (1s)
        if self.last_fetch < time.time() - 1:
            logging.warning("Get data to close to each other, try again")
            return

        # set the url to perform the get request
        page = httpx.get(self.fandom_url, headers=self.headers)
        self.last_fetch = time.time()

        # load the page content
        text = page.json()
        text = text["parse"]["text"]["*"]

        # make a soup object by using beautiful
        # soup and set the markup as html parser
        soup = BeautifulSoup(text, "html.parser")

        if self.html_output != "":
            with open(self.html_output, "w", encoding='utf-8') as file:
                # prettify the soup object and convert it into a string
                file.write(str(soup.prettify()))

        return soup

    def _extract_array(self, soup: BeautifulSoup) -> list[Tag]:
        """Extract an array from a html file

        Args:
            soup (BeautifulSoup): A soup object with a html containing an array

        Returns:
            list[Tag]: A list of the rows or a html array excluding the header
        """
        table = soup.find('table')
        rows = table.find_all('tr')
        return rows[1:]

    @abstractmethod
    def extract_class(self, html: str):
        """
        Args:
            html (str): a HTML like data from fandom
        """


if __name__ == "__main__":
    from src.urls import FEH_FANDOM_HEROES

    scraper = Scraper(FEH_FANDOM_HEROES, skip_download=True)

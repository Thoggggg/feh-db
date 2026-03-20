""" Functions to extract data from a template"""

from src.scraper.stats.stat_class import Stat
from src.scraper.template_extract import extract_default


def extract_all_stats(html: str, offset=0) -> Stat:
    # Seperate each columns
    html = html.split("<td")

    # Extract data from the html
    try:
        hp = extract_number(html[6 + offset]).replace("ù", "")
        atk = extract_number(html[7 + offset]).replace("ù", "")
        spe = extract_number(html[8 + offset]).replace("ù", "")
        dfe = extract_number(html[9 + offset]).replace("ù", "")
        res = extract_number(html[10 + offset]).replace("ù", "")

        return Stat(hp, atk, spe, dfe, res)
    except Exception as err:
        print(f"[ERROR] {err}. \n{html}")
        return Stat(0, 0, 0, 0, 0)


def extract_number(html: str) -> str:
    return extract_default(html, "../templates/stats/number.html", 0)


if __name__ == '__main__':
    # text = open("example/10.html", "r", encoding='utf-8').read()
    # template = open("template.html", "r", encoding='utf-8').read()

    for i in range(1, 11):
        print(f"==============={i}===============")
        text = open(f"example/{i}.html", "r", encoding='utf-8').read()
        stats = extract_all_stats(text)
        print(stats)

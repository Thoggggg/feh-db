import logging
from src.scraper.generic_scraper import FehScraper
from src.db.sql import SQL


def are_all_tab_are_equal(tables: list) -> bool:
    """ Check if all the table are of the same length

    Args:
        tables (list): List of list to check

    Returns:
        bool: If all tables are of the same size
    """
    expected_length = len(tables[0])
    for table in tables[1:]:
        if len(table) != expected_length:
            return False
        
    return True

# TODO : Add a confirmation
def sync(feh_scraper: FehScraper, db: SQL):
    """ Created a line for each hero in every db

    Args:
        feh_scraper (FehScraper): The scraper that got all the data
        db (SQL): the sql database
    """

    # Scrap new info
    heroes = feh_scraper.heroes.scrap()
    lvl1_stats = feh_scraper.scraper_lvl1.scrap()
    lvl40_stats = feh_scraper.scraper_lvl40.scrap()
    gr_stats = feh_scraper.scraper_gr.scrap()

    # For debug purposes
    skipped_counter = 0

    # Check iuf we can do the data extraction
    if not are_all_tab_are_equal([
        heroes, lvl1_stats, lvl40_stats, gr_stats
    ]):
        logging.error("All 4 tables don't have the same number of lines :")
        logging.error(f"Got : {len(heroes)=}, "
                      f"{len(lvl1_stats)=}, "
                      f" {len(lvl40_stats)=}, "
                      f" {len(gr_stats)=}")

    for h, l1, l40, gr in zip(heroes, lvl1_stats, lvl40_stats, gr_stats):
        # Extract from the soup
        hero = feh_scraper.heroes.extract_class(h)
        lvl1_stat = feh_scraper.scraper_lvl1.extract_class(l1)
        lvl40_stat = feh_scraper.scraper_lvl40.extract_class(l40)
        gr_stat = feh_scraper.scraper_gr.extract_class(gr)

        # Check if the data is correct
        if not hero.is_valid():
            logging.warning(f"{hero.name} name is invalid")
            continue

        if not lvl1_stat.is_valid():
            logging.warning(f"{hero.name} lvl1 is invalid")
            continue

        if not lvl40_stat.is_valid():
            logging.warning(f"{hero.name} lvl40 is invalid")
            continue

        if not gr_stat.is_valid():
            logging.warning(f"{hero.name} growth rate is invalid")
            continue

        if not db.is_character_existing(hero):
            logging.info(f"Adding {hero.name} as he was unknown before")
            hero_id = db.add_characters(hero)
            db.add_stats(hero_id, lvl1_stat, lvl40_stat, gr_stat)
        else:
            skipped_counter += 1

    logging.indo(f"skipped {skipped_counter} out of {len(heroes)}")


if __name__ == "__main__":
    scraper = FehScraper()

    db = SQL()

    sync(scraper, db)

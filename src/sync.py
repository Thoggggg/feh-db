from src.scraper.generic_scraper import FehScraper
from src.db.sql import SQL


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

    for h, l1, l40, gr in zip(heroes, lvl1_stats, lvl40_stats, gr_stats):
        # Extract from the soup
        hero = feh_scraper.heroes.extract_class(h)
        lvl1_stat = feh_scraper.scraper_lvl1.extract_class(l1)
        lvl40_stat = feh_scraper.scraper_lvl40.extract_class(l40)
        gr_stat = feh_scraper.scraper_gr.extract_class(gr)

        # Check if the data is correct
        if not hero.is_valid():
            print(f"[WARNING] {hero.name} name is invalid")
            continue

        if not lvl1_stat.is_valid():
            print(f"[WARNING] {hero.name} lvl1 is invalid")
            continue

        if not lvl40_stat.is_valid():
            print(f"[WARNING] {hero.name} lvl40 is invalid")
            continue

        if not gr_stat.is_valid():
            print(f"[WARNING] {hero.name} growth rate is invalid")
            continue

        if not db.is_character_existing(hero):
            print(f"[INFO] Adding {hero.name} as he was unknown before")
            hero_id = db.add_characters(hero)
            db.add_stats(hero_id, lvl1_stat, lvl40_stat, gr_stat)
        else:
            skipped_counter += 1

    print(f"[INFO] skipped {skipped_counter} out of {len(heroes)}")


if __name__ == "__main__":
    scraper = FehScraper()

    db = SQL()

    sync(scraper, db)

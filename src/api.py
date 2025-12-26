from fastapi import FastAPI, Response, status
from db.getter import get_heroes
from db.setter import set_my_characters
from db.sql import SQL
from reset import delete_all
from scraper.generic_scraper import FehScraper
from sync import sync

app = FastAPI()


# hero_scraper = HeroScraper(
#     skip_download=True)

# stats_scraper = StatsScraper(
#     skip_download=True)

feh_scraper = FehScraper()

db = SQL()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# TODO : Add date low and date high
@app.get("/heroes/")
def read_heroes(
    name="",
    title="",
    game_name="",
    movement_type="",
    weapon_type="",
    color="",
    start_date="1970-01-01",
    end_date=None,
    resplendent='FALSE',
    refresher='FALSE',
    harmonized='FALSE',
    emblem='FALSE',
    attuned='FALSE',
    ghb='FALSE',
    regular_5='FALSE',
    regular_4_3_2_1='FALSE',
    ascended='FALSE',
    specialRate='FALSE',
    duo='FALSE',
    aided='FALSE',
    rearmed='FALSE',
    mythic='FALSE',
    entwined='FALSE',
    legendary='FALSE',
    special='FALSE',
    story='FALSE',
    tempest='FALSE',
    Ranged='FALSE',
    Magical='FALSE',
    Melee='FALSE',
    Magic='FALSE',
    Dragon='FALSE',
    Multicolor='FALSE',
    Missile='FALSE',
    Close='FALSE',
    Physical='FALSE',
):
    # Create the filter dictionnary
    filter_dict = dict()

    # TODO : is this really the way to do it ?
    for key, filter in locals().items():
        if filter != "" and key != "filter_dict":
            filter_dict[key] = filter

    heroes = get_heroes(db.cursor, filter_dict)

    return heroes


# TODO : find a more suitable bad status
@app.patch("/heroes/", status_code=200)
def update_db(response: Response):
    sync(feh_scraper, db)
    # response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Hello": "World"}


@app.delete("/heroes/", status_code=200)
def delete_db(response: Response):
    global db
    # Delete the db
    delete_all(db.db, db.cursor)

    # Create it agan
    db = SQL()

    return {}


@app.get("/heroes/my", status_code=200)
def get_my_heroes():
    # TODO
    # Return id, lvl, fusion, buff, nerf

    query = "SELECT * FROM mycharacters JOIN characters ON Character_ID = characters.ID"
    db.cursor.execute(query, "")

    return db.cursor.fetchall()


@app.put("/heroes/my", status_code=200)
def change_my_heroe(
    id: str,
    lvl="0",
    fusion="0",
    buff="",
    nerf="",
    draco_flower="0"):

    set_my_characters(db.cursor, id, int(lvl), int(fusion), buff, nerf, int(draco_flower))

    return {}

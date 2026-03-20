""" The main API file """

from typing import Annotated
from fastapi import FastAPI, Query
from fastapi import HTTPException
from src.db.getter import get_heroes
from src.db.setter import set_my_characters
from src.db.sql import SQL
from pydantic import BaseModel, Field

from src.enums.colors import WeaponColor
from src.enums.movements import MOVEMENTS_TYPE
from src.enums.stats import STATS_TYPE
from src.enums.weapons import Weapons
from src.reset import delete_all
from src.scraper.generic_scraper import FehScraper
from src.sync import sync


# The 3 main components
app = FastAPI()

feh_scraper = FehScraper()

db = SQL()


class HeroesFilters(BaseModel):
    """ Base mode to validate the hero fetching """

    name: str | None = Field(
        None,
        description="Part or full name of the hero"
    )
    title: str = Field(
        None,
        description="Part or full title of the hero"
    )
    game_name: str = Field(
        None,
        description="Filter by the given game",
        examples=["Fire Emblem: Mystery of the Emblem", "Fire Emblem Fates"]
    )
    movement_type: MOVEMENTS_TYPE = Field(
        default=None,
        description="Movement Name",
        examples=["Infantry", "Flying"]
    )
    weapon_type: Weapons = Field(
        default=None,
        description="Weapon Type",
        examples=["Sword", "Breath"]
    )
    color: WeaponColor = Field(
        default=None,
        description="Weapon color",
        examples=["Red", "Unicolor"]
    )
    start_date: str = Field(default="1970-01-01")
    end_date: str = Field(
        default=None,
        examples=["09-01-2000"]
    )
    resplendent: bool | None = None
    refresher: bool | None = None
    harmonized: bool | None = None
    emblem: bool | None = None
    attuned: bool | None = None
    ghb: bool | None = None
    regular_5: bool | None = None
    regular_4_3_2_1: bool | None = None
    ascended: bool | None = None
    specialRate: bool | None = None
    duo: bool | None = None
    aided: bool | None = None
    rearmed: bool | None = None
    mythic: bool | None = None
    entwined: bool | None = None
    legendary: bool | None = None
    special: bool | None = None
    story: bool | None = None
    tempest: bool | None = None
    Ranged: bool | None = None
    Magical: bool | None = None
    Melee: bool | None = None
    Magic: bool | None = None
    Dragon: bool | None = None
    Multicolor: bool | None = None
    Missile: bool | None = None
    Close: bool | None = None
    Physical: bool | None = None


@app.get("/")
def read_root():
    """ For test purposes only, don't use """
    raise HTTPException(status_code=501, detail="Not implemented")


@app.get("/heroes/", status_code=200)
def read_heroes(
    hero_filter: Annotated[HeroesFilters, Query()]
):
    """ Get a filtered list of hero """

    heroes = get_heroes(db.cursor, hero_filter.model_dump())

    if heroes == -1:
        raise HTTPException(status_code=400, detail="Bad request")

    if len(heroes) == 0:
        raise HTTPException(status_code=204, detail="No content")

    return heroes


@app.patch("/heroes/", status_code=200)
def update_db():
    """ Add new heroes to the db """
    sync(feh_scraper, db)
    return {}


@app.delete("/heroes/", status_code=200)
def delete_db():
    """ Delete every db. Recreate the generic db"""
    global db
    # Delete the db
    delete_all(db.db, db.cursor)

    # Create it again
    db = SQL()

    return {}


@app.get("/heroes/my", status_code=200)
def get_my_heroes():
    # TODO
    # Return id, lvl, fusion, buff, nerf

    query = "SELECT * FROM mycharacters JOIN characters ON Character_ID = characters.ID"
    db.cursor.execute(query, "")

    return db.cursor.fetchall()


class MyHeroesFilters(BaseModel):
    id: int
    lvl: int = Field(default=40, gt=0, lt=41)
    fusion: int = Field(default=0, gt=-1, lt=41)
    draco_flower: int = Field(default=0, gt=-1)
    buff: STATS_TYPE | None = None
    nerf: STATS_TYPE | None = None


@app.put("/heroes/my", status_code=201)
def change_my_heroes(stats: Annotated[MyHeroesFilters, Query()]):

    name = set_my_characters(
        db.cursor,
        stats.id,
        int(stats.lvl),
        int(stats.fusion),
        stats.buff,
        stats.nerf,
        int(stats.draco_flower)
    )

    if len(name) == 0:
        raise HTTPException(status_code=400, detail="Bad ID")

    return {"OK": name}


@app.delete("/heroes/my")
def delete_hero(id: int):
    query = f"SELECT * FROM mycharacters WHERE Character_ID = {id}"
    db.cursor.execute(query, "")

    if len(db.cursor.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    query = f"DELETE FROM mycharacters WHERE Character_ID = {id}"
    db.cursor.execute(query, "")

    return {}

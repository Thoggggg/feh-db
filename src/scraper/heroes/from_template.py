from scraper.heroes.hero_class import Hero
from scraper.template_extract import extract_default


def extract_all_stats(html: str) -> Hero:
    # Seperate each columns
    html = html.split("<td")

    # Extract data from the html
    try:
        attributes, weapon, move = extract_header(html[0])
        move = move[0]
        try:
            attributes.remove("")
        except:
            pass

        picture = extract_picture(html[1])
        name, title = extract_hero(html[2])
        has_multiple_games = "harmonized" in attributes
        has_multiple_games |= "emblem" in attributes
        has_multiple_games |= title == "Plains Wind" or title == "Sage of the Wind"
        has_multiple_games |= name == "Leif" or name == "Naga"
        if has_multiple_games:
            game = ""
        else:
            game = extract_game(html[3])
        # entry = extract_entry(html[4])
        # move = extract_move(html[5])
        # weapon = extract_weapon(html[6])
        rarity = extract_rarity(html[7])
        release = extract_release(html[8])
        return Hero(picture, name, title, game, "",
                    move, weapon, rarity, attributes, release)
    except Exception as err:
        print(f"[ERROR] {err}. \n{html}")
        return Hero("", "", "", "", "", "", "", "", [], "0001-01-01")


def extract_header(html: str):
    # extract_default(html, "templates/heroes/header.html", 3).split(";") + \
    return extract_default(html, "templates/heroes/header.html", 0).split(";") + \
            extract_default(html, "templates/heroes/header.html", 1).split(";") + \
            extract_default(html, "templates/heroes/header.html", 4).split(";")[2:], \
            extract_default(html, "templates/heroes/header.html", 5), \
            extract_default(html, "templates/heroes/header.html", 2).split(";")


def extract_picture(html: str) -> str:
    return extract_default(html, "templates/heroes/picture.html", 0)


def extract_hero(html: str) -> tuple[str, str]:
    return extract_default(html, "templates/heroes/hero.html", 1), \
        extract_default(html, "templates/heroes/hero.html", 2)


def extract_game(html: str) -> str:
    return extract_default(html, "templates/heroes/game.html", 2)


def extract_entry(html: str) -> str:
    return extract_default(html, "templates/heroes/entry.html", 1)


def extract_move(html: str) -> str:
    return extract_default(html, "templates/heroes/move.html", 1)


def extract_weapon(html: str) -> str:
    return extract_default(html, "templates/heroes/weapon.html", 1)


def extract_rarity(html: str) -> str:
    pass


def extract_release(html: str) -> str:
    return extract_default(html, "templates/heroes/release.html", 0)


if __name__ == '__main__':
    # text = open("example/10.html", "r", encoding='utf-8').read()
    # template = open("template.html", "r", encoding='utf-8').read()

    for i in range(1, 11):
        print(f"==============={i}===============")
        text = open(f"example/{i}.html", "r", encoding='utf-8').read()
        hero = extract_all_stats(text)
        print(hero.picture)
        print(hero.name)
        print(hero.title)
        print(hero.game)
        print(hero.entry)
        print(hero.move)
        print(hero.weapon)
        print(hero.release)

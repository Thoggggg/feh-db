# This file has all the long sql queries

_games_create = """ Games (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    game_name VARCHAR(255) NOT NULL,
    static_img_path VARCHAR(255)
    );
"""

_movements_create = """Movements (
    ID INT PRIMARY KEY,
    movement_type VARCHAR(100),
    static_image_path VARCHAR(255)
);"""

_weapons_create = """Weapons (
    ID INT PRIMARY KEY,
    weapon_type VARCHAR(100),
    color VARCHAR(50),
    static_img VARCHAR(255)
);"""

_characters_create = """Characters (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Title VARCHAR(255),
    Game_ID INT,
    Movement_ID INT,
    Weapon_ID INT,
    Date DATE,
    Static_img_path VARCHAR(255),

    FOREIGN KEY (Game_ID) REFERENCES Games(ID),
    FOREIGN KEY (Movement_ID) REFERENCES Movements(ID),
    FOREIGN KEY (Weapon_ID) REFERENCES Weapons(ID)
);"""

_my_characters_create = """MyCharacters (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Character_ID INT,
    Buff VARCHAR(20),
    Nerf VARCHAR(20),
    Level INT,
    Fusion INT,
    Favorite BOOLEAN,
    Dracoflower INT,

    current_hp INT DEFAULT 0,
    current_atk INT DEFAULT 0,
    current_spe INT DEFAULT 0,
    current_def INT DEFAULT 0,
    current_res INT DEFAULT 0,
    FOREIGN KEY (Character_ID) REFERENCES Characters(ID)
);"""

_attributes_create = """Attributes (
    resplendent BOOLEAN DEFAULT FALSE,
    refresher BOOLEAN DEFAULT FALSE,
    harmonized BOOLEAN DEFAULT FALSE,
    emblem BOOLEAN DEFAULT FALSE,
    attuned BOOLEAN DEFAULT FALSE,
    ghb BOOLEAN DEFAULT FALSE,
    regular_5 BOOLEAN DEFAULT FALSE,
    regular_4_3_2_1 BOOLEAN DEFAULT FALSE,
    ascended BOOLEAN DEFAULT FALSE,
    specialRate BOOLEAN DEFAULT FALSE,
    duo BOOLEAN DEFAULT FALSE,
    aided BOOLEAN DEFAULT FALSE,
    rearmed BOOLEAN DEFAULT FALSE,
    mythic BOOLEAN DEFAULT FALSE,
    entwined BOOLEAN DEFAULT FALSE,
    legendary BOOLEAN DEFAULT FALSE,
    special BOOLEAN DEFAULT FALSE,
    story BOOLEAN DEFAULT FALSE,
    tempest BOOLEAN DEFAULT FALSE,
    ranged BOOLEAN DEFAULT FALSE,
    magical BOOLEAN DEFAULT FALSE,
    melee BOOLEAN DEFAULT FALSE,
    magic BOOLEAN DEFAULT FALSE,
    dragon BOOLEAN DEFAULT FALSE,
    multicolor BOOLEAN DEFAULT FALSE,
    missile BOOLEAN DEFAULT FALSE,
    close BOOLEAN DEFAULT FALSE,
    physical BOOLEAN DEFAULT FALSE,

    Character_ID INT PRIMARY KEY AUTO_INCREMENT
);"""

_stats_create = """CharacterStats (
    character_id INT PRIMARY KEY,

    hp_lvl1 INT DEFAULT 0,
    atk_lvl1 INT DEFAULT 0,
    spd_lvl1 INT DEFAULT 0,
    def_lvl1 INT DEFAULT 0,
    res_lvl1 INT DEFAULT 0,

    hp_growth  INT DEFAULT 0,
    atk_growth INT DEFAULT 0,
    spd_growth INT DEFAULT 0,
    def_growth INT DEFAULT 0,
    res_growth INT DEFAULT 0,

    hp_lvl40  INT DEFAULT 0,
    atk_lvl40 INT DEFAULT 0,
    spd_lvl40 INT DEFAULT 0,
    def_lvl40 INT DEFAULT 0,
    res_lvl40 INT DEFAULT 0,

    FOREIGN KEY (character_id) REFERENCES Characters(ID)
)"""

create_tables = {
    "Games": _games_create,
    "Movements": _movements_create,
    "Weapons": _weapons_create,
    "Characters": _characters_create,
    "Attributes": _attributes_create,
    "MyCharacters": _my_characters_create,
    "CharacterStats": _stats_create,
}

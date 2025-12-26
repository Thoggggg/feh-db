from math import floor
from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector.errors import ProgrammingError

from scraper.stats.stat_class import Stat


def set_my_characters(cursor: MySQLCursorAbstract, id: int, lvl: int, fusion: int, buff: str, nerf: str, draco_flower: int):
    character_stats = _get_characters_stats(cursor, id)

    if not buff:
        buff = "none"
    if not nerf:
        nerf = "none"
    traits_dic = _get_buff_dict(buff, nerf)

    # Unpack from the list
    try:
        lvl1 = _get_lvl1_dict(character_stats)

        # If not 40 considered one
        if lvl != 40:
            stat = lvl1

        growth = _get_growth_rate_dict(character_stats)
    except ValueError as err:
        print(character_stats)
        print(f"[ERROR] {err}")

        return

    # Compute the lvl 40 with the buff and nerf
    stat = compute_all_40(growth, traits_dic, lvl1, fusion)

    # Change the values in the
    query = f"SELECT * FROM mycharacters WHERE Character_ID = {id}"
    try:
        cursor.execute(query, "")
    except ProgrammingError as err:
        print(f"[ERROR] This query wasn't succesful : {' '.join(query.split())}")
        print(err)
        return

    if len(cursor.fetchall()) == 0:
        query = "INSERT INTO mycharacters (" \
            "Character_ID, Buff, Nerf, Level, Fusion, Favorite, Dracoflower, "\
            "current_hp, current_atk, current_spe, current_def, current_res) "\
            "VALUES (" \
            f"{id}, '{buff}', '{nerf}', {lvl}, {fusion}, {False}, {0}, {stat.hp},"\
            f"{stat.atk}, {stat.spd}, {stat.dfs}, {stat.res}"\
            ")"
    else:
        query = "UPDATE mycharacters SET " \
            f"Buff = '{buff}', " \
            f"Nerf = '{nerf}', " \
            f"Level = {lvl}, " \
            f"Fusion = {fusion}, " \
            f"Favorite = {False}, " \
            f"Dracoflower = {0}, " \
            f"current_hp = {stat.hp}, " \
            f"current_atk = {stat.atk}, " \
            f"current_spe = {stat.spd}, " \
            f"current_def = {stat.dfs}, " \
            f"current_res = {stat.res}, " \
            f"WHERE Character_ID = {id}"

    try:
        print(query)
        cursor.execute(query, "")
    except ProgrammingError as err:
        print(f"[ERROR] This query wasn't succesful : {' '.join(query.split())}")
        print(err)
        return


def _get_characters_stats(cursor: MySQLCursorAbstract, id: int):
    query = f"SELECT * FROM characterstats WHERE character_id = {id}"
    try:
        cursor.execute(query, "")
    except ProgrammingError as err:
        print(f"[ERROR] This query wasn't succesful : {' '.join(query.split())}")
        print(err)
        return
    character_stats = cursor.fetchall()

    # Check that the character stats are correct
    if len(character_stats) != 1:
        print(f"[ERROR] Fetched ID ({id}) is probably wrong")
        return []

    if len(character_stats[0]) != 16:
        print("[ERROR] Couldn't unpack characterstats, weird")
        return []

    return character_stats[0][1:]  # Ignore the character ID


def _get_buff_dict(buff: str, nerf: str) -> Stat:
    # Update the buff and nerf into datas
    # None is just here to not have any error when ""
    traits_dic = {'hp': 0, 'atk': 0, 'spd': 0, 'def': 0, 'res': 0, 'none': 0}

    if buff in traits_dic.keys():
        traits_dic[buff] = 1
    else:
        print(f"Ignoring {id} buff ({buff} was unexpected)")

    if nerf in traits_dic.keys():
        traits_dic[nerf] = -1
    else:
        print(f"Ignoring {id} nerf ({nerf} was unexpected)")

    return Stat(traits_dic['hp'], traits_dic['atk'], traits_dic['spd'], traits_dic['def'], traits_dic['res'])


def _get_lvl1_dict(character_stats: list) -> Stat:
    hp_lvl1, atk_lvl1, spd_lvl1, def_lvl1, res_lvl1 = character_stats[0:5]

    return Stat(hp_lvl1, atk_lvl1, spd_lvl1, def_lvl1, res_lvl1)


def _get_growth_rate_dict(character_stats: list) -> Stat:
    hp_growth, atk_growth, spd_growth, def_growth, res_growth = character_stats[5:10]

    return Stat(hp_growth, atk_growth, spd_growth, def_growth, res_growth)


def compute_all_40(growth_rate: Stat, buff: Stat, lvl1: Stat, fusion: int):
    """
    Translates the FEH Excel Formula for Level 40 Stats + Merges.

    Excel Equation logic:
    L13 (Base Lvl40)
    + P13 (Growth value - covered by 'fusion_default' in user logic context, or 'P' column context)
    + SI($O13<=MOD($P$4*2;5);1;0) (Merge distribution)
    + SI($P$4>=1; SI(MIN($E$8:$E$12)=-1;SI(E13=-1;3;0);SI(O13<4;1;0)); 0) (Flaw fix or Neutral bonus)
    """

    # 1. Calculate Base Lvl 40 Stats (Column L logic)
    # Formula: Lvl1 + Buff + Growth_Calculation
    # Note: We must iterate because floor operations happen on individual scalar values

    # Check if there is a flaw (Minimum of buff values is -1)
    has_flaw = any(val == -1 for val in buff)

    # Calculate Ranks based on Base Level 1 stats (Column O logic)
    # Note: FEH Merge priorities are usually based on Lvl 1 stats.
    lvl1_ranks = lvl1.rank()

    final_stats_list = []

    # Iterate through indices 0 to 4 (HP, Atk, Spd, Def, Res)
    for i in range(5):
        # Extract scalar values for this specific stat
        gr = growth_rate[i]
        b = buff[i]
        l1 = lvl1[i]
        rank = lvl1_ranks[i]

        # --- Base Level 40 Calculation ---
        # Corresponds to user snippet: floor(39 * floor(growth_rate_calc * 1.14) / 100)
        # and lvl40 = lvl1_calc + growth_value

        growth_rate_calc = gr + b
        lvl1_calc = l1 + b

        growth_value = floor(39 * floor(growth_rate_calc * 1.14) / 100)
        base_lvl40 = lvl1_calc + growth_value

        # --- Merge Calculations ---

        # 1. Fusion Default (Line P in logic / "+1 to all stats" part)
        # =ENT(($P$4*2)/5) -> floor(fusion * 2 / 5)
        fusion_default = floor(fusion * 2 / 5)

        # 2. Merge Distribution (The first SI/IF in the excel formula)
        # SI($O13<=MOD($P$4*2;5);1;0)
        # Adds +1 to specific stats based on rank and merge count
        merge_modulo_bonus = 0
        if rank <= (fusion * 2) % 5:
            merge_modulo_bonus = 1

        # 3. Flaw Fix / Neutral Bonus (The second SI/IF block)
        # SI($P$4>=1; SI(MIN...); 0)
        special_bonus = 0

        if fusion >= 1:
            if has_flaw:
                # SI(E13=-1;3;0) -> If this stat is the flaw, add 3
                if b == -1:
                    special_bonus = 3
            else:
                # Neutral Unit Logic: SI(O13<4;1;0) -> Top 3 stats get +1
                if rank < 4:
                    special_bonus = 1

        # Sum it all up
        final_val = base_lvl40 + fusion_default + merge_modulo_bonus + special_bonus
        final_stats_list.append(final_val)

    # Return a new Stat object with the calculated values
    return Stat(*final_stats_list)


def _set_my_character():
    pass

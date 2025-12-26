"""All the URLs from where I get data"""

# The generic API
FEH_FANDOM_API = "https://feheroes.fandom.com/api.php"

# A list of all the heroes
FEH_FANDOM_HEROES = f"{FEH_FANDOM_API}?action=parse&page=List_of_Heroes&prop=text&format=json"

# A list of the lvl 1 stats of each hero
FEH_FANDOM_LVL1 = f"{FEH_FANDOM_API}?action=parse&page=Level_1_stats_table&prop=text&format=json"

# A list of the lvl 40 stats of each hero
FEH_FANDOM_LVL40 = f"{FEH_FANDOM_API}?action=parse&page=Level_40_stats_table&prop=text&format=json"

# A list of the growth rate of each stat for each hero
# More info on growth rate : https://feheroes.fandom.com/wiki/Stat_growth
FEH_FANDOM_GROWTH_RATE = f"{FEH_FANDOM_API}?action=parse&page=Growth_rate_table&prop=text&format=json"

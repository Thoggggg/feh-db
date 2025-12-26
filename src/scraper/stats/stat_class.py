from scraper.generic_class import GenericDataConverterToDb


def rank_unique(data):
    # 1. Store the original index alongside the value: (index, value)
    indexed_data = list(enumerate(data))

    # 2. Sort based on the value (x[1]).
    # We use reverse=True so the Highest Stat gets Rank 1 (Standard FEH logic).
    # Python's sort is stable, so ties are broken by the original index (HP > Atk > Spd > Def > Res).
    sorted_data = sorted(indexed_data, key=lambda x: x[1], reverse=True)

    # 3. Create a result list of zeros to hold the ranks
    ranks = [0] * len(data)

    # 4. Assign ranks based on the position in the sorted list
    for rank, (original_index, value) in enumerate(sorted_data):
        # Use 'rank + 1' for 1-based ranking (1st, 2nd, 3rd)
        ranks[original_index] = rank + 1

    return ranks


class Stat(GenericDataConverterToDb):
    def __init__(self, hp: int = 0, atk: int = 0, spd: int = 0, dfs: int = 0, res: int = 0):
        self.hp = int(hp)
        self.atk = int(atk)
        self.spd = int(spd)
        self.dfs = int(dfs)
        self.res = int(res)

    def __str__(self):
        return f"hp={self.hp}, atk={self.atk}, spd={self.spd}, dfs={self.dfs}, res={self.res}"

    def __iter__(self):
        yield self.hp
        yield self.atk
        yield self.spd
        yield self.dfs
        yield self.res

    def __getitem__(self, item):
        # Allows accessing stats by index (0=hp, 1=atk, etc.) for iteration loops
        return list(self)[item]

    def __add__(self, val):
        if isinstance(val, Stat):
            return Stat(
                self.hp + val.hp,
                self.atk + val.atk,
                self.spd + val.spd,
                self.dfs + val.dfs,
                self.res + val.res,
            )
        if isinstance(val, int):
            return Stat(
                self.hp + val,
                self.atk + val,
                self.spd + val,
                self.dfs + val,
                self.res + val,
            )
        return self

    def rank(self):
        # Ranks based on values in this specific Stat object
        ranks = rank_unique([self.hp, self.atk, self.spd, self.dfs, self.res])
        return Stat(*ranks)

    def is_valid(self):
        return all([
            self.hp != 0,
            self.atk != 0,
            self.spd != 0,
            self.dfs != 0,
            self.res != 0,
        ])

# data structure for fast preference lookups
# creates ranking maps to check student preferences
def createRankingMaps(preferences):
    # init ranking maps list
    rankingMaps = []

    # process each unit's preference list
    for prefs in preferences:
        rankMap = {}
        
        # for each pos in prefs, map unit to its rank (0 = most preferred)
        for rank, unit in enumerate(prefs):
            rankMap[unit] = rank

        rankingMaps.append(rankMap)
    
    return rankingMaps
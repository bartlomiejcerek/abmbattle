import numpy as np

def manhattanMetcic(source, dest):

    return abs(source[0] - dest[0]), abs(source[1] - dest[1])

def findEnemies(field, uid):

    team = field.units[uid].team
    source = (np.where(field.uid_map == uid)[0][0], np.where(field.uid_map == uid)[1][0])

    dests = []
    for i in field.units:
        if not i == uid and not team == field.units[i].team:
            dests.append((np.where(field.uid_map == i)[0][0], np.where(field.uid_map == i)[1][0]))

    return source, dests

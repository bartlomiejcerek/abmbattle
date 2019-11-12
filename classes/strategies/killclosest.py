# -*- coding: utf-8 -*-
import random
import numpy as np

from classes.battlefield import BattleField

class KillTheClosest():
    def __init__(self):
        pass

    def findClosestEnemy(self, agent, enemies):

        distances = []

        for i in enemies:
            distances.append(manhattanMetcic(agent, i))

        return enemies[distances.index(min(distances))]

    def make_move(self, field, uid, poss_actions):

        if (len(poss_actions) == 1):
            return poss_actions[0]

        for i in range(0, len(poss_actions)):
            if (poss_actions[i][0] == BattleField.unit_attack):
                return poss_actions[i]

        mahBoy, enemies = findEnemies(field, uid)
        closestEnemy = self.findClosestEnemy(mahBoy, enemies)
        dist = manhattanMetcic(mahBoy, closestEnemy)

        poss_best_moves = []
        for action in poss_actions:
            if action[0] == BattleField.unit_nothing:
                continue
            if manhattanMetcic(action[1][1], closestEnemy) < dist:
                poss_best_moves.append(action)

        if len(poss_best_moves) == 0:
            move = random.randint(0, len(poss_actions)-2)
            return poss_actions[move]
        else:
            return random.choice(poss_best_moves)




def BFS(field, uid):

    """
        TODO: implement BFS from source to each destination, saving the path
        use findEnemies()
    """
    pass

def manhattanMetcic(source, dest):

    return abs(source[0] - dest[0]), abs(source[1] - dest[1])

def findEnemies(field, uid):

    team = field.units[uid][0]
    source = (np.where(field.uid_map == uid)[0][0], np.where(field.uid_map == uid)[1][0])

    dests = []
    for i in field.units:
        if not i == uid and not team == field.units[i][0]:
            dests.append((np.where(field.uid_map == i)[0][0], np.where(field.uid_map == i)[1][0]))

    return source, dests

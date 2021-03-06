# -*- coding: utf-8 -*-
import random
import numpy as np
import classes.strategies.Utils.enemies as en
import classes.strategies.Utils.search as srch

from classes.battlefield import BattleField

class KillTheClosest():
    def __init__(self):
        pass

    def make_move(self, field, uid, poss_actions):

        if (len(poss_actions) == 1):
            return poss_actions[0]

        for i in range(0, len(poss_actions)):
            if (poss_actions[i][0].type == 'Attack'):
                return poss_actions[i]

        mahBoy, enemies = en.findEnemies(field, uid)
        closestEnemy = srch.findClosestEnemy(mahBoy, enemies)
        dist = en.manhattanMetcic(mahBoy, closestEnemy)

        poss_best_moves = []
        for action in poss_actions:
            if action[0].type == 'Nothing':
                continue
            if en.manhattanMetcic(action[1][1], closestEnemy) < dist:
                poss_best_moves.append(action)

        if len(poss_best_moves) == 0:
            move = random.randint(0, len(poss_actions)-2)
            return poss_actions[move]
        else:
            return random.choice(poss_best_moves)



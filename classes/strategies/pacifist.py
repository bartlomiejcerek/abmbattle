# -*- coding: utf-8 -*-
import random

import classes.strategies.Utils.enemies as en
import classes.strategies.Utils.search as srch

class Pacifist():
    def __init__(self):
        pass

    def make_move(self, field, uid, poss_actions):

        mahBoy, enemies = en.findEnemies(field, uid)
        closestEnemy = srch.findClosestEnemy(mahBoy, enemies)
        dist = en.manhattanMetcic(mahBoy, closestEnemy)
        poss_best_moves = []

        for action in poss_actions:
            if action[0].type == 'Nothing' or action[0].type == 'Attack':
                continue
            if en.manhattanMetcic(action[1][1], closestEnemy) > dist:
                poss_best_moves.append(action)

        if not len(poss_best_moves) == 0:
            return random.choice(poss_best_moves)

        # 'Nothing'
        return poss_actions[-1]
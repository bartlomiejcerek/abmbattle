# -*- coding: utf-8 -*-
import classes.strategies.Utils.enemies as en
import classes.strategies.Utils.search as search


class Spartan():

    numberOfSpartans = -1

    def __init__(self):
        pass

    def countSpartans(self, field):
        currentNumberOfSpartans = 0
        for unit in field.units:
            if unit.strat == Spartan:
                currentNumberOfSpartans+=1

        if currentNumberOfSpartans > self.numberOfSpartans:
            self.numberOfSpartans = currentNumberOfSpartans
        return currentNumberOfSpartans

    def make_move(self, field, uid, poss_actions):

        if (len(poss_actions) == 1):
            return poss_actions[0]

        mahBoy, enemies = en.findEnemies(field, uid)
        closestEnemy = search.findClosestEnemy(mahBoy, enemies)
        currentNumberOfSpartans = self.countSpartans(field)

        if (float(self.numberOfSpartans)/float(currentNumberOfSpartans) > 0.3):
            if (en.manhattanMetcic(mahBoy, closestEnemy) == 0):
                for action in poss_actions:
                    if action[0].type == 'Block':
                        return action
            else:
                for action in poss_actions:
                    if action[0].type == 'Attack':
                        return action

        if (en.manhattanMetcic(mahBoy, closestEnemy) == 1):
            for action in poss_actions:
                if action[0].type == 'Attack':
                    return action

        # Block if confused
        for action in poss_actions:
            if action[0].type == 'Block':
                return action

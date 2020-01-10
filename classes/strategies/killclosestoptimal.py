# -*- coding: utf-8 -*-
import classes.strategies.Utils.enemies as en
import classes.strategies.Utils.search as search


class KillTheClosest():
    def __init__(self):
        pass

    def make_move(self, field, uid, poss_actions):

        if (len(poss_actions) == 2):
            return poss_actions[0]

        for i in range(0, len(poss_actions)):
            if (poss_actions[i][0].type == 'Attack'):
                return poss_actions[i]

        mahBoy, enemies = en.findEnemies(field, uid)

        if (len(enemies) == 0):  # important if no enemies left, but a move still has to be done to finish round
            return poss_actions[-1]

        vf = search.BFS(mahBoy, field)
        path = search.makePath(mahBoy, enemies, field, vf)

        # Will try to get rid of this in Utils.search.makePath, however this might need to stay
        
        if len(path) == 0:
            # return poss_actions[-1]
            vf = search.BFS(mahBoy, field, False)
            path = search.makePath(mahBoy, enemies, field, vf)

        # Dangerous pop
        nextStep = path.pop()

        for action in poss_actions:
            if (action[0].type == 'Move'):
                if (action[1][1] == nextStep):
                    return action

        return poss_actions[-1]

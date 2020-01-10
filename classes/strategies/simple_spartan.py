# -*- coding: utf-8 -*-
import classes.strategies.Utils.enemies as en
import classes.strategies.Utils.search as search
import math


class Spartan():

    numberOfSpartans = -1

    def __init__(self):
        pass
    
    @staticmethod
    def euclidian_dist(ag1, ag2):
        return int(math.sqrt((ag1[0] - ag2[0])**2 + (ag1[1] - ag2[1])**2))

    def make_move(self, field, uid, poss_actions):

        if (len(poss_actions) == 1):
            return poss_actions[0]

        mahBoy, enemies = en.findEnemies(field, uid)
        closestEnemy = search.findClosestEnemy(mahBoy, enemies)
        dist = self.euclidian_dist(mahBoy, closestEnemy)
        
        #Make decision about action based on distance to closest enemy
        if dist == 1:
            act_name = 'Block'
        elif dist == 2:
            act_name = 'Attack'
        else:
            act_name = 'Nothing'

        #Find method in possible action
        for act in poss_actions:
            if act[0].type == act_name:
                action = act
        
        #Rise error in case of wrong action
        if action is None:
            raise Exception('Wanted action was not accesible.')

        return action

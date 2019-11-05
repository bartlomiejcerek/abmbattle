# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:03:00 2019

@author: Bartek
"""

import random


class Engine:
    def __init__(self, field):
        self.field = field
        self.history = []
        self.history.append(field.get_shapshot())
        # For simple vizualization

    def makeRandomMove(self):
        '''Performs random move with each unit'''
        units = self.field.units
        uids = list(units.keys())

        for uid in uids:
            # Check if unit is not dead
            if uid not in units.keys():
                continue
            available_acts = self.field.getAvailableActions(uid)
            action, args = random.choice(available_acts)
            # Perform Action (explicit passing of object)
            action(self.field, *args)

        self.history.append(self.field.get_shapshot())

    def checkState(self):
        '''This function in futre will return info about mode, now only if over'''
        # Obtain set of teams
        teams = [self.field.units[k][0] for k in self.field.units.keys()]
        teams = set(teams)
        if len(teams) == 1:
            return True
        else:
            return False

    def get_history(self):
        return self.history

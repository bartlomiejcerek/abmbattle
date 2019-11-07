# -*- coding: utf-8 -*-
import random


class Engine:
    def __init__(self, field):
        self.field = field #Stores uid_map and units
        self.history = [] #History of uid_maps after every round
        self.det_history = [] #Detailed history, holds uids maps after every move
        
        self.history.append(field.get_snapshot()) # For simple vizualization
        self.det_history.append(field.get_snapshot())

    def run_random_round(self):
        '''Performs random move with each unit'''
        units = self.field.units
        uids = list(units.keys())

        for uid in uids:
            # Check if unit is not dead
            if uid not in units.keys():
                continue
            available_acts = self.field.get_available_actions(uid)
            action, args = random.choice(available_acts)
            # Perform Action (explicit passing of object)
            action(self.field, *args)
            self.det_history.append(self.field.get_snapshot())

        self.history.append(self.field.get_snapshot())

    def check_state(self):
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

    def get_det_history(self):
        return self.det_history
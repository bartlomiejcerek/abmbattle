# -*- coding: utf-8 -*-
import json

import numpy as np
import random

from classes.battlefield import BattleField
from classes.unit import Unit


class Engine:
    def __init__(self):
        self.history = []  # History of uid_maps after every move
        self.units_history = []  # History of uid_maps after every move
        self.round = 0
        self.teams = None

    def load_config(self, config_file):
        # Read map file
        with open(config_file, 'r') as f:
            setting_dict = json.load(f)
        init_pos = np.array(setting_dict['field'])
        self.teams = setting_dict['teams']
        units_dict = setting_dict['units']
        units = {}
        for uuid in units_dict.keys():
            params = units_dict[uuid]
            units[int(uuid)] = Unit(params['team'], 
                                    int(params['hp']), 
                                    int(params['att']), 
                                    int(params['ran']), 
                                    params['strat']
                                    )

        self.field = BattleField(init_pos, units)
        # For vizualization
        field, units = self.field.get_snapshot()
        self.history.append(field)
        self.units_history.append(units)

    def run_round(self):
        '''Performs move with each unit'''
        self.round += 1
        units = self.field.units

        # Unit can be killed and deleted from units dict during the round.
        # Then iterator will change and cause error so hard copy it
        all_uids = list(units.keys())
        random.shuffle(all_uids) #Random initiative in each round
        for uid in all_uids:
            # First check if unit was not killed IN THIS ROUND if yes ignore
            if uid not in units.keys():
                continue
            available_acts = self.field.get_available_actions(uid)
            action, args = units[uid].strat.make_move(self.field, uid, available_acts)
            # Perform Action (explicit passing of object)
            action(self.field, *args)

            # For vizualization
            field_snap, units_snap = self.field.get_snapshot()
            self.history.append(field_snap)
            self.units_history.append(units_snap)

    def check_state(self):
        '''This function in futre will return info about mode, now only if over'''
        # Obtain set of teams
        teams = [self.field.units[k].team for k in self.field.units.keys()]
        teams = set(teams)
        if len(teams) == 1:
            self.winner = teams.pop()  # Only remaining team is winner
            return True
        return False

    def get_winner(self):
        return self.winner

    def get_field_history_data(self):
        return self.history

    def get_units_visualization_data(self):
        return self.units_history, self.teams

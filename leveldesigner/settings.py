import json
import logging

import numpy as np


class Settings():

    def __init__(self):
        self.field = None
        self.teams = None
        self.units = None
        self.id_counter = 0

    def units_convert(self, units):
        self.units = {}
        uids = units.keys()
        for uid in uids:
            self.units[int(uid)] = units[uid]

    def load_file(self, filename):
        with open(filename, 'r') as f:
            setting_dict = json.load(f)
        self.field = np.array(setting_dict['field'])
        self.teams = setting_dict['teams']
        self.units_convert(setting_dict['units'])
        self.id_counter = max(self.units.keys())

    def save_to_file(self, filename):
        # sort units ids
        with open(filename, 'w') as f:
            json.dump({'field': self.field.tolist(), 'teams': self.teams, 'units': self.units}, f)

    def create_board(self, x, y):
        logging.info("Board with shape ({}, {}) created ".format(x, y))
        self.field = np.zeros((x, y))
        self.units = {}

    def add_team(self, team_name):
        if self.teams is None:
            self.teams = []
        self.teams.append(team_name)

    def delete_team(self, el):
        if self.teams and isinstance(el, int):
            del self.teams[el]

    def get_teams(self):
        if self.teams is None:
            self.teams = []
        return self.teams

    def get_field_shape(self):
        if self.field is None:
            return (0, 0)
        else:
            return self.field.shape

    def create_obstacle(self, x, y):
        if self.helth_check(x, y):
            self.field[x][y] = -1

    def clear_position(self, x, y):
        if self.helth_check(x, y):
            prev = self.field[x][y]
            self.field[x][y] = 0
            if prev > 0:
                del self.units[prev]

    def create_unit(self, x, y, team, hp, attack, strategy):
        if self.helth_check(x, y):
            prev = self.field[x][y]
            if prev > 0:
                self.units[prev]['team'] = team
                self.units[prev]['hp'] = hp
                self.units[prev]['att'] = attack
                self.units[prev]['strat'] = strategy
            else:
                self.id_counter += 1
                self.field[x][y] = self.id_counter
                self.units[self.id_counter] = {'uid': self.id_counter, 'team': team,
                                               'hp': hp, 'att': attack,
                                               'strat': strategy}

    def helth_check(self, x, y):
        if self.field is None:
            return False
        if x < 0 or x > self.field.shape[0]:
            return False
        if y < 0 or y > self.field.shape[1]:
            return False

        return True

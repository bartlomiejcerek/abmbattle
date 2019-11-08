# -*- coding: utf-8 -*-
import copy
import xml.etree.ElementTree as ET

from classes.battlefield import BattleField

class Engine:
    def __init__(self, strategy):
        self.strategy = strategy
        self.history = [] #History of uid_maps after every move
        
    def load_config(self, map_file, units_file):
        #Read map file
        init_pos = []
        with open(map_file) as f:
            for line in f:
                init_pos.append([int(pos) for pos in line.split() ])
        
        #Read units file
        units = {}
        tree = ET.parse(units_file)
        root = tree.getroot()
        for unit in root:
            uid = int(unit[0].text)
            #Key UID, Vals: team, HP, ATT
            units[uid] = (unit[1].text, int(unit[2].text), int(unit[3].text))
            
        self.field = BattleField(init_pos, units)
        self.history.append(self.field.get_snapshot()) # For vizualization

    def run_round(self):
        '''Performs move with each unit'''
        units = self.field.units
        uids = list(units.keys()) #Bcoz iteraotr will change size

        for uid in uids:
            # QUICK FIX Check if unit is not dead - don't delte from iterator !!!
            if uid not in units.keys():
                continue
            available_acts = self.field.get_available_actions(uid)
            action, args = self.strategy.make_move(self.field, uid, available_acts)
            # Perform Action (explicit passing of object)
            action(self.field, *args)
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
        return copy.deepcopy(self.history)

    def get_units(self):
        return copy.deepcopy(self.field.units)
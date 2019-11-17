# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from classes.battlefield import BattleField

class Engine:
    def __init__(self):
        self.history = []  # History of uid_maps after every move
        self.units_history = []  # History of uid_maps after every move
        self.round = 0

    def load_config(self, map_file, units_file):
        # Read map file
        init_pos = []
        with open(map_file) as f:
            for line in f:
                init_pos.append([int(pos) for pos in line.split()])

        # Read units file and parse it to classic touple
        units = {}
        tree = ET.parse(units_file)
        root = tree.getroot()
        for unit in root:
            uid = int(unit[0].text)
            # Key UID, Vals: team, HP, ATT
            units[uid] = (unit[1].text, int(unit[2].text), int(unit[3].text), unit[4].text)

        self.field = BattleField(init_pos, units)
        # For vizualization
        field, units = self.field.get_snapshot()
        self.history.append(field)
        self.units_history.append(units)

    def run_round(self):
        '''Performs move with each unit'''
        self.round += 1
        units = self.field.units
        
        #Unit can be killed and deleted from units dict during the round.
        #Then iterator will change and cause error so hard copy it 
        all_uids = list(units.keys())
        for uid in all_uids:
            #First check if unit was not killed IN THIS ROUND if yes ignore
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
            self.winner = teams.pop() #Only remaining team is winner
            return True
        return False
        
    def get_winner(self):
        return self.winner

    def get_history(self):
        return self.history

    def get_units_history(self):
        return self.units_history

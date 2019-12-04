# -*- coding: utf-8 -*-
import copy

import numpy as np


#Module Utilities
#Create neighbour dict given deltas and not obstacles - for different range options
def _create_neigh_dict(deltas, not_obstacles, uid_map):
    neigh_dict = {}
    for x, y in not_obstacles:
        neighbours = [(x + d[0], y + d[1]) for d in deltas]
        neigh_dict[(x, y)] = []
        for n in neighbours:
            x_ok = 0 <= n[0] < uid_map.shape[0]
            y_ok = 0 <= n[1] < uid_map.shape[1]
            if x_ok and y_ok:
                if uid_map[n] >= 0:  # Has to be separet if bcoz of exceptions
                    neigh_dict[(x, y)].append(n)                
    return neigh_dict
    

#Battle Field Class
class BattleField:
    def __init__(self, fields, units):
        # 2D array where -1..-1 obstacles, 0 free spot, 1..n UID
        self.uid_map = fields
        self.units = units

        # Find neighbours for range 1 and 2 apart of each cell that is not obstacle to use later
        deltas1 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        deltas2 = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        not_obstacles = [(x, y) for (x, y), _ in np.ndenumerate(self.uid_map) if self.uid_map[(x, y)] >= 0]
        #Range 1 
        self.neigh_dict1 = _create_neigh_dict(deltas1, not_obstacles, self.uid_map)
        #Range 2
        self.neigh_dict2 = _create_neigh_dict(deltas2, not_obstacles, self.uid_map)

        # Write positions of units to dictionary for fast locating - uid key, pos val
        self.units_pos = {}
        for uid in self.units.keys():
            pos = np.where(self.uid_map == uid)
            pos = (pos[0].item(), pos[1].item())  # Unpack from numpy
            self.units_pos[uid] = pos

    def unit_nothing(self, *args):  # Give option to take args bcoz touple will be passed
        pass

    unit_nothing.type = 'Nothing'  # Add type for easy checking

    def unit_move(self, uid, new_pos):
        '''That funcion DOES NOT check if move is legal!'''
        curr_pos = self.units_pos[uid]
        # Old position free, unit on new position
        self.uid_map[curr_pos] = 0
        self.uid_map[new_pos] = uid
        self.units_pos[uid] = new_pos  # Update units dict too

    unit_move.type = 'Move'  # Add type for easy checking

    def unit_attack(self, attacker_uid, defender_uid):
        '''That funcion DOES NOT check if move is legal!'''
        # Get attacker and defender stats
        attacker = self.units[attacker_uid]
        defender = self.units[defender_uid]

        # Check if we have kill
        if defender.hp - attacker.att <= 0:
            def_pos = self.units_pos[defender_uid]
            self.uid_map[def_pos] = 0  # Empty spot where defender was
            self.units.pop(defender_uid)  # Delte from units dict
            self.units_pos.pop(defender_uid)  # Delete from units pos dict
        else:
            self.units[defender_uid].hp = defender.hp - attacker.att

    unit_attack.type = 'Attack'  # Add type for easy checking

    def get_available_actions(self, uid):
        '''Returns list of touples where 0 - action method, 1 - parametrs'''
        # Prepare variables for checking
        curr_pos = self.units_pos[uid]
        neighbours1 = self.neigh_dict1[curr_pos] #Range 1
        neighbours2 = self.neigh_dict2[curr_pos] #Range 2
        unit = self.units[uid]
        poss_actions = []

        # Move options
        for n in neighbours1:
            if self.uid_map[n] == 0:  # is free
                poss_actions.append((BattleField.unit_move, (uid, n)))

        # Attack options, first check range of attack 
        if unit.ran > 1:
            neigh_to_attac = neighbours1 + neighbours2
        else:
            neigh_to_attac = neighbours1
        
        for n in neigh_to_attac:
            n_uid = int(self.uid_map[n].item())  # Get neighbour unit
            if n_uid == 0:
                continue  # Empty spot
            n_unit = self.units[n_uid]
            if unit.team == n_unit.team:
                continue  # friendly fire
            # Everything seems correct, attack
            poss_actions.append((BattleField.unit_attack, (uid, n_uid)))

        # Always append option to do nothing - with empty touple
        poss_actions.append((BattleField.unit_nothing, ()))

        return poss_actions

    def get_snapshot(self):
        return np.copy(self.uid_map), copy.deepcopy(self.units)

# -*- coding: utf-8 -*-
import numpy as np

class BattleField:
    def __init__(self, fields, units):
        self.uid_map = np.array(fields)
        self.units = units
        
        #Find neighbours of each cell that is not obstacle to use later
        niegh_dict = {}
        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        not_obstacles = [(x,y) for (x,y), _ in np.ndenumerate(self.uid_map) if self.uid_map[(x,y)] >= 0]
        for x, y in not_obstacles:
            neighbours = [(x + d[0], y + d[1]) for d in deltas]
            niegh_dict[(x,y)] = []
            for n in neighbours:
                x_ok = 0 <= n[0] < self.uid_map.shape[0]
                y_ok = 0 <= n[1] < self.uid_map.shape[1]
                if x_ok and y_ok:
                    if self.uid_map[n] >= 0: #Has to be separet if bcoz of exceptions
                        niegh_dict[(x,y)].append(n)
        self.neigh_dict = niegh_dict          

    def unit_nothing(self, *args):  # Give option to take args bcoz touple will be passed
        pass

    def unit_move(self, uid, new_pos):
        '''That funcion DOES NOT check if move is legal!'''
        curr_pos = np.where(self.uid_map == uid)
        # Old position free, unit on new position
        self.uid_map[curr_pos] = 0
        self.uid_map[new_pos] = uid

    def unit_attack(self, attacker_uid, defender_uid):
        '''That funcion DOES NOT check if move is legal!'''
        # Get attacker and defender stats
        a_team, a_hp, a_att = self.units[attacker_uid]
        d_team, d_hp, d_att = self.units[defender_uid]

        # Check if we have kill
        if d_hp - a_att <= 0:
            def_pos = np.where(self.uid_map == defender_uid)
            self.uid_map[def_pos] = 0  # Empty spot where defender was
            self.units.pop(defender_uid)  # Delte from units dict
        else:
            self.units[defender_uid] = (d_team, d_hp - a_att, d_att)

    def get_available_actions(self, uid):
        '''Returns list of touples where 0 - action method, 1 - parametrs'''
        # Prepare variables for checking
        curr_pos = np.where(self.uid_map == uid)
        
        #QUICK FIX
        curr_pos = (curr_pos[0].item(), curr_pos[1].item())
        
        neighbours = self.neigh_dict[curr_pos]
        a_team, a_hp, a_att = self.units[uid]
        poss_actions = []

        #Move options
        for n in neighbours:
            if self.uid_map[n] == 0: #is free
                poss_actions.append((BattleField.unit_move, (uid, n)))

        #Attack options
        for n in neighbours:
            d_uid = self.uid_map[n].item()
            if d_uid == 0:
                continue # Empty spot
            d_team, d_hp, d_att = self.units[d_uid]
            if d_team == a_team:
                continue  # friendly fire
            # Everything seems correct, attack
            poss_actions.append((BattleField.unit_attack, (uid, d_uid)))

        # Always append option to do nothing - with empty touple
        poss_actions.append((BattleField.unit_nothing, ()))

        return poss_actions

    def get_snapshot(self):
        return np.copy(self.uid_map)
    

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:01:50 2019

@author: Bartek
"""
import numpy as np


class BattleField:
    def __init__(self, fields, units):
        self.uid_map = np.array(fields)
        self.units = units

    def unitNothing(self, *args):  # Give option to take args bcoz touple will be passed
        pass

    def unitMove(self, uid, new_pos):
        '''That funcion DOES NOT check if move is legal!'''
        curr_pos = np.where(self.uid_map == uid)
        # Old position free, unit on new position
        self.uid_map[curr_pos] = 0
        self.uid_map[new_pos] = uid

    def unitAttack(self, attacker_uid, defender_uid):
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

    def getAvailableActions(self, uid):
        '''Returns list of touples where 0 - action method, 1 - parametrs'''
        # Prepare variables for checking
        coords = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        curr_pos = np.where(self.uid_map == uid)
        neighbours = [(curr_pos[0] + c[0], curr_pos[1] + c[1]) for c in coords]
        a_team, a_hp, a_att = self.units[uid]
        poss_actions = []

        # Check for move options
        for n in neighbours:
            try:  # Check if new move in map range and if free
                ocupation_ok = self.uid_map[n] == 0
            except IndexError:  # Will happend if position outside of board
                ocupation_ok = False
            if ocupation_ok:
                poss_actions.append((BattleField.unitMove, (uid, n)))

        # Check for attack options
        for n in neighbours:
            try:
                d_uid = self.uid_map[n].item()
            except IndexError:  # Will happend if position outside of board
                continue
            if d_uid == 0 or d_uid == -1:
                continue  # If obstacle or free field can't attack
            d_team, d_hp, d_att = self.units[d_uid]
            if d_team == a_team:
                continue  # If they are from same team can't attack
            # Everything seems correct attack
            poss_actions.append((BattleField.unitAttack, (uid, d_uid)))

        # Always append option to do nothing - with empty touple
        poss_actions.append((BattleField.unitNothing, ()))

        return poss_actions

    def get_shapshot(self):
        return np.copy(self.uid_map)

# -*- coding: utf-8 -*-
from classes.strategies.killclosestoptimal import KillTheClosest
from classes.strategies.randomstrat import RandomStrategy

#Define Which Strategies May Be used
available_strategies = [KillTheClosest, RandomStrategy]

startegies_by_name = {}
for strat in available_strategies:
    startegies_by_name[strat.__name__] = strat


class Unit:
    def __init__(self, unit_params):
        #touple of parameters: (team, HP, ATTACK)
        team, hp, att, strat_str = unit_params
        self.team = team
        self.hp = hp
        self.att = att
        self.strat = startegies_by_name[strat_str]()
        
    def __repr__(self):
        return "({}, {}, {})".format(self.team, self.hp, self.att)
    
    
        
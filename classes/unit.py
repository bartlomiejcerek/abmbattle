# -*- coding: utf-8 -*-
from classes.strategies.killclosestoptimal import KillTheClosest
from classes.strategies.randomstrat import RandomStrategy
from classes.strategies.pacifist import Pacifist
from classes.strategies.simple_spartan import Spartan

# Define Which Strategy May Be used
available_strategies = [KillTheClosest, RandomStrategy, Pacifist, Spartan]

startegies_by_name = {}
for strat in available_strategies:
    startegies_by_name[strat.__name__] = strat

class Unit:
    def __init__(self, team, hp, att, ran, strat_str):
        # touple of parameters: (team, HP, ATTACK)
        self.team = team
        self.hp = hp
        self.att = att
        self.ran = ran
        self.strat = startegies_by_name[strat_str]()
        self.shield = False

    def __repr__(self):
        return "({}, {}, {})".format(self.team, self.hp, self.att)

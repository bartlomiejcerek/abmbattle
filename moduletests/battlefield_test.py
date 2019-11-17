# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 11:26:48 2019

@author: Bartek
"""
from classes.battlefield import BattleField


uid_map = [[0,0],
           [1,2]]

units ={1: ('red',1,2,'RandomStrategy'),
        2: ('blue',1,2,'KillTheClosest') }

a = BattleField(uid_map, units)
print(dir(a))

print(a.uid_map)
a.unit_move(1, (0,0))
print(a.uid_map)
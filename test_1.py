# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:03:26 2019

@author: Bartek
"""
import sys
sys.path.append("classes/")

from battlefield import BattleField 
from engine import Engine 


### 2D list where: 
### -1 obstacle 
### 0 free spot 
### 1..n 
init_pos = [[ 0, 0, 0, 1, 2],
            [ 0,-1, 0, 0, 0],
            [ 0,-1,-1, 0, 0],
            [ 0, 0, 0, 0, 0],
            [ 3, 4, 0,-1,-1]]

### Dictionary of units where:
### key - name of unit 
### values - touple of parameters: (team, HP, ATTACK)
units = {1 : ('red', 3, 1),
         2 : ('red', 3, 1),
         3 : ('blue', 3, 1),
         4 : ('blue', 3, 1)}


field = BattleField(init_pos, units)
engine = Engine(field)
end = False

i = 0
while not end:
    engine.makeRandomMove()
    #engine.simpleVizualization()
    print(engine.field.uid_map)
    end = engine.checkState()
    i+=1

print('Over after {} moves'.format(i))
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:03:26 2019

@author: Bartek
"""

import copy
import matplotlib.pyplot as plt

from classes.viewer import Viewer
from classes.battlefield import BattleField
from classes.engine import Engine

### 2D list where: 
### -1 obstacle 
### 0 free spot 
### 1..n 
init_pos = [[0, 0, 0, 1, 2 ],
            [0, -1, 0, 0, 0],
            [0, -1, -1, 0, 0],
            [0, 0, 0, 0, 0 ],
            [3, 4, 0, -1, -1]]

### Dictionary of units where:
### key - name of unit 
### values - touple of parameters: (team, HP, ATTACK)
units = {1: ('red', 3, 1),
         2: ('red', 3, 1),
         3: ('blue', 3, 1),
         4: ('blue', 3, 1)}

field = BattleField(init_pos, units)
engine = Engine(field)
units_initial = copy.deepcopy(units)

end = False
i = 0
while not end:
    engine.run_random_round()
    #print(engine.field.uid_map)
    end = engine.check_state()
    i += 1

print('Over after {} moves'.format(i))

#Animation needs to be returned to context where it will be show to work with all backends
#history = engine.get_history()
det_history = engine.get_det_history()

animation = Viewer(units_initial, det_history).get_animation(interval = 300)
plt.show()


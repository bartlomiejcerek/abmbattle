# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from classes.engine import Engine
from classes.strategies.killclosest import KillTheClosest
from classes.viewer import Viewer

#2D list where -1..-1 obstacles, 0 free spot, 1..n UID
map_file = 'config/map.txt'
#Dictionary of units where KEY: uid, VALS:touple of parameters: (team, HP, ATTACK)
units_file = 'config/units.xml'

strategy = KillTheClosest()
engine = Engine(strategy)
engine.load_config(map_file, units_file)
units_initial = engine.get_units()

end = False
i = 0
while not end:
    engine.run_round()
    #print(engine.field.uid_map)
    end = engine.check_state()
    i += 1

print('Over after {} moves'.format(i))

#Animation needs to be returned to context where it will be show to work with all backends
history = engine.get_history()

animation = Viewer(units_initial, history).get_animation(interval = 300)
plt.show()


# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from classes.engine import Engine
from classes.viewer import Viewer

from classes.strategies.randomstrat import RandomStrategy
from classes.strategies.killclosestoptimal import KillTheClosest
from classes.strategies.killclosestsimple import KillTheClosest as KillTheClosesSimple


#2D list where -1..-1 obstacles, 0 free spot, 1..n UID
map_file = 'config/map.txt'
#Dictionary of units where KEY: uid, VALS:touple of parameters: (team, HP, ATTACK)
units_file = 'config/units.xml'

#CHOICE: RandomStrategy, KillTheClosest, KillTheClosesSimple
strategy = KillTheClosest()

engine = Engine(strategy)
engine.load_config(map_file, units_file)
units_initial = engine.get_units_history()

end = False
i = 0
while not end:
    engine.run_round()
    end = engine.check_state()
    i += 1

print('Over after {} rounds'.format(i))
print('Winner is team: ', engine.get_winner())


#Animation needs to be returned to context where it will be show to work with all backends
history = engine.get_history()
animation = Viewer(units_initial, history).get_animation(interval = 200)
plt.show()


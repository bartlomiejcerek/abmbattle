# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from classes.engine import Engine
from classes.viewer import Viewer
from classes.big_viewer import BigViewer

settings_file = 'config/spartan_test.json'
# settings_file = 'config/2x2_classic.json'
# settings_file = 'config/4_teams.json'

engine = Engine(save_all_moves = True)
engine.load_config(settings_file)

end = False
i = 0
while not end and i<1000: #limit
    engine.run_round(0.2) #Run round with 0.2 miss prob.
    end = engine.check_state()
    i += 1
    #print(i)

print('Over after {} rounds'.format(i))
print('Winner is team: ', engine.get_winner())

# Animation needs to be returned to context where it will be show to work with all backends
animation = Viewer(engine.get_units_visualization_data(), engine.get_field_history_data()).get_animation(interval=300)
#animation = BigViewer(engine.get_units_visualization_data(), engine.get_field_history_data()).get_animation(interval=100)
#animation.save('gifs/BV_50x50.gif')
#plt.show()

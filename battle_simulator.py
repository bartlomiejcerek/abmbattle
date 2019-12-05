# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from classes.engine import Engine
from classes.viewer import Viewer

settings_file = 'config/4_teams.json'

engine = Engine()
engine.load_config(settings_file)

end = False
i = 0
while not end and i<200: #100 limit
    engine.run_round(0.2) #Run round with 0.2 miss prob.
    end = engine.check_state()
    i += 1

print('Over after {} rounds'.format(i))
print('Winner is team: ', engine.get_winner())

# Animation needs to be returned to context where it will be show to work with all backends
animation = Viewer(engine.get_units_visualization_data(), engine.get_field_history_data()).get_animation(interval=50)
animation.save('gifs/4teams.gif')
#plt.show()

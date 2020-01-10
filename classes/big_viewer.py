# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import colors
import copy

class BigViewer:

    def __init__(self, units_data, history):
        self.history = history
        self.no_frames = len(history)
        self.units_history = units_data[0]
        self.fig = plt.figure()
        self.cmap = colors.ListedColormap(['black', 'white', 'red', 'blue'])        
        axes = plt.gca()
        x = history[0].shape[0]
        y = history[0].shape[1]
        axes.set_xlim([0-0.5, x-0.5]) #Shift to see all pixels
        axes.set_ylim([0-0.5, y-0.5]) #shift to see all pixels
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        axes.set_xticks([])
        axes.set_yticks([])

    def init_plot(self):
        #Iniatiate image
        image = self._hist_to_img(0)
        self.im = plt.imshow(image, cmap = self.cmap)
        return image

    def update(self, num):
        image = self._hist_to_img(num)
        self.im.set_array(image)
        return self.im

    def get_animation(self, interval=900):
        ani = FuncAnimation(self.fig, self.update, frames=self.no_frames,
                            init_func=self.init_plot, interval=interval)
        # ani.save('little_masakra.gif', dpi=120, writer='imagemagick')
        return ani

    def _hist_to_img(self, num):
        h = copy.deepcopy(self.history[num])
        u = copy.deepcopy(self.units_history[num])
        
        for (x,y), uid in np.ndenumerate(h):
            if uid in u.keys():
                h[x,y] = u[uid].team      
        return np.rot90(h, k=3) #Dont know why but it was rotated
        

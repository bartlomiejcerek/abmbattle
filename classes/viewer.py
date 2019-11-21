# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

colors = ['ro', 'bo', 'co', 'go', 'mo', 'yo']


class Viewer:

    def __init__(self, units_data, history):
        self.units_history = units_data[0]
        self.teams = units_data[1]
        self.states = history
        self.fig, self.ax = plt.subplots()
        self.obstacles, = plt.plot([], [], 'ks', markersize=15)
        self.data = {}
        for i, team in enumerate(self.teams):
            self.data[team] = plt.plot([], [], colors[i], markersize=15)

        plt.grid(True)
        axes = plt.gca()
        x = history[0].shape[0]
        y = history[0].shape[1]
        axes.set_xlim([0, x])
        axes.set_ylim([0, y])
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        axes.set_xticks(np.array(range(1, x)))
        self.ax.set_yticks(np.array(range(1, y)))
        self.annotations = []

    def init_plot(self):
        return self.update(0)

    def update(self, num):
        for i, a in enumerate(self.annotations):
            a.remove()

        self.annotations[:] = []
        obstacles, units = self.convert_to_data(self.states[num], self.units_history[num])
        for team in units.keys():
            self.data[team][0].set_data(units[team]['x'], units[team]['y'])
            for i, hp in enumerate(units[team]['hp']):
                hp_label = self.ax.annotate(hp, xy=(units[team]['x'][i], units[team]['y'][i]), ha='center', va='center',
                                            color='white', size=10)
                self.annotations.append(hp_label)
        self.obstacles.set_data(obstacles['x'], obstacles['y'])
        lines = (self.obstacles, [units[d] for d in units.keys()])
        return lines,

    def get_animation(self, interval=900):
        ani = FuncAnimation(self.fig, self.update, frames=len(self.states),
                            init_func=self.init_plot, interval=interval)
        ani.save('little_masakra.gif', dpi=120, writer='imagemagick')
        return ani

    def convert_to_data(self, field, units):

        obstacles = {'x': [], 'y': []}
        unit_cords = {}
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i, j] < 0:
                    obstacles['x'].append(i + 0.5)
                    obstacles['y'].append(j + 0.5)
                if field[i, j] > 0:
                    team = units[field[i, j]].team
                    if team not in unit_cords.keys():
                        unit_cords[team] = {'x': [], 'y': [], 'hp': []}
                    unit_cords[team]['x'].append(i + 0.5)
                    unit_cords[team]['y'].append(j + 0.5)
                    unit_cords[team]['hp'].append(units[field[i, j]].hp)
        return obstacles, unit_cords

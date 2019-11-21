# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Viewer:

    def __init__(self, units_history, history):
        self.units_history = units_history
        self.states = history
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.red_team, = plt.plot([], [], 'ro', markersize=15)
        self.blue_team, = plt.plot([], [], 'bo', markersize=15)
        self.obstacles, = plt.plot([], [], 'ks', markersize=30)
        plt.grid(True)
        axes = plt.gca()
        axes.set_xlim([0, history[0].shape[0]])
        axes.set_ylim([0, history[0].shape[1]])
        self.annotations = []

    def init_plot(self):
        return self.update(0)

    def update(self, num):
        for i, a in enumerate(self.annotations):
            a.remove()

        self.annotations[:] = []
        rX, rY, rL, bX, bY, bL, oX, oY = self.convert_to_data(self.states[num], self.units_history[num])
        self.red_team.set_data(rX, rY)
        self.blue_team.set_data(bX, bY)
        self.obstacles.set_data(oX, oY)

        for i, hp in enumerate(rL):
            hp_label = self.ax.annotate(hp, xy=(rX[i], rY[i]), ha='center', va='center', color='white')
            self.annotations.append(hp_label)
        for i, hp in enumerate(bL):
            hp_label = self.ax.annotate(hp, xy=(bX[i], bY[i]), ha='center', va='center',  color='white')
            self.annotations.append(hp_label)
        return (self.red_team, self.blue_team, self.obstacles),

    def get_animation(self, interval=900):
        ani = FuncAnimation(self.fig, self.update, frames=len(self.states),
                            init_func=self.init_plot, interval=interval)
        #ani.save('rules.gif', dpi=120, writer='imagemagick')
        return ani

    def convert_to_data(self, field, units):
        redX, redY, redL = [], [], []
        blueX, blueY, blueL = [], [], []
        obstacleX, obstacleY = [], []
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i, j] < 0:
                    obstacleX.append(i + 0.5)
                    obstacleY.append(j + 0.5)
                if field[i, j] > 0:
                    color = units[field[i, j]].team
                    hp = units[field[i, j]].hp
                    if color == 'red':
                        redX.append(i + 0.5)
                        redY.append(j + 0.5)
                        redL.append(hp)
                    else:
                        blueX.append(i + 0.5)
                        blueY.append(j + 0.5)
                        blueL.append(hp)

        return redX, redY, redL, blueX, blueY, blueL, obstacleX, obstacleY

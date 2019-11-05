import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Viewer:

    def __init__(self, units, history):
        self.units = units
        self.states = history
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.red_team, = plt.plot([], [], 'ro', markersize=15)
        self.blue_team, = plt.plot([], [], 'bo', markersize=15)
        self.obstacles, = plt.plot([], [], 'ks', markersize=30)
        plt.grid(True)
        axes = plt.gca()
        axes.set_xlim([0, history[0].shape[0] + 1])
        axes.set_ylim([0, history[0].shape[1] + 1])

    def init_plot(self):
        return self.update(0)

    def update(self, num):
        rX, rY, bX, bY, oX, oY = self.convert_to_data(self.states[num])
        self.red_team.set_data(rX, rY)
        self.blue_team.set_data(bX, bY)
        self.obstacles.set_data(oX, oY)
        return (self.red_team, self.blue_team, self.obstacles),

    def show(self):
        ani = FuncAnimation(self.fig, self.update, frames=len(self.states),
                            init_func=self.init_plot, interval=900)
        plt.show()

    def convert_to_data(self, field):
        redX, redY = [], []
        blueX, blueY = [], []
        obstacleX, obstacleY = [], []
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i, j] < 0:
                    obstacleX.append(i + 0.5)
                    obstacleY.append(j + 0.5)
                if field[i, j] > 0:
                    color = self.units[field[i, j]][0]
                    if color == 'red':
                        redX.append(i + 0.5)
                        redY.append(j + 0.5)
                    else:
                        blueX.append(i + 0.5)
                        blueY.append(j + 0.5)

        return redX, redY, blueX, blueY, obstacleX, obstacleY

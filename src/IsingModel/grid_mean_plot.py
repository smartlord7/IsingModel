from __future__ import division

import numpy as np
import simcx
from matplotlib import pyplot as plt

from game_of_ice import GameOfIce


class GridMeanPlot(simcx.MplVisual):
    def __init__(self, sim: GameOfIce, **kwargs):
        super(GridMeanPlot, self).__init__(sim, **kwargs)

        self.sim = sim
        self.x = [0]
        mean_influences = np.mean(self.sim.sum_inf_neighbours)
        mean_states = np.mean(self.sim.values)
        std_influences = np.std(self.sim.values)

        self.y1 = [mean_influences]
        self.y2 = [mean_states]
        self.y3 = [std_influences]

        self.ax1 = self.figure.add_subplot(111)
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Mean')
        self.ax1.set_xlim(0, 100)

        self._max_time = 100
        self.line1, = self.ax1.plot(self.x, self.y1, label='Influences mean')
        self.line2, = self.ax1.plot(self.x, self.y2,  label='States mean')
        # self.line3, = self.ax1.plot(self.x, self.y3, label='Influences std')
        plt.legend()

        self.update_image()

    def draw(self):

        self.x.append(self.x[-1] + 1)
        mean_influences = np.mean(self.sim.sum_inf_neighbours)
        mean_states = np.mean(self.sim.values)
        std_influences = np.std(self.sim.values)

        self.y1.append(mean_influences)
        self.y2.append(mean_states)
        self.y3.append(std_influences)

        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax1.set_xlim(0, self._max_time)

        min_v = min(min(self.y1), min(self.y2))
        max_v = max(max(self.y1), max(self.y2))

        self.ax1.set_ylim(min_v - 0.01, max_v + 0.01)

        self.line1.set_data(self.x, self.y1)
        self.line2.set_data(self.x, self.y2)
        # self.line3.set_data(self.x, self.y3)

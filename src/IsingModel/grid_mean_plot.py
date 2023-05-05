from __future__ import division
import simcx
from game_of_ice import GameOfIce


class GridMeanPlot(simcx.MplVisual):
    def __init__(self, sim: GameOfIce, **kwargs):
        super(GridMeanPlot, self).__init__(sim, **kwargs)

        self.sim = sim
        self.x = [0]
        width = self.sim.width
        height = self.sim.height
        self.n_grid = width*height
        self.y = [sum(sum(self.sim.sum_inf_neighbours))/self.n_grid]

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Mean')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-1, 1)
        self._max_time = 100
        self.im_data, = self.ax.plot(self.x, self.y)

        self.update_image()

    def draw(self):

        self.x.append(self.x[-1] + 1)
        self.y.append(sum(sum(self.sim.sum_inf_neighbours))/self.n_grid)
        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax.set_xlim(0, self._max_time)

        self.im_data.set_data(self.x, self.y)

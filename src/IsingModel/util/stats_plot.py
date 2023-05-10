from __future__ import division

import simcx
import numpy as np
from game_of_ice import GameOfIce
from matplotlib import pyplot as plt

from metrics import magnetization, energy, correlation


class StatsPlot(simcx.MplVisual):
    def __init__(self, sim: GameOfIce, **kwargs):
        """
        Initializes a StatsPlot instance.

        Parameters:
        -----------
        sim : GameOfIce
            A GameOfIce instance representing the simulation.
        **kwargs : dict
            Additional keyword arguments to pass to the parent class constructor.
        """
        super(StatsPlot, self).__init__(sim, **kwargs)

        # Store the GameOfIce instance
        self.sim = sim
        # Initialize the x and y arrays for the plot
        self.x = [0]
        self.phase_sensitivity = np.mean(self.sim.sum_inf_neighbours)
        self.magnetization_ = magnetization(self.sim.values)
        self.corr = correlation(self.sim.values)
        self.e = energy(self.sim.values)
        self.std = np.std(self.sim.values)

        self.y1 = [self.phase_sensitivity]
        self.y2 = [self.magnetization_]
        self.y3 = [self.std]
        self.y4 = [self.corr]
        self.y5 = [self.e]

        # Create a subplot with the appropriate labels and limits
        self.ax2 = self.figure.add_subplot(3, 1, 1)
        self.ax2.set_xlim([0, self.sim.width])
        self.ax2.set_ylim([0, self.sim.height])
        self.im = self.ax2.imshow(np.transpose(np.rot90(self.sim.sum_inf_neighbours, -1)),
                                  extent=[0, self.sim.width, 0, self.sim.height], cmap='inferno')
        self.color_bar = self.ax2.figure.colorbar(self.im, ax=self.ax2)

        self.ax1 = self.figure.add_subplot(3, 1, 2)
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Mean')
        self.ax1.set_xlim(0, 100)

        self._max_time = 100
        # Initialize the lines for the plot
        if sim.method == 'global':
            self.line1, = self.ax1.plot(self.x, self.y1, label='Phase-sensitivity')
        self.line2, = self.ax1.plot(self.x, self.y2, label='Magnetization')
        self.line4, = self.ax1.plot(self.x, self.y4, label='Correlation')
        # self.line3, = self.ax1.plot(self.x, self.y3, label='Influences self.std')
        plt.legend(fontsize='8')

        self.ax3 = self.figure.add_subplot(3, 1, 3)
        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('Energy')
        self.ax3.set_xlim(0, 100)
        self.line5, = self.ax3.plot(self.x, self.y5, label='Energy')
        plt.legend(fontsize='8')

        self.figure.subplots_adjust(left=0.2, hspace=0.5)
        # Update the image
        self.update_image()

    def draw(self):
        """
        Updates the plot with the latest statistics.
        """
        # Update the x and y arrays with the latest statistics
        self.x.append(self.x[-1] + 1)
        if self.sim.method == 'global':
            self.phase_sensitivity = np.mean(self.sim.sum_inf_neighbours)
        self.magnetization_ = np.mean(self.sim.values)
        self.corr = correlation(self.sim.values)
        self.e = energy(self.sim.values)
        self.std = np.std(self.sim.values)

        if self.sim.method == 'global':
            self.y1.append(self.phase_sensitivity)
        self.y2.append(self.magnetization_)
        # self.y3.append(std_influences)
        self.y4.append(self.corr)
        self.y5.append(self.e)

        # If the maximum time has been reached, increase the maximum time and update the x limit of the plot
        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax1.set_xlim(0, self._max_time)
            self.ax3.set_xlim(0, self._max_time)

        # Update the y limit of the plot based on the current minimum and maximum values of the y arrays
        if self.sim.method == 'global':
            min_v = min(min(self.y1), min(self.y2), min(self.y4))
            max_v = max(max(self.y1), max(self.y2), max(self.y4))
        else:
            min_v = min(min(self.y2), min(self.y4))
            max_v = max(max(self.y2), max(self.y4))


        min_v2 = min(self.y5)
        max_v2 = max(self.y5)

        self.ax1.set_ylim(min_v - 0.03, max_v + 0.03)
        self.ax3.set_ylim(min_v2, max_v2 + 3000)

        # Update the lines of the plot with the new x and y values
        if self.sim.method == 'global':
            self.line1.set_data(self.x, self.y1)
            self.im.set_data(np.transpose(np.rot90(self.sim.sum_inf_neighbours, -1)))
            self.im.set_clim(vmin=np.min(self.sim.sum_inf_neighbours), vmax=np.max(self.sim.sum_inf_neighbours))
            self.ax2.autoscale()
        self.line2.set_data(self.x, self.y2)
        self.line4.set_data(self.x, self.y4)
        self.line5.set_data(self.x, self.y5)
        # self.line3.set_data(self.x, self.y3)

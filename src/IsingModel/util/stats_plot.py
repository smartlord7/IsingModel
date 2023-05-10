from __future__ import division

import simcx
import numpy as np
from game_of_ice import GameOfIce
from matplotlib import pyplot as plt


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
        mean_influences = np.mean(self.sim.sum_inf_neighbours)
        mean_states = np.mean(self.sim.values)
        std_influences = np.std(self.sim.values)

        self.y1 = [mean_influences]
        self.y2 = [mean_states]
        self.y3 = [std_influences]

        # Create a subplot with the appropriate labels and limits
        self.ax1 = self.figure.add_subplot(3, 1, 1)
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Mean')
        self.ax1.set_xlim(0, 100)

        self._max_time = 100
        # Initialize the lines for the plot
        if sim.method == 'global':
            self.line1, = self.ax1.plot(self.x, self.y1, label='Influences mean')
        self.line2, = self.ax1.plot(self.x, self.y2,  label='States mean')
        # self.line3, = self.ax1.plot(self.x, self.y3, label='Influences std')
        plt.legend()

        self.ax2 = self.figure.add_subplot(2, 1, 2)
        self.im = self.ax2.imshow(np.transpose(np.rot90(self.sim.sum_inf_neighbours, -1)), cmap='inferno')
        self.color_bar = self.ax2.figure.colorbar( self.im, ax=self.ax2)
        self.figure.subplots_adjust(hspace=0.3)

        # Update the image
        self.update_image()

    def draw(self):
        """
        Updates the plot with the latest statistics.
        """
        # Update the x and y arrays with the latest statistics
        self.x.append(self.x[-1] + 1)
        if self.sim.method == 'global':
            mean_influences = np.mean(self.sim.sum_inf_neighbours)
        mean_states = np.mean(self.sim.values)
        # std_influences = np.std(self.sim.values)

        if self.sim.method == 'global':
            self.y1.append(mean_influences)
        self.y2.append(mean_states)
        # self.y3.append(std_influences)

        # If the maximum time has been reached, increase the maximum time and update the x limit of the plot
        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax1.set_xlim(0, self._max_time)

        # Update the y limit of the plot based on the current minimum and maximum values of the y arrays
        if self.sim.method == 'global':
            min_v = min(min(self.y1), min(self.y2))
            max_v = max(max(self.y1), max(self.y2))
        else:
            min_v = min(self.y2)
            max_v = max(self.y2)

        self.ax1.set_ylim(min_v - 0.03, max_v + 0.03)

        # Update the lines of the plot with the new x and y values
        if self.sim.method == 'global':
            self.line1.set_data(self.x, self.y1)
            self.im.set_data(np.transpose(np.rot90(self.sim.sum_inf_neighbours, -1)))
            self.im.set_clim(vmin=np.min(self.sim.sum_inf_neighbours), vmax=np.max(self.sim.sum_inf_neighbours))
            self.ax2.autoscale()
        self.line2.set_data(self.x, self.y2)
        # self.line3.set_data(self.x, self.y3)

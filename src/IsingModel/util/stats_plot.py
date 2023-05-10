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
        self.ax1 = self.figure.add_subplot(111)
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Mean')
        self.ax1.set_xlim(0, 100)

        self._max_time = 100
        # Initialize the lines for the plot
        self.line1, = self.ax1.plot(self.x, self.y1, label='Influences mean')
        self.line2, = self.ax1.plot(self.x, self.y2,  label='States mean')
        # self.line3, = self.ax1.plot(self.x, self.y3, label='Influences std')
        plt.legend()

        # Update the image
        self.update_image()

    def draw(self):
        """
        Updates the plot with the latest statistics.
        """
        # Update the x and y arrays with the latest statistics
        self.x.append(self.x[-1] + 1)
        mean_influences = np.mean(self.sim.sum_inf_neighbours)
        mean_states = np.mean(self.sim.values)
        std_influences = np.std(self.sim.values)

        self.y1.append(mean_influences)
        self.y2.append(mean_states)
        self.y3.append(std_influences)

        # If the maximum time has been reached, increase the maximum time and update the x limit of the plot
        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax1.set_xlim(0, self._max_time)

        # Update the y limit of the plot based on the current minimum and maximum values of the y arrays
        min_v = min(min(self.y1), min(self.y2))
        max_v = max(max(self.y1), max(self.y2))
        self.ax1.set_ylim(min_v - 0.01, max_v + 0.01)

        # Update the lines of the plot with the new x and y values
        self.line1.set_data(self.x, self.y1)
        self.line2.set_data(self.x, self.y2)
        # self.line3.set_data(self.x, self.y3)

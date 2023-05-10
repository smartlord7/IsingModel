# -*- coding: utf-8 -*-

# Import necessary modules
from __future__ import division

from typing import Callable, Any

import numpy as np
import simcx
from scipy import signal

from perturbations import perturb_circle
from util.graphic_util import *
from distribution_functions import *

__docformat__ = 'restructuredtext'
__author__ = 'David Ressurreição & Sancho Simões (based on the original GameOfLife - Tiago Batista)'


class GameOfIce(simcx.Simulator):
    """
    A Game of Ice simulator.

    Parameters:
    -----------
    width : int, optional (default=50)
        Width of the grid.
    height : int, optional (default=50)
        Height of the grid.
    neighbourhood_size : int, optional (default=1)
        Size of the neighbourhood for each cell.
    method : str, optional (default='global')
        Method used to update the grid. Can be 'global' or 'local'.
    initial_temperature : float, optional (default=1.0)
        Initial temperature of the simulation.
    n_temperature_decay_steps : int, optional (default=100)
        Number of temperature decay steps.
    coupling_constant : float, optional (default=1.0)
        Coupling constant used in the local field calculation.
    dist_func : str, optional (default='gaussian')
        Distribution function used to create the initial grid.
    func_config : dict, optional (default=None)
        Configuration dictionary for the distribution function.
    boundary : str, optional (default='fill')
        Boundary condition used in the convolution.
    fill : int, optional (default=0)
        Fill value used in the convolution.

    """

    # Default parameter values
    DEFAULT_WIDTH = 50
    DEFAULT_HEIGHT = 50
    DEFAULT_NEIGHBOUR_SIZE = 1
    DEFAULT_METHOD = 'global'
    DEFAULT_DIST_FUNC = 'gaussian'
    DEFAULT_BOUNDARY = 'fill'
    DEFAULT_FILL = 0
    DEFAULT_INITIAL_TEMPERATURE = 1.0
    DEFAULT_COUPLING_CONSTANT = 1.0
    DEFAULT_N_TEMPERATURE_DECAY_STEPS = 100
    DEFAULT_PERTURBATION_FUNCTION = perturb_circle

    def __init__(self,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT,
                 neighbourhood_size: int = DEFAULT_NEIGHBOUR_SIZE,
                 method: str = DEFAULT_METHOD,
                 initial_temperature: float = DEFAULT_INITIAL_TEMPERATURE,
                 n_temperature_decay_steps: int = DEFAULT_N_TEMPERATURE_DECAY_STEPS,
                 perturbation_function: Callable[[np.ndarray, int, int, int, int], Any] = DEFAULT_PERTURBATION_FUNCTION,
                 coupling_constant: float = DEFAULT_COUPLING_CONSTANT,
                 dist_func: str = DEFAULT_DIST_FUNC,
                 func_config: dict = None,
                 boundary: str = DEFAULT_BOUNDARY,
                 fill: int = DEFAULT_FILL):
        super(GameOfIce, self).__init__()

        # Set the simulation parameters
        self.width = width
        self.height = height
        self.neighbourhood_size = neighbourhood_size
        self.method = method
        self.temperature = initial_temperature
        self.n_temperature_decay_steps = n_temperature_decay_steps
        self.perturbation_function = perturbation_function
        self.temperature_decay_step = self.temperature / self.n_temperature_decay_steps
        self.coupling_constant = coupling_constant
        self.values = np.zeros((self.height, self.width))
        self.boundary = boundary
        self.fill = fill
        self.sum_inf_neighbours = np.zeros((self.height, self.width))

        # Create grid and perform distribution function
        center_x, center_y = np.array((height, width)) // 2
        x, y, mesh = create_mesh2d(width, height, mn=0, mx=width)

        if dist_func == 'gaussian':
            std = (width ** (1 / 2), height ** (1 / 2))

            if func_config is not None:
                std = func_config['std']

            grid = gaussian(mesh, mean=(center_x, center_y), std=std)
        elif dist_func == 'exp_decay':
            decay_rate = (((height + width) / 2) ** (1 / 2))

            if func_config is not None:
                decay_rate = func_config['decay_rate']

            grid = exp_decay(mesh, center=(center_x, center_y), decay_rate=decay_rate)
        elif dist_func == 'normal':
            grid = np.ones((height, width))
        elif dist_func == "rayleigh":
            grid = rayleigh(mesh, center=(center_x, center_y), sigma=5.0)
        elif dist_func == "log_normal":
            grid = log_normal_distribution(mesh, center=(center_x, center_y), sigma=1.0, mu=0.0)

        grid[center_x, center_y] = 0  # reset the center cell
        sm = np.sum(grid)  # normalize so that the sum is ~ 1
        grid /= sm

        # Extract a sub-grid from the modified grid
        sub_grid_size = (neighbourhood_size, neighbourhood_size)
        sub_grid_x, sub_grid_y = sub_grid_size[0], sub_grid_size[1]
        neighbour_init = grid[center_x - sub_grid_x:center_x + sub_grid_x + 1,
                         center_y - sub_grid_y:center_y + sub_grid_y + 1]

        self.neighbourhood = neighbour_init
        self.dirty = False

    def local_field(self, i, j):
        """
        Calculate the local field for a given cell.

        Parameters:
        -----------
        i : int
            Row index of the cell.
        j : int
            Column index of the cell.

        Returns:
        --------
        float
            Local field value.
        """
        top = self.values[(i - 1) % self.height, j]
        bottom = self.values[(i + 1) % self.height, j]
        left = self.values[i, (j - 1) % self.width]
        right = self.values[i, (j + 1) % self.width]

        return self.coupling_constant * (top + bottom + left + right)

    def local_prob_switch(self, i, j):
        """
        Calculate the probability of a cell switching its state based on the local field and the current temperature.

        Parameters:
        -----------
        i : int
            Row index of the cell.
        j : int
            Column index of the cell.

        Returns:
        --------
        float
            Probability of the cell switching its state.
        """
        t = self.temperature
        e = -self.local_field(i, j) * self.values[i, j]

        return np.exp(-e / t) / (np.exp(-e / t) + np.exp(e / t))  # boltzmann distribution

    def random(self, prob):
        """
        Initialize the grid with random values based on a given probability.

        Parameters:
        -----------
        prob : float
            Probability of a cell being alive.
        """
        self.values = np.random.choice((-1, +1), (self.height, self.width),
                                       p=(1 - prob, prob))
        self.dirty = True

    def add_block(self, block, pos_x, pos_y):
        """
        Add a block of cells to the grid at a given position.

        Parameters:
        -----------
        block : numpy.ndarray
            Block of cells to add to the grid.
        pos_x : int
            X-coordinate of the position to add the block.
        pos_y : int
            Y-coordinate of the position to add the block.
        """
        height, width = block.shape

        for y in range(height):
            for x in range(width):
                self.values[pos_y + y, pos_x + x] = block[y, x]

        self.dirty = True

    def step(self, delta=0):
        """
        Update the grid by applying the Game of Life rules.
        """
        if self.temperature - self.temperature_decay_step > 0:
            self.temperature -= self.temperature_decay_step

        if self.method == 'global':
            self.sum_inf_neighbours = signal.convolve2d(self.values, self.neighbourhood,
                                                        mode='same', boundary=self.boundary, fillvalue=self.fill)

        if self.method == 'global':
            n = self.sum_inf_neighbours
            mask1 = np.random.random(size=n.shape) < n
            mask2 = -np.random.random(size=n.shape) > n
            self.values[mask1 & (n > 0)] = +1
            self.values[mask2] = -1
        elif self.method == 'local':
            inf = self.local_field(np.arange(self.height)[:, None], np.arange(self.width))
            e = -inf * self.values
            p = np.exp(-e / self.temperature) / (np.exp(-e / self.temperature) + np.exp(e / self.temperature))
            mask = np.random.rand(*self.values.shape) < p
            self.values[mask] = -self.values[mask]

        self.dirty = True

    def perturbate(self,
                   x: int,
                   y: int,
                   radius: int,
                   value: int):
        """
        Puts a block at the specified coordinates.

        Parameters:
        -----------
        x : int
            The x coordinate of the center of the peeturbation.
        y : int
            The y coordinate of the center of the peeturbation.
        """

        self.perturbation_function(self.values, x, y, radius, value)

# -*- coding: utf-8 -*- ----------------------------------------------------------------------------- Copyright (c)
# 2022-2023 David Ressurreição & Sancho Simões (based on the original GameOfLife from 2015-2016 - Tiago Batista) All
# rights reserved. -----------------------------------------------------------------------------

'''
Game of Life example using the simcx framework.

'''

from __future__ import division

import simcx
from scipy import signal
from util.graphic_util import *
from distribution_functions import *

__docformat__ = 'restructuredtext'
__author__ = 'David Ressurreição & Sancho Simões (based on the original GameOfLife - Tiago Batista)'


class GameOfIce(simcx.Simulator):
    '''A Game of Ice simulator.'''

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

    def __init__(self,

                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT,
                 neighbourhood_size: int = DEFAULT_NEIGHBOUR_SIZE,
                 method: str = 'global',
                 initial_temperature: float = DEFAULT_INITIAL_TEMPERATURE,
                 n_temperature_decay_steps: int = DEFAULT_N_TEMPERATURE_DECAY_STEPS, # as if
                 coupling_constant: float = DEFAULT_COUPLING_CONSTANT,
                 dist_func: str = DEFAULT_DIST_FUNC,
                 func_config: dict = None,
                 boundary: str = 'fill',
                 fill: int = DEFAULT_FILL):
        super(GameOfIce, self).__init__()

        self.width = width
        self.height = height
        self.neighbourhood_size = neighbourhood_size
        self.method = method
        self.temperature = initial_temperature
        self.n_temperature_decay_steps = n_temperature_decay_steps
        self.temperature_decay_step = self.temperature / self.n_temperature_decay_steps
        self.coupling_constant = coupling_constant
        self.values = np.zeros((self.height, self.width))
        self.boundary = boundary
        self.fill = fill
        self.sum_inf_neighbours = np.zeros((self.height, self.width))

        # Create grid and perform gaussian function

        # Replace the center to 0
        center_x, center_y = np.array((height, width)) // 2
        x, y, mesh = create_mesh2d(width, height, mn=0, mx=width)

        if dist_func == 'gaussian':
            std = (width ** (1 / 2), height ** (1 / 2))

            if func_config is not None:
                std = func_config['std']

            grid = gaussian(mesh, mean=(center_x, center_y), std=std)
            # grid += center_value / (width * height - 1) # increase equally to the remaining cells
        elif dist_func == 'exp_decay':
            decay_rate = (((height + width) / 2) ** (1 / 2))

            if func_config is not None:
                decay_rate = func_config['decay_rate']

            grid = exp_decay(mesh, center=(center_x, center_y), decay_rate=decay_rate)
            # grid += center_value / (width * height - 1) # increase equally to the remaining cells
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
        sub_grid_size = (neighbourhood_size, neighbourhood_size)  # set the desired size of the sub-grid
        sub_grid_x, sub_grid_y = sub_grid_size[0], sub_grid_size[1]
        neighbour_init = grid[center_x - sub_grid_x:center_x + sub_grid_x + 1,
                         center_y - sub_grid_y:center_y + sub_grid_y + 1]

        # print(neighbour_init)

        self.neighbourhood = neighbour_init
        self.dirty = False

    def local_field(self, i, j):
        top = self.values[(i - 1) % self.height, j]
        bottom = self.values[(i + 1) % self.height, j]
        left = self.values[i, (j - 1) % self.width]
        right = self.values[i, (j + 1) % self.width]

        return self.coupling_constant * (top + bottom + left + right)

    def local_prob_switch(self, i, j):
        t = self.temperature
        e = -self.local_field(i, j) * self.values[i, j]

        return np.exp(-e / t) / (np.exp(-e / t) + np.exp(e / t)) # boltzmann distribution

    def random(self, prob):
        self.values = np.random.choice((-1, +1), (self.height, self.width),
                                       p=(1 - prob, prob))
        self.dirty = True

    def add_block(self, block, pos_x, pos_y):
        height, width = block.shape

        for y in range(height):
            for x in range(width):
                self.values[pos_y + y, pos_x + x] = block[y, x]

        self.dirty = True

    def step(self, delta=0):
        if self.temperature - self.temperature_decay_step > 0: # linear temperature annealing
            self.temperature -= self.temperature_decay_step
        print(self.temperature)

        if self.method == 'global':
            self.sum_inf_neighbours = signal.convolve2d(self.values, self.neighbourhood,
                                                        mode='same', boundary=self.boundary, fillvalue=self.fill)
        for y in range(self.height):
            for x in range(self.width):
                if self.method == 'global':
                    n = self.sum_inf_neighbours[y, x]
                    # if n > 0: print(n)
                    if np.random.random() < n and n > 0:
                        self.values[y, x] = +1
                    elif -np.random.random() > n:
                        self.values[y, x] = -1
                elif self.method == 'local':
                    p = self.local_prob_switch(y, x)
                    if np.random.rand() < p:
                        self.values[y, x] = -self.values[y, x]

        self.dirty = True

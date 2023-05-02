# -*- coding: utf-8 -*- ----------------------------------------------------------------------------- Copyright (c)
# 2022-2023 David Ressurreição & Sancho Simões (based on the original GameOfLife from 2015-2016 - Tiago Batista) All
# rights reserved. -----------------------------------------------------------------------------

"""
Game of Life example using the simcx framework.

"""

from __future__ import division

import simcx
import pyglet
import matplotlib
from scipy import signal
from graphic_util import *
from distribution_functions import *

__docformat__ = 'restructuredtext'
__author__ = 'David Ressurreição & Sancho Simões (based on the original GameOfLife - Tiago Batista)'


class GameOfIce(simcx.Simulator):
    """A Game of Life simulator."""

    def __init__(self, width=50, height=50, neighbour_size=1, func="gaussian"):
        super(GameOfIce, self).__init__()
        self.width = width
        self.height = height
        self.values = np.zeros((self.height, self.width))

        # Create grid and perform gaussian function

        # Replace the center to 0
        center_x, center_y = np.array((width, height)) // 2
        x, y, mesh = create_mesh2d(width, height, min=0, max=width)
        if func == "gaussian":
            grid = gaussian(mesh, mean=(center_x, center_y), std=(width ** (1 / 2), height ** (1 / 2)))
        elif func == "exp":
            grid = exp_decay(mesh, center=(center_x, center_y), decay_rate=(width ** (1 / 2)))
        sm = np.sum(grid)
        grid /= sm
        grid[center_x, center_y] = 0

        # Extract a sub-grid from the modified grid
        sub_grid_size = (neighbour_size, neighbour_size)  # set the desired size of the sub-grid
        sub_grid_x, sub_grid_y = sub_grid_size[0], sub_grid_size[1]
        neighbour_init = grid[center_x - sub_grid_x:center_x + sub_grid_x + 1,
                         center_y - sub_grid_y:center_y + sub_grid_y + 1]

        print(neighbour_init)

        self.neighbourhood = neighbour_init
        self.dirty = False

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
        sum_inf_neighbours = signal.convolve2d(self.values, self.neighbourhood,
                                               mode='same', boundary='wrap')
        for y in range(self.height):
            for x in range(self.width):
                n = sum_inf_neighbours[y, x]
                if n > 0: print(n)
                if np.random.random() < n and n > 0:
                    self.values[y, x] = +1
                elif -np.random.random() > n:
                    self.values[y, x] = -1

        self.dirty = True


class Grid2D(simcx.Visual):
    QUAD_BLACK = (0, 0, 0) * 4
    QUAD_WHITE = (255, 255, 255) * 4

    def __init__(self, sim: simcx.Simulator, cell_size=20):
        super(Grid2D, self).__init__(sim, width=sim.width * cell_size,
                                     height=sim.height * cell_size)

        self._grid_width = sim.width
        self._grid_height = sim.height

        # create graphics objects
        self._batch = pyglet.graphics.Batch()
        self._grid = []
        for y in range(self._grid_height):
            self._grid.append([])
            for x in range(self._grid_width):
                vertex_list = self._batch.add(4, pyglet.gl.GL_QUADS, None,
                                              ('v2i',
                                               (x * cell_size, y * cell_size,
                                                x * cell_size + cell_size,
                                                y * cell_size,
                                                x * cell_size + cell_size,
                                                y * cell_size + cell_size,
                                                x * cell_size,
                                                y * cell_size + cell_size)),
                                              ('c3B', self.QUAD_BLACK))
                self._grid[y].append(vertex_list)

    def draw(self):
        if self.sim.dirty:
            self._update_graphics()
        self._batch.draw()

    def _update_graphics(self):
        for y in range(self._grid_height):
            for x in range(self._grid_width):
                if self.sim.values[y, x] == 1:
                    self._grid[y][x].colors[:] = self.QUAD_WHITE
                else:
                    self._grid[y][x].colors[:] = self.QUAD_BLACK


if __name__ == '__main__':
    # Example patterns
    matplotlib.use('TkAgg')
    cell = np.array([[-1, 1, -1], [-1, 1, -1], [-1, -1, -1]])

    gol = GameOfIce(50, 50, 25)
    gol.random(0.505)
    # gol.add_block(glider, 10, 10)
    # gol.add_block(glider, 30, 30)

    # gol.add_block(glider, 10, 10)
    # gol.add_block(glider, 5, 5)
    vis = Grid2D(gol, 10)

    display = simcx.Display(interval=0.025)
    display.add_simulator(gol)
    display.add_visual(vis)
    simcx.run()

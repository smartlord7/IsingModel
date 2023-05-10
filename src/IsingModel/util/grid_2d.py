import pyglet
import simcx


class Grid2D(simcx.Visual):
    """
    A class for visualizing a 2D grid of cells using Pyglet.

    Parameters:
    -----------
    sim : simcx.Simulator
        The simulator object that contains the grid of cells to be visualized.
    cell_size : int, optional
        The size of each cell in pixels. Default is 20.

    Attributes:
    -----------
    _grid_width : int
        The width of the grid.
    _grid_height : int
        The height of the grid.
    _batch : pyglet.graphics.Batch
        A Pyglet batch object used to efficiently draw the graphics objects.
    _grid : list
        A 2D list that stores the graphics objects for each cell in the grid.

    Methods:
    --------
    draw()
        Draws the graphics objects to the screen.
    _update_graphics()
        Updates the graphics objects to reflect the current state of the grid.
    """

    # Colors for the cells
    QUAD_BLACK = (0, 0, 0) * 4
    QUAD_WHITE = (255, 255, 255) * 4

    def __init__(self, sim: simcx.Simulator, cell_size=20):
        """
        Initializes the Grid2D object.

        Parameters:
        -----------
        sim : simcx.Simulator
            The simulator object that contains the grid of cells to be visualized.
        cell_size : int, optional
            The size of each cell in pixels. Default is 20.
        """

        # Call the parent constructor
        super(Grid2D, self).__init__(sim, width=sim.width * cell_size,
                                      height=sim.height * cell_size)

        # Store the grid dimensions
        self._grid_width = sim.width
        self._grid_height = sim.height

        # Create graphics objects
        self._batch = pyglet.graphics.Batch()
        self._grid = []

        for y in range(self._grid_height):
            self._grid.append([])
            for x in range(self._grid_width):
                # Create a vertex list for each cell
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
        """
        Draws the graphics objects to the screen.
        """

        # Update the graphics if the simulation has changed
        if self.sim.dirty:
            self._update_graphics()

        # Draw the graphics objects
        self._batch.draw()

    def _update_graphics(self):
        """
        Updates the graphics objects to reflect the current state of the grid.
        """

        for y in range(self._grid_height):
            for x in range(self._grid_width):
                # Set the color of the cell based on its state
                if self.sim.values[y, x] == 1:
                    self._grid[y][x].colors[:] = self.QUAD_WHITE
                else:
                    self._grid[y][x].colors[:] = self.QUAD_BLACK

from simcx import Display
from game_of_ice import GameOfIce


class CustomDisplay(Display):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SPREAD_DURATION = 0.1

    def __init__(self,
                 sim: GameOfIce,
                 x_min: int,
                 x_max: int,
                 y_min: int,
                 y_max: int,
                 cell_size: int,
                 width=500,
                 height=500,
                 interval=0.05,
                 multi_sampling=True,
                 **kwargs):
        """
        Initializes a CustomDisplay instance.

        Parameters:
        -----------
        sim : GameOfIce
            A GameOfIce instance representing the simulation.
        x_min : int
            The minimum x coordinate of the display.
        x_max : int
            The maximum x coordinate of the display.
        y_min : int
            The minimum y coordinate of the display.
        y_max : int
            The maximum y coordinate of the display.
        cell_size : int
            The size of each cell in the display.
        width : int, optional
            The width of the display in pixels (default is 500).
        height : int, optional
            The height of the display in pixels (default is 500).
        interval : float, optional
            The time interval between frames in seconds (default is 0.05).
        multi_sampling : bool, optional
            Whether to use multi-sampling to improve the display quality (default is True).
        **kwargs : dict
            Additional keyword arguments to pass to the parent class constructor.
        """
        super().__init__(width, height, interval, multi_sampling, **kwargs)

        self.sim = sim
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.cell_size = cell_size

    def put_ice_block(self,
                      x: int,
                      y: int,
                      side: int = None):
        """
        Puts an ice block at the specified coordinates.

        Parameters:
        -----------
        x : int
            The x coordinate of the center of the ice block.
        y : int
            The y coordinate of the center of the ice block.
        side : int, optional
            The side length of the ice block in cells (default is None).
        """
        if side == None:
            side = int(min(self.sim.height, self.sim.width) / 10)

        # Calculate the coordinates of the top-left corner of the square
        start_x = ((x - self.x_min) // self.cell_size) - side // 2
        start_y = ((y - self.y_min) // self.cell_size) - side // 2
        # Fill the square with -1
        self.sim.values[start_x:start_x + side, start_y:start_y + side] = -1

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handles mouse press events.

        Parameters:
        -----------
        x : int
            The x coordinate of the mouse click.
        y : int
            The y coordinate of the mouse click.
        button : int
            The button that was pressed (1 for left, 2 for middle, 3 for right).
        modifiers : int
            The modifier keys that were pressed (bitwise OR of constants like pyglet.window.key.MOD_SHIFT).
        """
        if self.x_min < x < self.x_max and self.y_min < y < self.y_max:
            print(f"Mouse button {button} pressed at ({x}, {y})")
            self.put_ice_block(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Handles mouse release events.

        Parameters:
        -----------
        x : int
            The x coordinate of the mouse click.
        y : int
            The y coordinate of the mouse click.
        button : int
            The button that was released (1 for left, 2 for middle, 3 for right).
        modifiers : int
            The modifier keys that were pressed (bitwise OR of constants like pyglet.window.key.MOD_SHIFT).
        """
        if self.x_min < x < self.x_max and self.y_min < y < self.y_max:
            print(f"Mouse button {button} released at ({x}, {y})")

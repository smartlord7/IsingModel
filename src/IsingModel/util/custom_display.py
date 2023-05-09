import math

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
        super().__init__(width, height, interval, multi_sampling, **kwargs)
        self.show_fps = True

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
        if side == None:
            side = int(min(self.sim.height, self.sim.width) / 10)

        # Calculate the coordinates of the top-left corner of the square
        start_x = ((x - self.x_min) // self.cell_size) - side // 2
        start_y = ((y - self.y_min) // self.cell_size) - side // 2
        # Fill the square with -1
        self.sim.values[start_x:start_x + side, start_y:start_y + side] = -1

    def on_mouse_press(self, x, y, button, modifiers):
        if self.x_min < x < self.x_max and self.y_min < y < self.y_max:
            print(f"Mouse button {button} pressed at ({x}, {y})")
            self.put_ice_block(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.x_min < x < self.x_max and self.y_min < y < self.y_max:
            print(f"Mouse button {button} released at ({x}, {y})")

import matplotlib
import numpy as np
import simcx
from game_of_ice import Grid2D, GameOfIce
from grid_mean_plot import GridMeanPlot


def main():
    # Example patterns
    matplotlib.use('TkAgg')
    # FUNCTIONS: exp / gaussian / ...
    func_config = {
        'decay_rate': 4
    }
    goi = GameOfIce(50, 50, 25, "exp", func_config)
    goi.random(0.5)

    vis = Grid2D(goi, 10)
    vis2 = GridMeanPlot(goi, width=500, height=200)

    display = simcx.Display(interval=0.1)
    display.add_simulator(goi)
    display.add_visual(vis, 0, 200)
    display.add_visual(vis2)
    simcx.run()


if __name__ == '__main__':
    main()

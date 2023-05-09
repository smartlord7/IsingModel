import simcx
import matplotlib
from game_of_ice import Grid2D, GameOfIce
from grid_mean_plot import GridMeanPlot


def main():
    # Example patterns
    matplotlib.use('TkAgg')
    # FUNCTIONS: exp / gaussian / ...
    func_config = {
        'decay_rate': 1
    }
    GRID_WIDTH_CELLS = 400
    GRID_HEIGHT_CELLS = 400
    NEIGHBOURHOOD_SIZE = 1
    PROB_GENERATION = 0.5
    CELL_SIZE = 2
    GRID_MEAN_PLOT_WIDTH = GRID_WIDTH_CELLS * CELL_SIZE
    GRID_MEAN_PLOT_HEIGHT = int(GRID_HEIGHT_CELLS / CELL_SIZE)

    goi = GameOfIce(width=GRID_WIDTH_CELLS,
                    height=GRID_HEIGHT_CELLS,
                    neighbour_size=NEIGHBOURHOOD_SIZE,
                    func="exp_decay",
                    func_config=func_config)

    goi.random(PROB_GENERATION)

    vis = Grid2D(goi, CELL_SIZE)
    vis2 = GridMeanPlot(goi,
                        width=GRID_MEAN_PLOT_WIDTH,
                        height=GRID_MEAN_PLOT_HEIGHT)

    display = simcx.Display(interval=0.1)
    display.add_simulator(goi)
    display.add_visual(vis, 0, 200)
    display.add_visual(vis2)
    simcx.run()


if __name__ == '__main__':
    main()

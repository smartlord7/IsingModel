import simcx
from game_of_ice import GameOfIce
from util.grid_2d import Grid2D
from util.stats_plot import StatsPlot
from util.custom_display import CustomDisplay


def main():
    # Example patterns
    # FUNCTIONS: exp / gaussian / ...
    func_config = {
        'decay_rate': 1
    }
    GRID_WIDTH_CELLS = 200
    GRID_HEIGHT_CELLS = 200
    NEIGHBOURHOOD_SIZE = 200
    PROB_GENERATION = 0.5
    CELL_SIZE = 2
    GRID_MEAN_PLOT_WIDTH = GRID_WIDTH_CELLS * CELL_SIZE
    GRID_MEAN_PLOT_HEIGHT = 200

    goi = GameOfIce(width=GRID_WIDTH_CELLS,
                    height=GRID_HEIGHT_CELLS,
                    neighbourhood_size=NEIGHBOURHOOD_SIZE,
                    initial_temperature=300,
                    dist_func='exp_decay',
                    method="global",
                    fill=-1)

    goi.random(PROB_GENERATION)

    vis = Grid2D(goi, CELL_SIZE)
    vis2 = StatsPlot(goi,
                     width=GRID_MEAN_PLOT_WIDTH,
                     height=GRID_MEAN_PLOT_HEIGHT)

    display = CustomDisplay(goi,
                            x_min=0,
                            x_max=CELL_SIZE * GRID_WIDTH_CELLS,
                            y_min=GRID_MEAN_PLOT_HEIGHT,
                            y_max=GRID_MEAN_PLOT_HEIGHT + CELL_SIZE * GRID_HEIGHT_CELLS,
                            cell_size=CELL_SIZE,
                            interval=0.0001)
    display.add_simulator(goi)
    display.add_visual(vis, 0, 200)
    display.add_visual(vis2)
    simcx.run()


if __name__ == '__main__':
    main()

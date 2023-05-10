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
    GRID_WIDTH_CELLS = 50
    GRID_HEIGHT_CELLS = 50
    NEIGHBOURHOOD_SIZE = 200
    PROB_GENERATION = 0.5
    CELL_SIZE = 4
    GRID_STATS_PLOT_WIDTH = GRID_WIDTH_CELLS * CELL_SIZE
    GRID_STATS_PLOT_HEIGHT = 200

    goi = GameOfIce(width=GRID_WIDTH_CELLS,
                    height=GRID_HEIGHT_CELLS,
                    neighbourhood_size=NEIGHBOURHOOD_SIZE,
                    initial_temperature=300,
                    dist_func='gaussian',
                    method="global",
                    fill=0)

    goi.random(PROB_GENERATION)

    vis = Grid2D(goi, CELL_SIZE)
    vis2 = StatsPlot(goi,
                     width=GRID_STATS_PLOT_WIDTH,
                     height=GRID_STATS_PLOT_HEIGHT)

    display = CustomDisplay(goi,
                            x_min=0,
                            x_max=CELL_SIZE * GRID_WIDTH_CELLS,
                            y_min=GRID_STATS_PLOT_WIDTH,
                            y_max=GRID_STATS_PLOT_HEIGHT + CELL_SIZE * GRID_HEIGHT_CELLS,
                            cell_size=CELL_SIZE,
                            interval=0.1)
    display.add_simulator(goi)
    display.add_visual(vis, 0, 200)
    display.add_visual(vis2)
    simcx.run()


if __name__ == '__main__':
    main()

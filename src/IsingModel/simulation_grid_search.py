from time import perf_counter

import simcx

from game_of_ice import GameOfIce
from perturbations import perturb_circle
from util.grid_2d import Grid2D
from util.stats_plot import StatsPlot
from util.custom_display import CustomDisplay


def main():
    # Example patterns
    # FUNCTIONS: exp / gaussian / ...
    func_config = {
        'decay_rate': 1
    }
    # Set the size of the grid
    GRID_WIDTH_CELLS = 100
    GRID_HEIGHT_CELLS = 100
    curr_time = perf_counter()
    LOG_FILE_PATH = str(curr_time) + 'output.log'
    LOG_FILE_HEADER = 'neighbourhood,prob_generation,method,coupling_constant,initial_temperature,dist_function,boundary,fill\n'

    # Set the size of the cells in the visualization
    CELL_SIZE = 2

    # Set the size of the stats plot
    GRID_STATS_PLOT_WIDTH = GRID_WIDTH_CELLS * CELL_SIZE
    GRID_STATS_PLOT_HEIGHT = 200

    # Set the size of the neighborhood
    NEIGHBOURHOOD_SIZE = [GRID_HEIGHT_CELLS // 8, GRID_HEIGHT_CELLS // 2, GRID_HEIGHT_CELLS]
    # Set the probability of generating a spin up
    PROB_GENERATION = [0.25, 0.50, 0.75]
    COUPLING_CONSTANT = [0.1, 1.0, 4.0]
    METHOD = ['global', 'local']
    INITIAL_TEMPERATURE = [300, 20]
    DIST_FUNCTION = ['gaussian']
    BOUNDARY = ['wrap', 'fill']
    FILL = [-1, 0, 1]

    with open(LOG_FILE_PATH, 'w') as f:
        f.write(LOG_FILE_HEADER)

        for neighbourhood_size in NEIGHBOURHOOD_SIZE:
            for prob_generation in PROB_GENERATION:
                for method in METHOD:
                    for coupling_constant in COUPLING_CONSTANT:
                        for initial_temperature in INITIAL_TEMPERATURE:
                            for dist_function in DIST_FUNCTION:
                                for boundary in BOUNDARY:
                                    for fill in FILL:
                                        screenshot_name = 'Neigh%dProb%.2fMethod%s' % (neighbourhood_size,
                                                                                       prob_generation,
                                                                                       method)
                                        if method == 'local':
                                            screenshot_name += 'Coup%.1fTemp%.1f' % (coupling_constant,
                                                                                       initial_temperature)
                                        screenshot_name += 'Dist%sBound%s' % (dist_function, boundary)

                                        if boundary == 'fill':
                                            screenshot_name += 'Fill%d' % fill

                                        goi = GameOfIce(width=GRID_WIDTH_CELLS,
                                                        height=GRID_HEIGHT_CELLS,
                                                        neighbourhood_size=neighbourhood_size,
                                                        perturbation_function=perturb_circle,
                                                        coupling_constant=coupling_constant,
                                                        method=method,
                                                        initial_temperature=initial_temperature,
                                                        dist_func=dist_function,
                                                        boundary=boundary,
                                                        fill=fill)

                                        # Generate a random spin configuration
                                        goi.random(prob_generation)

                                        # Create a Grid2D instance to visualize the grid
                                        vis = Grid2D(goi, CELL_SIZE)
                                        # Create a StatsPlot instance to plot the statistics
                                        vis2 = StatsPlot(goi,
                                                         width=GRID_STATS_PLOT_WIDTH,
                                                         height=GRID_STATS_PLOT_HEIGHT)

                                        # Create a CustomDisplay instance to display the simulation
                                        display = CustomDisplay(goi,
                                                                vis,
                                                                screenshot_name,
                                                                x_min=0,
                                                                x_max=CELL_SIZE * GRID_WIDTH_CELLS,
                                                                y_min=GRID_STATS_PLOT_HEIGHT,
                                                                y_max=GRID_STATS_PLOT_HEIGHT + CELL_SIZE * GRID_HEIGHT_CELLS,
                                                                cell_size=CELL_SIZE,
                                                                interval=0.1)
                                        # Add the GameOfIce instance, the Grid2D instance, and the StatsPlot instance to
                                        # the display
                                        display.add_simulator(goi)
                                        display.add_visual(vis, 0, GRID_STATS_PLOT_HEIGHT)
                                        display.add_visual(vis2)
                                        # Run the simulation using the simcx library
                                        simcx.run()


if __name__ == '__main__':
    main()

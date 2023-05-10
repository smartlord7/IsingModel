import simcx
from game_of_ice import GameOfIce
from perturbations import perturb_square
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
    # Set the size of the neighborhood
    NEIGHBOURHOOD_SIZE = max(GRID_WIDTH_CELLS, GRID_HEIGHT_CELLS)
    # Set the probability of generating a spin up
    PROB_GENERATION = 0.5
    # Set the size of the cells in the visualization
    CELL_SIZE = 3
    # Set the size of the stats plot
    GRID_STATS_PLOT_WIDTH = GRID_WIDTH_CELLS * CELL_SIZE
    GRID_STATS_PLOT_HEIGHT = 600

    # Create a GameOfIce instance with the specified parameters
    goi = GameOfIce(width=GRID_WIDTH_CELLS,
                    height=GRID_HEIGHT_CELLS,
                    neighbourhood_size=NEIGHBOURHOOD_SIZE,
                    perturbation_function=perturb_square,
                    coupling_constant=2,
                    initial_temperature=300,
                    dist_func='gaussian',
                    method="global",
                    fill=0)

    # Generate a random spin configuration
    goi.random(PROB_GENERATION)

    # Create a Grid2D instance to visualize the grid
    vis = Grid2D(goi, CELL_SIZE)
    # Create a StatsPlot instance to plot the statistics
    vis2 = StatsPlot(goi,
                     width=GRID_STATS_PLOT_WIDTH,
                     height=GRID_STATS_PLOT_HEIGHT)

    # Create a CustomDisplay instance to display the simulation
    display = CustomDisplay(goi,
                            vis,
                            'screenshot',
                            x_min=0,
                            x_max=CELL_SIZE * GRID_WIDTH_CELLS,
                            y_min=GRID_STATS_PLOT_HEIGHT,
                            y_max=GRID_STATS_PLOT_HEIGHT + CELL_SIZE * GRID_HEIGHT_CELLS,
                            cell_size=CELL_SIZE,
                            interval=0.1)
    # Add the GameOfIce instance, the Grid2D instance, and the StatsPlot instance to the display
    display.add_simulator(goi)
    display.add_visual(vis, 0, GRID_STATS_PLOT_HEIGHT)
    display.add_visual(vis2)
    # Run the simulation using the simcx library
    simcx.run()


if __name__ == '__main__':
    main()

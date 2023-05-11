import matplotlib
import matplotlib.pyplot as plt
from distribution_functions import *
from util.graphic_util import *

matplotlib.use('TkAgg')
n_points = 21
x, y, mesh = create_mesh2d(n_points, n_points)

dist_functions = [gaussian, exp_decay, log_normal, rayleigh]

for dist_function in dist_functions:
    z = dist_function(mesh)

    # Normalize the distribution so that the sum of probabilities is 1
    sm = np.sum(z)
    z /= sm

    # Plot the Gaussian distribution with grid lines
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x, y, z, cmap='viridis', edgecolors='black', linewidth=0.5)
    fig.colorbar(im,)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('2D %s distribution' % dist_function.__name__)

    ax.tick_params(axis='x', which='both', length=0)
    ax.tick_params(axis='y', which='both', length=0)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.show()

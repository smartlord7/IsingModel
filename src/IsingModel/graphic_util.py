import numpy as np


def create_mesh2d(n_points, min=0, max=1):
    x = np.linspace(min, max, n_points)
    y = np.linspace(min, max, n_points)
    xv, yv = np.meshgrid(x + (x[1] - x[0]) / 2, y + (y[1] - y[0]) / 2)
    mesh = (xv, yv)

    return x, y, mesh

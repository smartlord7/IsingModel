import numpy as np


def create_mesh2d(x_points, y_points, min=0, max=1):
    x = np.linspace(min, max, x_points)
    y = np.linspace(min, max, y_points)
    xv, yv = np.meshgrid(x + (x[1] - x[0]) / 2, y + (y[1] - y[0]) / 2)
    mesh = (xv, yv)

    return x, y, mesh

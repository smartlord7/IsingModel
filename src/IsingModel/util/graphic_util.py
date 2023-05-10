import numpy as np


def create_mesh2d(x_points, y_points, mn=0, mx=1):
    # Create arrays for the x and y positions of the grid lines
    x = np.linspace(mn, mx, x_points,  endpoint=False)
    y = np.linspace(mn, mx, y_points, endpoint=False)
    xv, yv = np.meshgrid(x, y)
    mesh = (xv, yv)

    return x, y, mesh
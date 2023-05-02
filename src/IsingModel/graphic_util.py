import numpy as np


def create_mesh2d(x_points, y_points, min=0, max=1):
    dx = (max - min) / x_points
    dy = (max - min) / y_points

    # Create arrays for the x and y positions of the grid lines
    x = np.linspace(min, max, x_points,  endpoint=False) # + dx / 2
    y = np.linspace(min, max, y_points, endpoint=False) # + dy / 2
    xv, yv = np.meshgrid(x, y)
    mesh = (xv, yv)

    return x, y, mesh
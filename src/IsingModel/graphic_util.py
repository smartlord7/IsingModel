import numpy as np


def create_mesh2d(n_points, min=0, max=1):
    dx = (max - min) / n_points
    dy = (max - min) / n_points

    # Create arrays for the x and y positions of the grid lines
    x = np.linspace(min, max, n_points, endpoint=False) + dx / 2
    y = np.linspace(min, max, n_points, endpoint=False) + dy / 2
    xv, yv = np.meshgrid(x, y)
    mesh = (xv, yv)

    return x, y, mesh

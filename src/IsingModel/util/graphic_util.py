import numpy as np


def create_mesh2d(x_points, y_points, mn=0, mx=1):
    """
    Creates a 2D meshgrid.

    Parameters:
    -----------
    x_points : int
        The number of points along the x-axis.
    y_points : int
        The number of points along the y-axis.
    mn : float, optional
        The minimum value of the x and y axes. Default is 0.
    mx : float, optional
        The maximum value of the x and y axes. Default is 1.

    Returns:
    --------
    x : numpy.ndarray
        A 1D numpy array representing the x positions of the grid lines.
    y : numpy.ndarray
        A 1D numpy array representing the y positions of the grid lines.
    mesh : tuple
        A tuple representing the meshgrid of the x and y positions.
    """

    # Create arrays for the x and y positions of the grid lines
    x = np.linspace(mn, mx, x_points, endpoint=False)
    y = np.linspace(mn, mx, y_points, endpoint=False)

    # Create a meshgrid of the x and y positions
    xv, yv = np.meshgrid(x, y)
    mesh = (xv, yv)

    return x, y, mesh
import numpy as np


def perturb_circle(matrix, center_row, center_col, radius, value):
    """
    Creates a circle of a given value around a certain cell in a 2D matrix.

    Parameters:
    -----------
    matrix : numpy.ndarray
        The 2D matrix.
    center_row : int
        The row index of the center cell.
    center_col : int
        The column index of the center cell.
    radius : int
        The radius of the circle.
    value : int
        The value to set for the cells in the circle.

    Returns:
    --------
    numpy.ndarray
        The updated 2D matrix.
    """
    # Create a mask of the same shape as the matrix
    mask = np.zeros_like(matrix, dtype=bool)

    # Set the center cell to True
    mask[center_row, center_col] = True

    # Create a distance matrix using the Euclidean distance formula
    rows, cols = np.indices(matrix.shape)
    distances = np.sqrt((rows - center_row) ** 2 + (cols - center_col) ** 2)

    # Set the mask to True for cells within the radius
    mask[distances <= radius] = True

    # Set the values of the cells in the mask to X
    matrix[mask] = value

    return matrix
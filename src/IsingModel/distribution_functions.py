import numpy as np


def gaussian(mesh: tuple, mean: tuple = (0.5, 0.5), std: tuple = (0.1, 0.1)):
    mesh_x = mesh[0]
    mesh_y = mesh[1]
    mean_x = mean[0]
    mean_y = mean[1]
    std_x = std[0]
    std_y = std[1]

    return np.exp(-((mesh_x - mean_x) ** 2 / (2 * std_x ** 2) + (mesh_y - mean_y) ** 2/(2 * std_y ** 2)))


def exp_decay(mesh: tuple, center: tuple = (0.5, 0.5), decay_rate=0.5):
    mesh_x = mesh[0]
    mesh_y = mesh[1]
    center_x = center[0]
    center_y = center[1]

    return np.exp(-decay_rate * np.sqrt((mesh_x - center_x) ** 2 + (mesh_y - center_y) ** 2))

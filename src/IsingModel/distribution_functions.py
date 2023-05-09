import numpy as np
from scipy.stats import rayleigh


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

def rayleigh(mesh: tuple, center: tuple = (0.5, 0.5), sigma=2.0):
    mesh_x = mesh[0]
    mesh_y = mesh[1]
    center_x = center[0]
    center_y = center[1]

    distances = np.sqrt((mesh_x - center_x) ** 2 + (mesh_y - center_y) ** 2)
    return (distances / sigma**2) * np.exp(-distances**2 / (2 * sigma**2))

def lognormal_distribution(mesh: tuple, center: tuple = (0.5, 0.5), sigma=1.0, mu=0.0):
    mesh_x = mesh[0]
    mesh_y = mesh[1]
    center_x = center[0]
    center_y = center[1]

    distances = np.sqrt((mesh_x - center_x) ** 2 + (mesh_y - center_y) ** 2)
    z = (np.log(distances) - mu) / sigma
    return np.exp(-0.5 * z**2) / (sigma * distances)

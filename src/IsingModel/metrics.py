import numpy as np


def magnetization(states: np.ndarray):
    return np.mean(states)


def energy(states: np.ndarray):
    nb_sum = np.roll(states, 1, axis=0) + np.roll(states, -1, axis=0) + np.roll(states, 1, axis=1) + np.roll(states, -1,
                                                                                                          axis=1)
    return np.sum(states * nb_sum)


def correlation(states: np.ndarray):
    return np.mean(states * np.roll(states, 1, axis=0))

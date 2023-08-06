"""Custom fitness functions.

Link: [Fitness Functions](https://antenna.atlanswer.com/optimization/implementation/fitness)
"""

import numpy as np
import pandas as pd


def num_point_under_target(s: pd.Series, target: float):
    return (s < target).sum()


def distance_to_widebeam(p: pd.Series):
    p = p[30:331]
    p = p.clip(lower=-40)
    return (p.max() - p).sum()


def beamwidth(p: pd.Series):
    idx_max = int(p.idxmax())
    thr = p.max() - 3
    l_idx = r_idx = idx_max
    for i in range(idx_max, 0, -1):
        if p[i] > thr:
            l_idx = i
        else:
            break
    for i in range(idx_max, len(p), 1):
        if p[i] > thr:
            r_idx = i
        else:
            break
    return r_idx - l_idx


def target_s_param_point_db(s: np.ndarray, point: int, target: float) -> float:
    """Return distance to the target at the specified point.

    :param np.ndarray s: scattering parameter array
    :param int point: the point to evaluate the S-parameter
    :param float target: target value

    :return float: distance

    :Examples:
    ```py
    >>> s = np.array([0, 1, 2, 3])
    >>> point = 1
    >>> target = -1
    >>> target_s_param_point_db(s, point, target)
    2
    ```
    """
    return max(s[point] - target, 0)


# def fit_matching_point(s_11: np.ndarray, point: int, target: int):
#     return max(s_11[point] - target, 0)


# def fit_matching(s_11: np.ndarray):
#     (min_x, min_y) = get_s11_min(s_11)
#     return max(min_y + 30, 0)


# def fit_frequency(s_11: np.ndarray):
#     (min_x, min_y) = get_s11_min(s_11)
#     min_x_freq = idx2freq(int(min_x))
#     logger.debug(f"Iter: s_11 min -> {min_x_freq} GHz, {min_y} dB")
#     return abs(min_x_freq - 24.1)


# def fit_bandwidth(s_11: np.ndarray):
#     bandwidth = get_10db_impedance_bandwidth(s_11)
#     logger.debug(f"Iter: bandwidth -> {bandwidth} GHz")
#     return max(float(2.5 - bandwidth), 0)

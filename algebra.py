import numpy as np
from numpy.typing import NDArray


def calc_angles(arr: NDArray[int]) -> NDArray[float]:
    """
    assuming vectors have length
    """
    number_of_angles = max(0, arr.shape[0] - 2)
    angles = np.zeros(number_of_angles, dtype=np.float32)
    for i in range(number_of_angles):
        v0 = arr[i + 1] - arr[i]
        v1 = arr[i + 2] - arr[i + 1]
        dot_product = np.dot(v0, v1)
        magnitude_product = np.linalg.norm(v0) * np.linalg.norm(v1)
        quotient_product = np.clip(dot_product / magnitude_product, -1, 1)
        angles[i] = np.arccos(quotient_product)
    return angles


def calc_distance(a: NDArray[int], b: NDArray[int]) -> float:
    return np.linalg.norm(a - b)

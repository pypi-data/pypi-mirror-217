import numpy as np
np.seterr(divide='ignore', invalid='ignore')


def sqdiff(u: np.ndarray, v: np.ndarray, isNorm: bool = False) -> float:
    vector_u = np.squeeze(u).flatten().astype(np.float32)
    vector_v = np.squeeze(v).flatten().astype(np.float32)
    square_difference = np.linalg.norm((vector_u - vector_v), ord=2)**2
    if isNorm:
        square_difference /= np.linalg.norm(vector_u, ord=2) * np.linalg.norm(vector_v, ord=2)
    return square_difference

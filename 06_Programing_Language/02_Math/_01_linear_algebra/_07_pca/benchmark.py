"""
7. PCA(주성분 분석, Principal Component Analysis) - 순수 Python vs sklearn 속도 비교

비교 대상:
    순수 Python: fit_transform() — 공분산 행렬 계산 + numpy.linalg.eigh 고유값 분해
    sklearn    : sklearn.decomposition.PCA — 내부적으로 numpy.linalg.svd 사용

number_of_components = 2로 고정 (2차원으로 축소)
"""

import time
import random
import numpy as np
from sklearn.decomposition import PCA as SklearnPCA

from _01_linear_algebra._07_pca.pure import fit_transform

REPEAT = 5
NUMBER_OF_COMPONENTS = 2


def measure(fn, *args) -> float:
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def make_data(number_of_samples: int, number_of_features: int, seed: int = 42) -> tuple:
    rng = random.Random(seed)
    X_list = [
        [rng.gauss(0, 1) for _ in range(number_of_features)]
        for _ in range(number_of_samples)
    ]
    X_np = np.array(X_list)
    return X_list, X_np


def benchmark(number_of_samples: int, number_of_features: int):
    X_list, X_np = make_data(number_of_samples, number_of_features)
    sklearn_pca = SklearnPCA(n_components=NUMBER_OF_COMPONENTS)

    pure  = measure(fit_transform, X_list, NUMBER_OF_COMPONENTS)
    skl   = measure(sklearn_pca.fit_transform, X_np)
    speedup = pure / skl

    print(f"n={number_of_samples:>5}, d={number_of_features:>4} | "
          f"순수 Python: {pure:>10.3f} ms | "
          f"sklearn: {skl:>8.3f} ms | "
          f"speedup: {speedup:>7.1f}x")


if __name__ == "__main__":
    print("PCA 속도 비교 (number_of_components=2, 반복 횟수={})\n".format(REPEAT))
    print(f"{'':30} {'순수 Python (ms)':>18} {'sklearn (ms)':>12} {'speedup':>10}")
    print("-" * 75)
    for number_of_samples, number_of_features in [
        (100,  10),
        (100,  50),
        (500,  50),
        (500, 100),
        (1000, 100),
        (1000, 200),
    ]:
        benchmark(number_of_samples, number_of_features)
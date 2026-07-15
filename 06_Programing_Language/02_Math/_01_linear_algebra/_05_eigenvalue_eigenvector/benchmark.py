"""
5. 고유값(eigenvalue)·고유벡터(eigenvector) - 순수 Python vs NumPy 속도 비교

비교 대상:
    순수 Python: power_iteration()  — 거듭제곱법(power iteration), O(k·n²)
    NumPy:       numpy.linalg.eig() — LAPACK의 dgeev 루틴, QR 알고리즘 기반 O(n³)

주의:
    두 알고리즘은 목적이 다름.
    - power_iteration: 지배 고유값(dominant eigenvalue) 1개만 근사
    - numpy.linalg.eig: 모든 고유값·고유벡터 계산

    따라서 speedup 수치는 "알고리즘 우열"이 아닌
    "단일 고유값 근사 vs 전체 고유값 계산"의 비용 차이를 반영함.
"""

import time
import random
import numpy as np
from pure import power_iteration

REPEAT = 5


def measure(fn, *args) -> float:
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def make_symmetric_matrix(n: int, seed: int = 42) -> tuple:
    """n×n 대칭 행렬(symmetric matrix) 생성

    대칭 행렬을 사용하는 이유:
        실수 고유값(real eigenvalue)이 보장되어 비교 기준이 명확해짐.
        (비대칭 행렬은 복소수 고유값이 등장할 수 있음)
    """
    rng = random.Random(seed)
    M = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    # A = M + Mᵀ로 대칭화, 대각 우세 보장
    A_list = [
        [M[i][j] + M[j][i] + (n * 2 if i == j else 0)
         for j in range(n)]
        for i in range(n)
    ]
    A_np = np.array(A_list, dtype=float)
    return A_list, A_np


def benchmark(n: int):
    A_list, A_np = make_symmetric_matrix(n)

    pure = measure(power_iteration, A_list)
    npy  = measure(np.linalg.eig, A_np)
    speedup = pure / npy

    print(f"n={n:>5} | 순수 Python(power iteration): {pure:>10.3f} ms "
          f"| NumPy(eig, 전체): {npy:>8.3f} ms | speedup: {speedup:>7.1f}x")


if __name__ == "__main__":
    print("고유값 계산 속도 비교 (n×n 대칭 행렬, 반복 횟수 = {})\n".format(REPEAT))
    print("※ 순수 Python은 지배 고유값 1개, NumPy는 전체 고유값 계산\n")
    for n in [10, 50, 100, 200]:
        benchmark(n)
"""
3. 선형 시스템(linear system) - 순수 Python vs NumPy 속도 비교

비교 대상:
    순수 Python: solve()  (가우스 소거법, O(n³))
    NumPy:       numpy.linalg.solve()  (LAPACK의 _gesv 루틴 — LU 분해 기반)

주의:
    numpy.linalg.solve는 내부적으로 LAPACK(Linear Algebra PACKage)의
    dgesv (Double precision GEneral SolVer) 루틴을 호출함.
    dgesv는 LU 분해(LU decomposition)와 부분 피벗팅(partial pivoting)을
    결합한 방식으로 O(n³) 알고리즘을 캐시 친화적 블록 연산으로 처리함.
    알고리즘 복잡도는 동일하지만 상수 인수(constant factor)에서 차이가 남.
"""

import time
import random
import numpy as np
from _01_linear_algebra._03_linear_system_gaussian_elimination.pure import solve

REPEAT = 3


def measure(fn, *args) -> float:
    """fn(*args)를 REPEAT회 실행한 평균 시간(ms) 반환"""
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def make_system(n: int) -> tuple:
    """n×n 비특이(non-singular) 선형 시스템 생성

    대각 우세(diagonally dominant) 행렬을 사용해 singular(특이) 케이스를 회피함.
    대각 우세 조건: |A_{ii}| > Σ_{j≠i} |A_{ij}|
    """
    A_list = []
    for i in range(n):
        row = [random.uniform(-1, 1) for _ in range(n)]
        row[i] = sum(abs(v) for v in row) + 1.0   # 대각 우세 보장
        A_list.append(row)
    b_list = [random.uniform(-10, 10) for _ in range(n)]

    A_np = np.array(A_list)
    b_np = np.array(b_list)
    return A_list, b_list, A_np, b_np


def benchmark(n: int):
    A_list, b_list, A_np, b_np = make_system(n)

    pure = measure(solve, A_list, b_list)
    npy  = measure(np.linalg.solve, A_np, b_np)
    speedup = pure / npy

    print(f"n={n:>5} | 순수 Python: {pure:>10.3f} ms "
          f"| NumPy: {npy:>8.3f} ms | speedup: {speedup:>8.1f}x")


if __name__ == "__main__":
    print("선형 시스템 Ax=b 풀기 속도 비교 (n×n, 반복 횟수 = {})\n".format(REPEAT))
    for n in [5, 10, 50, 100, 200, 500]:
        benchmark(n)
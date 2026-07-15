"""
1. 편미분(partial derivative)과 gradient(기울기 벡터) - 순수 Python vs NumPy 속도 비교

NumPy 구현 방식:
    numpy.gradient()가 아닌 동일한 중앙 차분 공식을 NumPy 벡터 연산으로 구현함.
    순수 Python은 변수 수(n)만큼 반복문을 실행하는 반면,
    NumPy는 모든 변수에 대한 편미분을 벡터 연산으로 한 번에 처리함.

비교 대상:
    f(x) = Σ xᵢ² (변수 수 n개의 이차 함수)
    gradient의 해석적 값: ∇f(x) = 2x
"""

import time
import numpy as np
from pure import gradient

REPEAT = 10


def measure(fn, *args) -> float:
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def gradient_numpy(function_numpy, point_np: np.ndarray, step_size: float = 1e-5) -> np.ndarray:
    """NumPy 벡터 연산 기반 gradient 계산

    각 변수에 대해 step_size만큼 이동한 point를 한 번에 구성해
    중앙 차분을 벡터 연산으로 처리함.
    """
    n = len(point_np)
    gradient_vector = np.zeros(n)

    for i in range(n):
        point_forward  = point_np.copy()
        point_backward = point_np.copy()
        point_forward[i]  += step_size
        point_backward[i] -= step_size
        gradient_vector[i] = (function_numpy(point_forward) - function_numpy(point_backward)) / (2 * step_size)

    return gradient_vector


def benchmark(n: int):
    point_list = [float(i) for i in range(1, n + 1)]
    point_np   = np.array(point_list)

    # f(x) = Σ xᵢ²
    f_pure  = lambda point: sum(x ** 2 for x in point)
    f_numpy = lambda point: np.sum(point ** 2)

    pure = measure(gradient, f_pure, point_list)
    npy  = measure(gradient_numpy, f_numpy, point_np)
    speedup = pure / npy

    print(f"n={n:>6} | 순수 Python: {pure:>10.3f} ms "
          f"| NumPy: {npy:>8.3f} ms | speedup: {speedup:>7.1f}x")


if __name__ == "__main__":
    print("gradient 계산 속도 비교 (n = 변수 수, 반복 횟수 = {})\n".format(REPEAT))
    for n in [10, 50, 100, 500, 1000]:
        benchmark(n)
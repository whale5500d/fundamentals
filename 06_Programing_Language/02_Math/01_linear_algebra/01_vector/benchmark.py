"""
1. 벡터(vector)와 연산 - 순수 Python vs NumPy 속도 비교

목적: NumPy의 벡터화 연산(vectorization)이 제공하는 최적화 확인
대상: vector_add, scalar_multiply, dot_product, norm (4개 연산 전부)
"""

import time
import numpy as npw
from pure import vector_add, scalar_multiply, dot_product, norm

REPEAT = 10


def measure(fn, *args) -> float:
    """fn(*args)를 REPEAT회 실행한 평균 시간(ms) 반환"""
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def benchmark(n: int):
    a_list = list(range(n))
    b_list = list(range(n, 2 * n))
    c = 3.0

    a_np = np.array(a_list, dtype=float)
    b_np = np.array(b_list, dtype=float)

    results = {
        "vector_add":        (measure(vector_add, a_list, b_list),
                              measure(lambda a, b: a + b, a_np, b_np)),
        "scalar_multiply":   (measure(scalar_multiply, c, a_list),
                              measure(lambda c, a: c * a, c, a_np)),
        "dot_product":       (measure(dot_product, a_list, b_list),
                              measure(np.dot, a_np, b_np)),
        "norm":              (measure(norm, a_list),
                              measure(np.linalg.norm, a_np)),
    }

    print(f"\n--- n = {n:,} ---")
    print(f"{'연산':<20} {'순수 Python (ms)':>18} {'NumPy (ms)':>14} {'speedup':>10}")
    print("-" * 66)
    for op, (pure, npy) in results.items():
        speedup = pure / npy
        print(f"{op:<20} {pure:>18.4f} {npy:>14.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    print("벡터 연산 속도 비교 (n = 벡터 차원 수, 반복 횟수 = {})".format(REPEAT))
    for n in [10, 100, 1_000, 10_000, 100_000, 1_000_000]:
        benchmark(n)
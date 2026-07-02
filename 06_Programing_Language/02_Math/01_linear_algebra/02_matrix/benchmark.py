"""
2. 행렬(matrix)과 기본 연산 - 순수 Python vs NumPy 속도 비교

목적: NumPy의 벡터화 연산(vectorization)이 제공하는 최적화 확인
대상: matrix_add, transpose, matmul (3개 연산 전부)

주의:
    행렬은 n×n 정방 행렬(square matrix)로 고정.
    matmul의 시간 복잡도는 O(n³)이므로 n이 커질수록 순수 Python 비용이
    다른 연산(O(n²))에 비해 급격히 증가함.
    따라서 matmul은 더 작은 n 범위에서 비교함.
"""

import time
import numpy as np
from pure import matrix_add, transpose, matmul

REPEAT = 5


def measure(fn, *args) -> float:
    """fn(*args)를 REPEAT회 실행한 평균 시간(ms) 반환"""
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def make_matrix(n: int) -> tuple:
    """n×n list[list[float]]과 np.ndarray 동시 생성"""
    import random
    flat = [random.random() for _ in range(n * n)]
    M_list = [flat[i * n:(i + 1) * n] for i in range(n)]
    M_np = np.array(M_list)
    return M_list, M_np


def benchmark_on2(n: int):
    """matrix_add, transpose: O(n²) 연산"""
    A_list, A_np = make_matrix(n)
    B_list, B_np = make_matrix(n)

    results = {
        "matrix_add": (
            measure(matrix_add, A_list, B_list),
            measure(np.add, A_np, B_np),
        ),
        "transpose": (
            measure(transpose, A_list),
            measure(np.transpose, A_np),
        ),
    }

    print(f"\n--- n×n = {n}×{n} (O(n²) 연산) ---")
    print(f"{'연산':<15} {'순수 Python (ms)':>18} {'NumPy (ms)':>14} {'speedup':>10}")
    print("-" * 61)
    for op, (pure, npy) in results.items():
        speedup = pure / npy if npy > 0 else float("inf")
        print(f"{op:<15} {pure:>18.4f} {npy:>14.4f} {speedup:>9.1f}x")


def benchmark_matmul(n: int):
    """matmul: O(n³) 연산 — 별도로 비교"""
    A_list, A_np = make_matrix(n)
    C_list, C_np = make_matrix(n)

    pure = measure(matmul, A_list, C_list)
    npy  = measure(np.matmul, A_np, C_np)
    speedup = pure / npy if npy > 0 else float("inf")

    print(f"{'matmul':<15} {pure:>18.4f} {npy:>14.4f} {speedup:>9.1f}x", end="")
    print(f"   ← n={n}")


if __name__ == "__main__":
    print("=" * 70)
    print("행렬 연산 속도 비교 (n×n 정방 행렬, 반복 횟수 = {})".format(REPEAT))
    print("=" * 70)

    # O(n²) 연산: matrix_add, transpose
    for n in [10, 100, 500, 1_000]:
        benchmark_on2(n)

    # O(n³) 연산: matmul (n이 작은 범위에서만 비교)
    print(f"\n--- matmul (O(n³) 연산) ---")
    print(f"{'연산':<15} {'순수 Python (ms)':>18} {'NumPy (ms)':>14} {'speedup':>10}   크기")
    print("-" * 70)
    for n in [10, 50, 100, 200]:
        benchmark_matmul(n)
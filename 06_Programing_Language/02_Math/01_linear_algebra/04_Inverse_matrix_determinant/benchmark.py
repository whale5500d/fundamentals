"""
4. 역행렬(inverse matrix)과 행렬식(determinant) - 순수 Python vs NumPy 속도 비교

NumPy 내부:
    numpy.linalg.inv  → LAPACK의 dgetrf (LU 분해) + dgetri (역행렬 추출) 루틴
    numpy.linalg.det  → LAPACK의 dgetrf (LU 분해) 후 대각 원소 곱

두 연산 모두 LU 분해(LU decomposition) 기반이며 시간 복잡도는 O(n³)으로 동일함.
차이는 상수 인수(constant factor): LAPACK은 캐시(cache) 친화적 블록 연산과
SIMD (Single Instruction Multiple Data) 명령어로 처리함.
"""

import time
import random
import numpy as np
from pure import inverse, determinant

REPEAT = 3


def measure(fn, *args) -> float:
    start = time.perf_counter()
    for _ in range(REPEAT):
        fn(*args)
    return (time.perf_counter() - start) / REPEAT * 1000


def make_matrix(n: int) -> tuple:
    """n×n 비특이(non-singular) 정방 행렬 생성 (대각 우세 조건 적용)"""
    M_list = []
    for i in range(n):
        row = [random.uniform(-1, 1) for _ in range(n)]
        row[i] = sum(abs(v) for v in row) + 1.0
        M_list.append(row)
    M_np = np.array(M_list)
    return M_list, M_np


def benchmark(n: int):
    A_list, A_np = make_matrix(n)

    results = {
        "inverse":     (measure(inverse, A_list),
                        measure(np.linalg.inv, A_np)),
        "determinant": (measure(determinant, A_list),
                        measure(np.linalg.det, A_np)),
    }

    print(f"\n--- n×n = {n}×{n} ---")
    print(f"{'연산':<15} {'순수 Python (ms)':>18} {'NumPy (ms)':>14} {'speedup':>10}")
    print("-" * 61)
    for op, (pure, npy) in results.items():
        speedup = pure / npy if npy > 0 else float("inf")
        print(f"{op:<15} {pure:>18.4f} {npy:>14.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    print("역행렬·행렬식 속도 비교 (n×n 정방 행렬, 반복 횟수 = {})".format(REPEAT))
    for n in [5, 10, 50, 100, 200, 500]:
        benchmark(n)
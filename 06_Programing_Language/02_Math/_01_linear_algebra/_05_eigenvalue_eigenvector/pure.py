"""
5. 고유값(eigenvalue)·고유벡터(eigenvector) - 순수 Python 구현

알고리즘: 거듭제곱법(power iteration)
    - 절댓값이 가장 큰 고유값(지배 고유값, dominant eigenvalue)과
      대응하는 고유벡터를 반복적으로 근사함
    - 수렴 조건: 연속된 두 고유값 추정치의 차이가 tol 미만

시간 복잡도(time complexity): O(k·n²)  (k: 수렴까지 반복 횟수)
"""

import math
import random


def _matvec(A: list, v: list) -> list:
    """행렬-벡터곱(matrix-vector multiplication): w = A·v

    Args:
        A: 행렬, shape = n×n
        v: 벡터, shape = n

    Returns:
        w = A·v, shape = n
    """
    n = len(A)

    # basic
    # 단순 2중 반복문이 아니라,
    # 곱한 다음 덧셈까지 실행한 결과를 append 해야함.
    # 예시:nxn * nx1 = nx1이 되기 때문
    # result = []
    # for i in range(n):
    #     total = 0
    #     for j in range(n):
    #         total += A[i][j] * v[j]
    #     result.append(total)
    # return result

    # comprehension
    return [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]


def _norm(v: list) -> float:
    """L2 norm(노름): ‖v‖ = sqrt(Σ vᵢ²)"""
    # 제곱을 사용하기 때문에 L2라 부름
    # 절대값을 사용하면 L1이라 부름

    # basic 1
    # sum = 0
    # for x in v:
    #     sum += x * x
    # return math.sqrt(sum)

    # basic 2
    return math.sqrt(sum(x * x for x in v))


def _normalize(v: list) -> list:
    """벡터 정규화(normalization): v / ‖v‖"""
    n = _norm(v)

    # basic 1
    # result = []
    # for x in v:
    #     result.append(x / n)
    # return result

    # basic 2
    return [x / n for x in v]


def _rayleigh_quotient(A: list, v: list) -> float:
    """레일리 지수(Rayleigh quotient): λ ≈ vᵀAv / vᵀv

    정규화된 벡터 v(‖v‖=1)에 대해 vᵀAv = vᵀ(Av) = dot(v, Av)
    지배 고유값의 추정치로 사용됨.
    """
    Av = _matvec(A, v)

    # basic 1
    # result = 0
    # for i in range(len(Av)): # Av가 더 안전, 방어적 프로그래밍
    #     result += v[i] * Av[i]
    # return result

    # basic 2
    return sum(v[i] * Av[i] for i in range(len(v)))



def power_iteration(
    A: list,
    tolerance: float = 1e-10,
    maximum_iterations: int = 1000,
    seed: int = 42,
) -> tuple:
    """거듭제곱법(power iteration)으로 지배 고유값·고유벡터 근사

    Args:
        A                  : 정방 행렬(square matrix), shape = n×n
        tolerance          : 허용 오차, 수렴 판정 기준 — 연속된 고유값 추정치 차이가 tol 미만이면 수렴으로 판단
        maximum_iterations : 최대 반복 횟수
        seed               : 초기 벡터 난수 시드(random seed) — 재현성(reproducibility) 보장

    Returns:
        (eigenvalue, eigenvector) 튜플
            eigenvalue : 지배 고유값(dominant eigenvalue) λ (float)
            eigenvector: 대응하는 고유벡터 v, shape = n, ‖v‖ = 1
    """
    n = len(A)
    assert len(A[0]) == n, "A는 정방 행렬(square matrix)이어야 함"

    # 초기 벡터: 재현성을 위해 시드 고정
    rng = random.Random(seed)
    v = _normalize([rng.gauss(0, 1) for _ in range(n)])

    eigenvalue = 0.0

    for _ in range(maximum_iterations):
        w = _matvec(A, v)              # w = A·v
        v_new = _normalize(w)          # 정규화
        eigenvalue_new = _rayleigh_quotient(A, v_new)  # 고유값 추정

        # 수렴 판정: 고유값 추정치 변화량이 tolerance 미만이면 중단
        if abs(eigenvalue_new - eigenvalue) < tolerance:
            return eigenvalue_new, v_new

        v = v_new
        eigenvalue = eigenvalue_new

    # maximum_iterations 도달 시 현재 추정값 반환 (수렴 미보장)
    return eigenvalue, v
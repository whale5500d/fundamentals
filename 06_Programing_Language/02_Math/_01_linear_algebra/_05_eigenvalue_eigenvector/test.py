"""
5. 고유값(eigenvalue)·고유벡터(eigenvector) - 테스트 코드

검증 방식:
    거듭제곱법(power iteration)은 지배 고유값(dominant eigenvalue) 하나만 근사함.
    numpy.linalg.eig는 모든 고유값을 반환하므로, 그 중 절댓값이 가장 큰 것과 비교함.

고유벡터 부호(sign) 주의:
    Av = λv이면 A(-v) = λ(-v)도 성립함. 즉 고유벡터의 부호는 정의에 의해 임의적임.
    따라서 방향 일치 여부는 절댓값 내적(|dot(v, v_expected)|)으로 검증함.
"""

import math
import numpy as np
import pytest

from pure import power_iteration, _matvec, _norm, _rayleigh_quotient


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def dominant_eig_numpy(A: list) -> tuple:
    """NumPy로 지배 고유값·고유벡터 계산 (비교 기준값)"""
    eigenvalues, eigenvectors = np.linalg.eig(np.array(A, dtype=float))
    idx = np.argmax(np.abs(eigenvalues))
    return float(np.real(eigenvalues[idx])), np.real(eigenvectors[:, idx])

def abs_dot(v1: list, v2) -> float:
    """두 벡터의 절댓값 내적: |Σ v1ᵢ·v2ᵢ| — 방향 일치 여부 검증용"""
    return abs(sum(v1[i] * float(v2[i]) for i in range(len(v1))))


# ── 기본 동작 검증 ────────────────────────────────────────────────────────────

def test_eigenvalue_2x2():
    # 고유값이 명확한 2×2 대칭 행렬
    # 고유값: 5, 1 → 지배 고유값 = 5
    A = [[4, 1],
         [1, 2]]
    eigenvalue, eigenvector = power_iteration(A)
    expected_val, expected_vec = dominant_eig_numpy(A)

    assert math.isclose(eigenvalue, expected_val, abs_tol=1e-6)
    assert math.isclose(abs_dot(eigenvector, expected_vec), 1.0, abs_tol=1e-6)


def test_eigenvalue_3x3():
    A = [[2, 1, 0],
         [1, 3, 1],
         [0, 1, 2]]
    eigenvalue, eigenvector = power_iteration(A)
    expected_val, expected_vec = dominant_eig_numpy(A)

    assert math.isclose(eigenvalue, expected_val, abs_tol=1e-6)
    assert math.isclose(abs_dot(eigenvector, expected_vec), 1.0, abs_tol=1e-6)


def test_eigenvector_is_normalized():
    # 반환된 고유벡터의 norm이 1이어야 함
    A = [[3, 1],
         [1, 3]]
    _, eigenvector = power_iteration(A)
    assert math.isclose(_norm(eigenvector), 1.0, abs_tol=1e-10)


def test_eigenvector_satisfies_definition():
    # Av = λv 정의 검증: ‖Av - λv‖ ≈ 0
    A = [[4, 1],
         [2, 3]]
    eigenvalue, eigenvector = power_iteration(A)
    Av = _matvec(A, eigenvector)
    lv = [eigenvalue * eigenvector[i] for i in range(len(eigenvector))]
    residual = _norm([Av[i] - lv[i] for i in range(len(Av))])
    assert residual < 1e-6, f"잔차(residual) {residual}이 허용 범위 초과"


def test_rayleigh_quotient_equals_eigenvalue():
    # 수렴된 고유벡터에 대한 레일리 지수(Rayleigh quotient)가 고유값과 일치해야 함
    A = [[5, 2],
         [2, 1]]
    eigenvalue, eigenvector = power_iteration(A)
    rq = _rayleigh_quotient(A, eigenvector)
    assert math.isclose(rq, eigenvalue, abs_tol=1e-8)


def test_diagonal_matrix():
    # 대각 행렬(diagonal matrix): 대각 원소가 고유값, 표준 기저가 고유벡터
    # 지배 고유값 = 5
    A = [[5, 0, 0],
         [0, 3, 0],
         [0, 0, 1]]
    eigenvalue, _ = power_iteration(A)
    assert math.isclose(eigenvalue, 5.0, abs_tol=1e-6)


if __name__ == "__main__":
    test_eigenvalue_2x2()
    test_eigenvalue_3x3()
    test_eigenvector_is_normalized()
    test_eigenvector_satisfies_definition()
    test_rayleigh_quotient_equals_eigenvalue()
    test_diagonal_matrix()
    print("모든 테스트 통과")
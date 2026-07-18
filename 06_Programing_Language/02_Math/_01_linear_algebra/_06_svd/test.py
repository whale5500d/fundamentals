"""
6. SVD(특이값 분해, Singular Value Decomposition) - 테스트 코드

검증 항목:
    1. A = U·Σ·Vᵀ 재구성 정확도
    2. U, V 정규직교성(orthonormality)
    3. 특이값 내림차순 정렬
    4. 특이값과 AᵀA 고유값의 관계
    5. 저랭크 근사 오차와 Eckart-Young 이론값 일치
"""

import math
import numpy as np
import pytest

from pure import svd_decompose, low_rank_approximation, frobenius_norm


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def make_sigma(singular_values: np.ndarray, m: int, n: int) -> np.ndarray:
    """특이값 벡터로 m×n Σ 행렬 구성"""
    Sigma = np.zeros((m, n))
    for i in range(min(m, n)):
        Sigma[i, i] = singular_values[i]
    return Sigma


# ── 재구성 검증 ───────────────────────────────────────────────────────────────

def test_reconstruction_square():
    # 정방 행렬: A = U·Σ·Vᵀ 재구성 오차가 기계 엡실론 수준이어야 함
    A = np.array([[3.0, 1.0], [1.0, 3.0]])
    U, singular_values, Vt = svd_decompose(A)
    Sigma = make_sigma(singular_values, *A.shape)
    A_reconstructed = U @ Sigma @ Vt
    assert np.allclose(A, A_reconstructed, atol=1e-12)


def test_reconstruction_nonsquare():
    # 비정방 행렬(m > n): 재구성 검증
    A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    U, singular_values, Vt = svd_decompose(A)
    Sigma = make_sigma(singular_values, *A.shape)
    A_reconstructed = U @ Sigma @ Vt
    assert np.allclose(A, A_reconstructed, atol=1e-12)


# ── 정규직교성(orthonormality) 검증 ──────────────────────────────────────────

def test_U_is_orthonormal():
    # UᵀU = I 검증
    A = np.random.default_rng(0).random((4, 3))
    U, _, _ = svd_decompose(A)
    assert np.allclose(U.T @ U, np.eye(U.shape[0]), atol=1e-12)


def test_V_is_orthonormal():
    # VᵀV = I 검증
    A = np.random.default_rng(0).random((4, 3))
    _, _, Vt = svd_decompose(A)
    V = Vt.T
    assert np.allclose(V.T @ V, np.eye(V.shape[0]), atol=1e-12)


# ── 특이값 정렬 검증 ──────────────────────────────────────────────────────────

def test_singular_values_descending():
    # 특이값이 내림차순(σ₁ ≥ σ₂ ≥ ... ≥ 0)으로 정렬되어야 함
    A = np.random.default_rng(1).random((5, 4))
    _, singular_values, _ = svd_decompose(A)
    for i in range(len(singular_values) - 1):
        assert singular_values[i] >= singular_values[i + 1]


def test_singular_values_nonnegative():
    A = np.random.default_rng(2).random((3, 5))
    _, singular_values, _ = svd_decompose(A)
    assert all(sv >= 0 for sv in singular_values)


# ── 특이값과 AᵀA 고유값의 관계 검증 ─────────────────────────────────────────

def test_singular_values_relation_to_eigenvalues():
    # σᵢ² = λᵢ(AᵀA) 검증
    A = np.array([[3.0, 1.0, 1.0],
                  [1.0, 3.0, 1.0],
                  [1.0, 1.0, 3.0],
                  [1.0, 1.0, 1.0]])
    _, singular_values, _ = svd_decompose(A)
    AtA_eigenvalues = np.sort(np.linalg.eigvalsh(A.T @ A))[::-1]
    assert np.allclose(singular_values ** 2, AtA_eigenvalues, atol=1e-10)


# ── 저랭크 근사(low-rank approximation) 검증 ─────────────────────────────────

def test_low_rank_approximation_error_matches_theory():
    # Eckart-Young 정리: 근사 오차 = √(σₖ₊₁² + ... + σᵣ²)
    A = np.array([[3.0, 1.0, 1.0],
                  [1.0, 3.0, 1.0],
                  [1.0, 1.0, 3.0],
                  [1.0, 1.0, 1.0]])
    _, singular_values, _ = svd_decompose(A)

    for k in range(1, min(A.shape)):
        A_k = low_rank_approximation(A, k)
        actual_error = frobenius_norm(A - A_k)
        theoretical_error = float(np.sqrt(np.sum(singular_values[k:] ** 2)))
        assert math.isclose(actual_error, theoretical_error, abs_tol=1e-10)


def test_full_rank_approximation_is_exact():
    # rank = min(m,n)이면 오차가 0이어야 함
    A = np.random.default_rng(3).random((4, 3))
    A_full = low_rank_approximation(A, min(A.shape))
    assert np.allclose(A, A_full, atol=1e-12)


def test_rank1_approximation_is_outer_product():
    # rank=1 근사: A₁ = σ₁·u₁·v₁ᵀ
    A = np.array([[4.0, 0.0], [3.0, 0.0]])
    U, singular_values, Vt = svd_decompose(A)
    A_1_expected = singular_values[0] * np.outer(U[:, 0], Vt[0, :])
    A_1_actual = low_rank_approximation(A, 1)
    assert np.allclose(A_1_actual, A_1_expected, atol=1e-12)


if __name__ == "__main__":
    test_reconstruction_square()
    test_reconstruction_nonsquare()
    test_U_is_orthonormal()
    test_V_is_orthonormal()
    test_singular_values_descending()
    test_singular_values_nonnegative()
    test_singular_values_relation_to_eigenvalues()
    test_low_rank_approximation_error_matches_theory()
    test_full_rank_approximation_is_exact()
    test_rank1_approximation_is_outer_product()
    print("모든 테스트 통과")
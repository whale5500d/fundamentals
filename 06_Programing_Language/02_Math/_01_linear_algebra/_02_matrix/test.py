"""
2. 행렬(matrix)과 기본 연산 - 테스트 코드

검증 방식: 순수 Python 구현 결과 vs NumPy 결과 비교(assertion)
"""

import numpy as np
import pytest

from _01_linear_algebra._02_matrix.pure import shape, matrix_add, transpose, matmul


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def to_numpy(M: list) -> np.ndarray:
    return np.array(M, dtype=float)

def allclose(M: list, expected: np.ndarray) -> bool:
    return np.allclose(to_numpy(M), expected)


# ── shape ─────────────────────────────────────────────────────────────────────

def test_shape():
    A = [[1, 2, 3],
         [4, 5, 6]]          # 2×3 행렬
    assert shape(A) == (2, 3)


# ── matrix_add ────────────────────────────────────────────────────────────────

def test_matrix_add():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = to_numpy(A) + to_numpy(B)
    assert allclose(matrix_add(A, B), expected)


def test_matrix_add_shape_mismatch():
    # shape가 다른 행렬을 더하면 AssertionError 발생해야 함
    A = [[1, 2], [3, 4]]
    B = [[1, 2, 3], [4, 5, 6]]
    with pytest.raises(AssertionError):
        matrix_add(A, B)


# ── transpose ─────────────────────────────────────────────────────────────────

def test_transpose_square():
    # 정방 행렬(square matrix)
    A = [[1, 2], [3, 4]]
    expected = to_numpy(A).T
    assert allclose(transpose(A), expected)


def test_transpose_nonsquare():
    # 비정방 행렬: 2×3 → 3×2
    A = [[1, 2, 3],
         [4, 5, 6]]
    expected = to_numpy(A).T
    result = transpose(A)
    assert shape(result) == (3, 2)
    assert allclose(result, expected)


def test_transpose_double():
    # 전치를 두 번 적용하면 원래 행렬과 동일해야 함: (A^T)^T = A
    A = [[1, 2, 3], [4, 5, 6]]
    assert transpose(transpose(A)) == A


# ── matmul ────────────────────────────────────────────────────────────────────

def test_matmul_square():
    # 정방 행렬끼리 곱셈
    A = [[1, 2], [3, 4]]
    C = [[5, 6], [7, 8]]
    expected = to_numpy(A) @ to_numpy(C)
    assert allclose(matmul(A, C), expected)


def test_matmul_nonsquare():
    # 2×3 @ 3×4 → 2×4
    A = [[1, 2, 3],
         [4, 5, 6]]
    C = [[7,  8,  9,  10],
         [11, 12, 13, 14],
         [15, 16, 17, 18]]
    expected = to_numpy(A) @ to_numpy(C)
    result = matmul(A, C)
    assert shape(result) == (2, 4)
    assert allclose(result, expected)


def test_matmul_not_commutative():
    # 행렬곱은 교환법칙이 성립하지 않음: A·C ≠ C·A
    A = [[1, 2], [3, 4]]
    C = [[5, 6], [7, 8]]
    assert matmul(A, C) != matmul(C, A)


def test_matmul_shape_mismatch():
    # A의 열 수 != C의 행 수이면 AssertionError 발생해야 함
    A = [[1, 2, 3], [4, 5, 6]]   # 2×3
    C = [[1, 2], [3, 4]]          # 2×2
    with pytest.raises(AssertionError):
        matmul(A, C)


if __name__ == "__main__":
    test_shape()
    test_matrix_add()
    test_matrix_add_shape_mismatch()
    test_transpose_square()
    test_transpose_nonsquare()
    test_transpose_double()
    test_matmul_square()
    test_matmul_nonsquare()
    test_matmul_not_commutative()
    test_matmul_shape_mismatch()
    print("모든 테스트 통과")
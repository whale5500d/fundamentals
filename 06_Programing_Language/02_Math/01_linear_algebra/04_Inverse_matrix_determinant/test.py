import math
import numpy as np
import pytest

from pure import inverse, determinant
from 03_linear_system_gaussian_elimination.pure import SingularMatrixError


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────
def allclose(M: list, expected: np.ndarray, tol: float = 1e-9) -> bool:
    return np.allclose(np.array(M), expected, atol=tol)

# ── inverse ───────────────────────────────────────────────────────────────────
def test_inverse_2x2():
    A = [[4, 7],
        [2, 6]]
    result = inverse(A)
    expected = np.linalg.inv(A)
    assert allclose(result, expected)

def test_inverse_3x3():
    A = [[2, 1, -1],
         [-3, -1, 2],
         [-2 , 1, 2]]
    result = inverse(A)
    expected = np.linalg.inv(A)
    assert allclose(result, expected)

def test_inverse_idnetity_property():
    """A * A^{-1} = I 검증"""
    A = [[3, 1, 2],
         [1, 4, 1],
         [2, 1, 5]]
    A_inv = inverse(A)
    n = len(A)

    # A * A^{-1} 직접 계산
    # 기초 계산
    # product = []
    # for i in range(n):
    #     for j in range(n):
    #         for k in range(n):
    #             dot = sum(A[i][k] * A_inv[k][j])
    #             product.append(dot)
    # 컴프리헨션
    product = [
        [sum(A[i][k] * A_inv[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]

    I = np.eye(n)
    assert allclose(product, I)

    
def test_inverse_double():
    A = [[2, 1],
         [5, 3]]
    A_inv = inverse(A)
    A_inv_inv = inverse(A_inv)
    assert allclose(A_inv_inv, np.array(A, dtype=float))
    
def test_inverse_singular():
    # singular(특이 행렬) → SingularMatrixError 발생해야 함
    A = [[1, 2],
         [2, 4]]   # 2행 = 2 × 1행 → 선형 종속(linearly dependent)
    with pytest.raises(SingularMatrixError):
        inverse(A)

# ── determinant ───────────────────────────────────────────────────────────────
def test_determinant_2x2():
    A = [[3, 8],
         [4, 6]]
    result = determinant(A)
    expected = np.linalg.det(A)
    assert math.isclose(result, expected, abs_tol=1e-9)

def test_determinant_3x3():
    A = [[6, 1, 1],
         [4, -2, 5],
         [2, 8, 7]]
    result = determinant(A)
    expected = np.linalg.det(A)
    assert math.isclose(result, expected, abs_tol=1e-9)

def test_determinant_singular():
    # singular(특이 행렬)의 행렬식 = 0
    A = [[1, 2],
         [2, 4]]
    assert math.isclose(determinant(A), 0.0, abs_tol=1e-9)

def test_determinant_identity():
    # 단위 행렬(identity matrix)의 행렬식 = 1
    I = [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]
    assert math.isclose(determinant(I), 1.0, abs_tol=1e-9)

def test_determinant_row_swap_sign():
    # 행 교환(row swap) 1회 → 행렬식 부호(sign) 반전
    A = [[1, 2],
         [3, 4]]
    A_swapped = [[3, 4],
                 [1, 2]]
    assert math.isclose(determinant(A), -determinant(A_swapped), abs_tol=1e-9)

def test_determinant_relation_to_inverse():
    # det(A) ≠ 0 이면 역행렬 존재, det(A) = 0 이면 역행렬 없음
    A_inv = [[2, 1], [5, 3]]   # det = 1 ≠ 0
    A_sing = [[1, 2], [2, 4]]  # det = 0
 
    assert not math.isclose(determinant(A_inv), 0.0, abs_tol=1e-9)
    assert math.isclose(determinant(A_sing), 0.0, abs_tol=1e-9)

if __name__ == "__main__":
    test_inverse_2x2()
    test_inverse_3x3()
    test_inverse_idnetity_property()
    test_inverse_double()
    test_inverse_singular()
    test_determinant_2x2()
    test_determinant_3x3()
    test_determinant_singular()
    test_determinant_identity()
    test_determinant_row_swap_sign()
    test_determinant_relation_to_inverse()
    print("모든 테스트 통과")
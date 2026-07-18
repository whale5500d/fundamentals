"""
3. 선형 시스템(linear system) - 테스트 코드

검증 방식: 순수 Python 구현 결과 vs numpy.linalg.solve 결과 비교(assertion)
"""

import math
import numpy as np
import pytest

from _01_linear_algebra._03_linear_system_gaussian_elimination.pure import (
    solve,
    forward_elimination,
    back_substitution,
    SingularMatrixError,
    _augmented,
)


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def allclose(x: list, expected, tol: float = 1e-9) -> bool:
    return all(math.isclose(x[i], expected[i], abs_tol=tol) for i in range(len(x)))


# ── 기본 동작 검증 ────────────────────────────────────────────────────────────

def test_solve_2x2():
    # 2×2 기본 케이스
    # 2x + y = 5
    # x + 3y = 10  →  x=1, y=3
    A = [[2, 1],
         [1, 3]]
    b = [5, 10]
    x = solve(A, b)
    expected = np.linalg.solve(A, b)
    assert allclose(x, expected)


def test_solve_3x3():
    # 3×3 일반 케이스 (교재 예제)
    A = [[ 2,  1, -1],
         [-3, -1,  2],
         [-2,  1,  2]]
    b = [8, -11, -3]
    x = solve(A, b)
    expected = np.linalg.solve(A, b)
    assert allclose(x, expected)


def test_solve_verify_residual():
    # 해 x를 구한 뒤 Ax - b 의 잔차(residual)가 0에 가까운지 확인
    A = [[4, 3, 2],
         [1, 5, 1],
         [2, 1, 6]]
    b = [1, 2, 3]
    x = solve(A, b)
    for i in range(len(b)):
        row_result = sum(A[i][j] * x[j] for j in range(len(x)))
        assert math.isclose(row_result, b[i], abs_tol=1e-9), (
            f"잔차(residual) 불일치: 행 {i}, Ax={row_result}, b={b[i]}"
        )


# ── 부분 피벗팅(partial pivoting) 검증 ───────────────────────────────────────

def test_solve_requires_pivoting():
    # 피벗팅 없이는 첫 번째 피벗이 0이어서 실패하는 케이스
    # 피벗팅이 올바르게 적용되면 정상적으로 풀려야 함
    A = [[0, 1],
         [2, 3]]
    b = [1, 5]
    x = solve(A, b)
    expected = np.linalg.solve(A, b)
    assert allclose(x, expected)


def test_solve_large_diagonal_difference():
    # 대각 원소 간 크기 차이가 큰 경우 — 피벗팅 없이는 수치 불안정 발생
    A = [[1e-15, 1],
         [1,     1]]
    b = [1, 2]
    x = solve(A, b)
    expected = np.linalg.solve(A, b)
    assert allclose(x, expected, tol=1e-6)


# ── singular(특이 행렬) 예외 처리 검증 ───────────────────────────────────────

def test_solve_singular_matrix():
    # 행렬식(determinant)이 0인 singular(특이) 행렬 → SingularMatrixError 발생해야 함
    A = [[1, 2],
         [2, 4]]   # 2행 = 2 × 1행 → 선형 종속(linearly dependent)
    b = [1, 2]
    with pytest.raises(SingularMatrixError):
        solve(A, b)


# ── 내부 단계별 검증 ──────────────────────────────────────────────────────────

def test_forward_elimination_produces_upper_triangular():
    # 전방 소거(forward elimination) 후 하삼각 영역이 0인지 확인
    A = [[2, 1, -1],
         [-3, -1, 2],
         [-2, 1, 2]]
    b = [8, -11, -3]
    Ab = _augmented(A, b)
    U = forward_elimination(Ab)
    n = len(A)
    for i in range(n):
        for j in range(i):   # 하삼각(lower triangular) 영역
            assert math.isclose(U[i][j], 0.0, abs_tol=1e-12), (
                f"U[{i}][{j}] = {U[i][j]} (0이어야 함)"
            )


def test_back_substitution_after_manual_elimination():
    # [U|c]를 직접 구성한 뒤 후방 대입(back substitution)만 검증
    # 2x + y = 5, 3y = 9  →  y=3, x=1
    Ab = [[2, 1, 5],
          [0, 3, 9]]
    x = back_substitution(Ab)
    assert math.isclose(x[0], 1.0, abs_tol=1e-12)
    assert math.isclose(x[1], 3.0, abs_tol=1e-12)


if __name__ == "__main__":
    test_solve_2x2()
    test_solve_3x3()
    test_solve_verify_residual()
    test_solve_requires_pivoting()
    test_solve_large_diagonal_difference()
    test_solve_singular_matrix()
    test_forward_elimination_produces_upper_triangular()
    test_back_substitution_after_manual_elimination()
    print("모든 테스트 통과")
"""
1. 편미분(partial derivative)과 gradient(기울기 벡터) - 테스트 코드

검증 방식:
    해석적 미분값(analytic derivative)과 수치 미분값(numerical derivative) 비교.
    수치 미분의 오차는 O(h²)이므로 h=1e-5 기준 약 1e-10 수준의 오차를 허용함.

테스트 함수:
    f(x, y)     = x² + y²         → ∂f/∂x = 2x, ∂f/∂y = 2y
    f(x, y)     = x²y + 3y        → ∂f/∂x = 2xy, ∂f/∂y = x² + 3
    f(x, y, z)  = x²+ 2y² + 3z²  → ∇f = [2x, 4y, 6z]
"""

import math
import pytest

from pure import partial_derivative, gradient, directional_derivative


TOLERANCE = 1e-8   # 수치 미분 허용 오차


# ── 편미분(partial derivative) 검증 ──────────────────────────────────────────

def test_partial_derivative_quadratic_x():
    # f(x, y) = x² + y² → ∂f/∂x = 2x
    f = lambda point: point[0] ** 2 + point[1] ** 2
    point = [3.0, 4.0]
    result = partial_derivative(f, point, variable_index=0)
    analytic = 2 * point[0]   # 2x = 6.0
    assert math.isclose(result, analytic, abs_tol=TOLERANCE)


def test_partial_derivative_quadratic_y():
    # f(x, y) = x² + y² → ∂f/∂y = 2y
    f = lambda point: point[0] ** 2 + point[1] ** 2
    point = [3.0, 4.0]
    result = partial_derivative(f, point, variable_index=1)
    analytic = 2 * point[1]   # 2y = 8.0
    assert math.isclose(result, analytic, abs_tol=TOLERANCE)


def test_partial_derivative_mixed():
    # f(x, y) = x²y + 3y → ∂f/∂x = 2xy, ∂f/∂y = x² + 3
    f = lambda point: point[0] ** 2 * point[1] + 3 * point[1]
    point = [2.0, 5.0]

    result_x = partial_derivative(f, point, variable_index=0)
    result_y = partial_derivative(f, point, variable_index=1)

    analytic_x = 2 * point[0] * point[1]   # 2xy = 20.0
    analytic_y = point[0] ** 2 + 3          # x² + 3 = 7.0

    assert math.isclose(result_x, analytic_x, abs_tol=TOLERANCE)
    assert math.isclose(result_y, analytic_y, abs_tol=TOLERANCE)


def test_partial_derivative_does_not_modify_point():
    # partial_derivative 호출 후 원본 point가 변경되지 않아야 함
    f = lambda point: point[0] ** 2 + point[1] ** 2
    point = [3.0, 4.0]
    original_point = point[:]
    partial_derivative(f, point, variable_index=0)
    assert point == original_point


# ── gradient 검증 ─────────────────────────────────────────────────────────────

def test_gradient_quadratic():
    # f(x, y, z) = x² + 2y² + 3z² → ∇f = [2x, 4y, 6z]
    f = lambda point: point[0]**2 + 2*point[1]**2 + 3*point[2]**2
    point = [1.0, 2.0, 3.0]
    result = gradient(f, point)
    analytic = [2*point[0], 4*point[1], 6*point[2]]   # [2, 8, 18]
    for i in range(len(result)):
        assert math.isclose(result[i], analytic[i], abs_tol=TOLERANCE)


def test_gradient_length():
    # gradient의 길이가 입력 변수 수와 동일해야 함
    f = lambda point: sum(x**2 for x in point)
    point = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = gradient(f, point)
    assert len(result) == len(point)


def test_gradient_at_minimum_is_zero():
    # f(x, y) = x² + y²의 최솟값은 (0, 0) → ∇f(0, 0) = [0, 0]
    f = lambda point: point[0]**2 + point[1]**2
    point = [0.0, 0.0]
    result = gradient(f, point)
    for component in result:
        assert math.isclose(component, 0.0, abs_tol=TOLERANCE)


# ── 방향 미분(directional derivative) 검증 ───────────────────────────────────

def test_directional_derivative_along_axis():
    # f(x, y) = x² + y², x축 방향 단위 벡터 [1, 0]
    # D_u f(3, 4) = ∇f · [1, 0] = 2x = 6
    f = lambda point: point[0]**2 + point[1]**2
    point = [3.0, 4.0]
    result = directional_derivative(f, point, direction=[1.0, 0.0])
    assert math.isclose(result, 6.0, abs_tol=TOLERANCE)


def test_directional_derivative_gradient_direction_is_maximum():
    # gradient 방향으로의 방향 미분이 최대여야 함
    # D_u f = ∇f · u ≤ ‖∇f‖ (등호는 u = ∇f/‖∇f‖일 때)
    f = lambda point: point[0]**2 + 2*point[1]**2
    point = [1.0, 2.0]
    grad = gradient(f, point)
    magnitude = math.sqrt(sum(g**2 for g in grad))

    # gradient 방향으로의 방향 미분 = ‖∇f‖
    result = directional_derivative(f, point, direction=grad)
    assert math.isclose(result, magnitude, abs_tol=TOLERANCE)


def test_directional_derivative_zero_direction_raises():
    f = lambda point: point[0]**2 + point[1]**2
    with pytest.raises(AssertionError):
        directional_derivative(f, [1.0, 2.0], direction=[0.0, 0.0])


if __name__ == "__main__":
    test_partial_derivative_quadratic_x()
    test_partial_derivative_quadratic_y()
    test_partial_derivative_mixed()
    test_partial_derivative_does_not_modify_point()
    test_gradient_quadratic()
    test_gradient_length()
    test_gradient_at_minimum_is_zero()
    test_directional_derivative_along_axis()
    test_directional_derivative_gradient_direction_is_maximum()
    test_directional_derivative_zero_direction_raises()
    print("모든 테스트 통과")
"""
2. Chain rule(연쇄 법칙) - 테스트 코드

검증 방식:
    1. chain_rule_single/multiple: 해석적 미분값과 비교
    2. Value 클래스(자동 미분): 수치 미분(1단계 구현)과 비교

테스트 함수:
    h(x) = (x²)³     → dh/dx = 6x⁵  (chain rule: 3(x²)² · 2x)
    f(x) = ReLU(2x+1) → 구간별 미분 검증
    f(x,y) = x²y + y³ → ∂f/∂x = 2xy, ∂f/∂y = x² + 3y²
"""

import math
import pytest

from _02_multivariable_calculus._02_chain_rule.pure import chain_rule_single, chain_rule_multiple, Value
from _02_multivariable_calculus._01_partial_derivative_graident.pure import gradient


TOLERANCE = 1e-6


# ── chain_rule_single / chain_rule_multiple ───────────────────────────────────

def test_chain_rule_single_basic():
    # h(x) = (x²)³ → dh/dx = 3(x²)² · 2x = 6x⁵
    # x=2: outer=3*(2²)²=48, inner=2*2=4 → 48*4=192
    x = 2.0
    outer_derivative = 3 * (x ** 2) ** 2   # d/d(x²) of (x²)³
    inner_derivative = 2 * x               # d/dx of x²
    result = chain_rule_single(outer_derivative, inner_derivative)
    analytic = 6 * x ** 5                  # 6*32 = 192
    assert math.isclose(result, analytic, abs_tol=TOLERANCE)


def test_chain_rule_multiple_three_layers():
    # h(x) = sin(x²+1) 을 3개 층으로 분해
    # layer1: u = x,  du/dx = 1
    # layer2: v = x²+1, dv/du = 2x
    # layer3: w = sin(v), dw/dv = cos(v)
    # x=1: dw/dx = cos(2) * 2 * 1
    x = 1.0
    v = x ** 2 + 1
    derivatives = [1.0, 2 * x, math.cos(v)]
    result = chain_rule_multiple(derivatives)
    analytic = math.cos(x ** 2 + 1) * 2 * x
    assert math.isclose(result, analytic, abs_tol=TOLERANCE)


# ── Value: forward pass 검증 ──────────────────────────────────────────────────

def test_value_add():
    x = Value(3.0)
    y = Value(4.0)
    z = x + y
    assert math.isclose(z.data, 7.0)


def test_value_mul():
    x = Value(3.0)
    y = Value(4.0)
    z = x * y
    assert math.isclose(z.data, 12.0)


def test_value_pow():
    x = Value(3.0)
    z = x ** 2
    assert math.isclose(z.data, 9.0)


def test_value_relu_positive():
    x = Value(2.0)
    z = x.relu()
    assert math.isclose(z.data, 2.0)


def test_value_relu_negative():
    x = Value(-2.0)
    z = x.relu()
    assert math.isclose(z.data, 0.0)


# ── Value: backward pass (gradient) 검증 ─────────────────────────────────────

def test_backward_simple_quadratic():
    # f(x) = x² → df/dx = 2x
    # x=3: gradient = 6
    x = Value(3.0)
    loss = x ** 2
    loss.backward()
    assert math.isclose(x.gradient, 6.0, abs_tol=TOLERANCE)


def test_backward_matches_numerical_gradient():
    # f(x, y) = x²y + y³
    # 자동 미분 결과 vs 수치 미분 결과 비교
    x_val, y_val = 2.0, 3.0

    # 자동 미분
    x = Value(x_val)
    y = Value(y_val)
    loss = x ** 2 * y + y ** 3
    loss.backward()

    # 수치 미분 (1단계 구현 활용)
    f = lambda point: point[0] ** 2 * point[1] + point[1] ** 3
    numerical_grad = gradient(f, [x_val, y_val])

    assert math.isclose(x.gradient, numerical_grad[0], abs_tol=TOLERANCE)
    assert math.isclose(y.gradient, numerical_grad[1], abs_tol=TOLERANCE)


def test_backward_chain_rule_composition():
    # f(x) = (x + 1)² → df/dx = 2(x+1)
    # x=2: gradient = 6
    x = Value(2.0)
    loss = (x + 1) ** 2
    loss.backward()
    analytic = 2 * (x.data + 1)   # 2*3 = 6
    assert math.isclose(x.gradient, analytic, abs_tol=TOLERANCE)


def test_backward_relu_positive():
    # f(x) = ReLU(x), x > 0 → df/dx = 1
    x = Value(3.0)
    loss = x.relu()
    loss.backward()
    assert math.isclose(x.gradient, 1.0, abs_tol=TOLERANCE)


def test_backward_relu_negative():
    # f(x) = ReLU(x), x < 0 → df/dx = 0
    x = Value(-3.0)
    loss = x.relu()
    loss.backward()
    assert math.isclose(x.gradient, 0.0, abs_tol=TOLERANCE)


def test_backward_gradient_accumulates():
    # 동일 노드가 여러 연산에 사용되면 gradient가 누적(accumulate)되어야 함
    # f(x) = x² + x → df/dx = 2x + 1
    # x=3: gradient = 7
    x = Value(3.0)
    loss = x ** 2 + x
    loss.backward()
    assert math.isclose(x.gradient, 7.0, abs_tol=TOLERANCE)


def test_backward_two_layer_network():
    # 2층 신경망 순전파/역전파 시뮬레이션
    # layer1: a = ReLU(w1 * x)
    # layer2: loss = (a - target)²
    x      = Value(2.0)
    w1     = Value(3.0)
    target = Value(4.0)

    a    = (w1 * x).relu()
    loss = (a - target) ** 2
    loss.backward()

    # 수치 미분으로 검증
    f = lambda point: (max(0.0, point[0] * 2.0) - 4.0) ** 2
    numerical_grad = gradient(f, [w1.data])
    assert math.isclose(w1.gradient, numerical_grad[0], abs_tol=TOLERANCE)


if __name__ == "__main__":
    test_chain_rule_single_basic()
    test_chain_rule_multiple_three_layers()
    test_value_add()
    test_value_mul()
    test_value_pow()
    test_value_relu_positive()
    test_value_relu_negative()
    test_backward_simple_quadratic()
    test_backward_matches_numerical_gradient()
    test_backward_chain_rule_composition()
    test_backward_relu_positive()
    test_backward_relu_negative()
    test_backward_gradient_accumulates()
    test_backward_two_layer_network()
    print("모든 테스트 통과")
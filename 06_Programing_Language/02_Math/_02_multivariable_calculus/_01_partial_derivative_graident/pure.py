"""
1. 편미분(partial derivative)과 gradient(기울기 벡터) - 순수 Python 구현

수치 미분(numerical differentiation) 방식:
    중앙 차분(central difference): [f(x+h) - f(x-h)] / (2h)
    오차: O(h²) — 전방/후방 차분의 O(h)보다 정확

핵심 함수:
    partial_derivative() : 단일 변수에 대한 편미분
    gradient()           : 모든 변수에 대한 편미분 벡터
    directional_derivative(): 임의 방향으로의 변화율
"""

import math


def partial_derivative(
    function,
    point: list,
    variable_index: int,
    step_size: float = 1e-5,
) -> float:
    """중앙 차분(central difference)으로 편미분 계산

    ∂f/∂xᵢ ≈ [f(x₁,...,xᵢ+h,...,xₙ) - f(x₁,...,xᵢ-h,...,xₙ)] / (2h)

    Args:
        function      : 편미분할 다변수 함수 f(x: list) -> float
        point         : 편미분을 계산할 지점 x, shape = n
        variable_index: 편미분할 변수의 인덱스 i
        step_size     : 수치 미분 간격 h

    Returns:
        xᵢ에 대한 편미분값 ∂f/∂xᵢ (float)
    """
    point_forward  = point[:]
    point_backward = point[:]

    point_forward[variable_index]  += step_size
    point_backward[variable_index] -= step_size

    return (function(point_forward) - function(point_backward)) / (2 * step_size)


def gradient(
    function,
    point: list,
    step_size: float = 1e-5,
) -> list:
    """모든 변수에 대한 편미분을 모아 gradient 벡터 계산

    ∇f(x) = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ

    Args:
        function : 편미분할 다변수 함수 f(x: list) -> float
        point    : gradient를 계산할 지점 x, shape = n
        step_size: 수치 미분 간격 h

    Returns:
        gradient 벡터 ∇f(x), shape = n
    """
    return [
        partial_derivative(function, point, i, step_size)
        for i in range(len(point))
    ]


def directional_derivative(
    function,
    point: list,
    direction: list,
    step_size: float = 1e-5,
) -> float:
    """방향 미분(directional derivative): D_u f(x) = ∇f(x) · u

    임의의 방향 벡터 direction을 단위 벡터로 정규화한 뒤
    gradient와의 내적으로 계산함.

    Args:
        function : 다변수 함수 f(x: list) -> float
        point    : 방향 미분을 계산할 지점 x, shape = n
        direction: 방향 벡터 (단위 벡터가 아니어도 됨), shape = n
        step_size: 수치 미분 간격 h

    Returns:
        direction 방향으로의 변화율 (float)
    """
    # 방향 벡터 정규화(normalization)
    magnitude = math.sqrt(sum(d ** 2 for d in direction))
    assert magnitude > 0, "방향 벡터가 영벡터(zero vector)일 수 없음"
    unit_direction = [d / magnitude for d in direction]

    grad = gradient(function, point, step_size)

    return sum(grad[i] * unit_direction[i] for i in range(len(grad)))
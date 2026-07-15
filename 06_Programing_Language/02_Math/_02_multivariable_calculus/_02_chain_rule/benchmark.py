"""
2. Chain rule(연쇄 법칙) - Value 자동 미분 vs PyTorch autograd 비교

속도 비교보다 정확도 비교가 핵심인 이유:
    chain rule의 구현 목적은 "backpropagation의 수학적 원리 이해"이므로
    PyTorch autograd와 gradient 결과가 일치하는지 검증함.

    PyTorch는 C++ 레벨 계산 그래프와 CUDA 가속을 사용하므로
    순수 Python 구현과 속도 비교는 실용적 의미가 없음.

비교 함수:
    f(x, y) = x² * y + y³      → ∂f/∂x = 2xy,    ∂f/∂y = x² + 3y²
    f(x)    = ReLU(2x + 1)²    → 구간별 미분
    f(x, y) = (x - y)²        → ∂f/∂x = 2(x-y), ∂f/∂y = -2(x-y)
"""

import math

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from _02_multivariable_calculus._02_chain_rule.pure import Value


TOLERANCE = 1e-5


def compare(label: str, value_result: float, torch_result: float):
    match = math.isclose(value_result, torch_result, abs_tol=TOLERANCE)
    status = "✓" if match else "✗"
    print(f"  {status} {label:30s} | Value: {value_result:>10.6f} | PyTorch: {torch_result:>10.6f}")


def test_case_polynomial(x_val: float, y_val: float):
    print(f"\n[1] f(x,y) = x²y + y³, x={x_val}, y={y_val}")

    # Value 자동 미분
    x = Value(x_val)
    y = Value(y_val)
    loss = x ** 2 * y + y ** 3
    loss.backward()

    if TORCH_AVAILABLE:
        xt = torch.tensor(x_val, requires_grad=True, dtype=torch.float64)
        yt = torch.tensor(y_val, requires_grad=True, dtype=torch.float64)
        lt = xt ** 2 * yt + yt ** 3
        lt.backward()
        compare("∂f/∂x = 2xy", x.gradient, float(xt.grad))
        compare("∂f/∂y = x²+3y²", y.gradient, float(yt.grad))
    else:
        analytic_x = 2 * x_val * y_val
        analytic_y = x_val ** 2 + 3 * y_val ** 2
        compare("∂f/∂x = 2xy (해석적)", x.gradient, analytic_x)
        compare("∂f/∂y = x²+3y² (해석적)", y.gradient, analytic_y)


def test_case_relu(x_val: float):
    print(f"\n[2] f(x) = ReLU(2x+1)², x={x_val}")

    x = Value(x_val)
    loss = ((x * 2 + 1).relu()) ** 2
    loss.backward()

    if TORCH_AVAILABLE:
        xt = torch.tensor(x_val, requires_grad=True, dtype=torch.float64)
        lt = (torch.relu(xt * 2 + 1)) ** 2
        lt.backward()
        compare("∂f/∂x", x.gradient, float(xt.grad))
    else:
        inner = 2 * x_val + 1
        analytic = 2 * max(0.0, inner) * (2.0 if inner > 0 else 0.0)
        compare("∂f/∂x (해석적)", x.gradient, analytic)


def test_case_squared_diff(x_val: float, y_val: float):
    print(f"\n[3] f(x,y) = (x-y)², x={x_val}, y={y_val}")

    x = Value(x_val)
    y = Value(y_val)
    loss = (x - y) ** 2
    loss.backward()

    if TORCH_AVAILABLE:
        xt = torch.tensor(x_val, requires_grad=True, dtype=torch.float64)
        yt = torch.tensor(y_val, requires_grad=True, dtype=torch.float64)
        lt = (xt - yt) ** 2
        lt.backward()
        compare("∂f/∂x = 2(x-y)", x.gradient, float(xt.grad))
        compare("∂f/∂y = -2(x-y)", y.gradient, float(yt.grad))
    else:
        compare("∂f/∂x = 2(x-y) (해석적)", x.gradient, 2 * (x_val - y_val))
        compare("∂f/∂y = -2(x-y) (해석적)", y.gradient, -2 * (x_val - y_val))


if __name__ == "__main__":
    backend = "PyTorch autograd" if TORCH_AVAILABLE else "해석적 미분값"
    print(f"Value 자동 미분 vs {backend} 비교\n" + "=" * 60)

    test_case_polynomial(2.0, 3.0)
    test_case_relu(1.0)    # ReLU 활성화 구간
    test_case_relu(-1.0)   # ReLU 비활성화 구간
    test_case_squared_diff(3.0, 1.0)

    print("\n" + "=" * 60)
    print("✓ = 허용 오차(1e-5) 이내 일치")
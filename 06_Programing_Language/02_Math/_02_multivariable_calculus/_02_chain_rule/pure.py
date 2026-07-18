"""
2. Chain rule(연쇄 법칙) - 순수 Python 구현

구현 내용:
    1. 단변수 chain rule 적용 함수
    2. 계산 그래프(computational graph) 기반 자동 미분(automatic differentiation)
       - forward pass : 함수값 계산과 동시에 local gradient 저장
       - backward pass: chain rule로 gradient 역방향 전달

목적:
    PyTorch의 autograd가 내부적으로 하는 일을 최소한의 구조로 재현해,
    backpropagation의 수학적 원리를 코드 레벨에서 이해함.
"""


# ── 1. 단변수 chain rule ──────────────────────────────────────────────────────

def chain_rule_single(
    outer_derivative: float,
    inner_derivative: float,
) -> float:
    """단변수 chain rule: dh/dx = f'(g(x)) · g'(x)

    Args:
        outer_derivative: 외부 함수의 미분값 f'(g(x))
        inner_derivative: 내부 함수의 미분값 g'(x)

    Returns:
        합성 함수의 미분값 dh/dx
    """
    return outer_derivative * inner_derivative


def chain_rule_multiple(derivatives: list) -> float:
    """다층 합성 함수의 chain rule: d/dx[f_n ∘ ... ∘ f_1] = Π f_i'

    Args:
        derivatives: 각 층의 local gradient 목록 [f_1', f_2', ..., f_n']

    Returns:
        전체 합성 함수의 미분값
    """
    result = 1.0
    for derivative in derivatives:
        result *= derivative
    return result


# ── 2. 계산 그래프(computational graph) 기반 자동 미분 ────────────────────────

class Value:
    """계산 그래프의 노드(node) — 스칼라 값과 gradient를 함께 관리

    forward pass : 연산 수행 시 자동으로 계산 그래프 구성
    backward pass: backward() 호출 시 chain rule로 gradient 역방향 전달

    PyTorch의 Tensor(requires_grad=True)를 단순화한 구조임.
    """

    def __init__(self, data: float, _children: tuple = (), _operation: str = ""):
        self.data = data                    # 순전파(forward) 계산값
        self.gradient = 0.0                 # 역전파(backward) gradient, 초기값 0
        self._backward = lambda: None       # 역전파 함수 (연산별로 정의)
        self._previous = set(_children)     # 이 노드를 만든 이전 노드들
        self._operation = _operation        # 디버깅용 연산 이름

    def __add__(self, other):
        """덧셈: z = x + y → ∂z/∂x = 1, ∂z/∂y = 1"""
        other = other if isinstance(other, Value) else Value(other)
        result = Value(self.data + other.data, (self, other), "+")

        def _backward():
            # chain rule: 상위 gradient × local gradient(=1)
            self.gradient  += result.gradient * 1.0
            other.gradient += result.gradient * 1.0

        result._backward = _backward
        return result

    def __mul__(self, other):
        """곱셈: z = x * y → ∂z/∂x = y, ∂z/∂y = x"""
        other = other if isinstance(other, Value) else Value(other)
        result = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.gradient  += result.gradient * other.data
            other.gradient += result.gradient * self.data

        result._backward = _backward
        return result

    def __pow__(self, exponent: float):
        """거듭제곱: z = x^n → ∂z/∂x = n * x^(n-1)"""
        result = Value(self.data ** exponent, (self,), f"**{exponent}")

        def _backward():
            self.gradient += result.gradient * (exponent * self.data ** (exponent - 1))

        result._backward = _backward
        return result

    def relu(self):
        """ReLU 활성화 함수: z = max(0, x) → ∂z/∂x = 1 if x>0 else 0"""
        result = Value(max(0.0, self.data), (self,), "relu")

        def _backward():
            self.gradient += result.gradient * (1.0 if self.data > 0 else 0.0)

        result._backward = _backward
        return result

    def backward(self):
        """역전파(backward pass): 출력 노드에서 입력 노드 방향으로 gradient 전달

        위상 정렬(topological sort)로 연산 순서를 역방향으로 결정한 뒤
        각 노드의 _backward()를 순서대로 호출함.
        """
        topological_order = []
        visited = set()

        def build_topological_order(node):
            if node not in visited:
                visited.add(node)
                for child in node._previous:
                    build_topological_order(child)
                topological_order.append(node)

        build_topological_order(self)

        # 출력 노드의 gradient = 1 (∂Loss/∂Loss = 1)
        self.gradient = 1.0
        for node in reversed(topological_order):
            node._backward()

    # Python 연산자 오버로딩 보조
    def __radd__(self, other): return self + other
    def __rmul__(self, other): return self * other
    def __neg__(self):         return self * -1
    def __sub__(self, other):  return self + (-other)

    def __repr__(self):
        return f"Value(data={self.data:.4f}, gradient={self.gradient:.4f})"
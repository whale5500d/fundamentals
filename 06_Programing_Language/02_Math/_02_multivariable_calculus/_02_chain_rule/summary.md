# Chain Rule (연쇄 규칙)

## 1.1 배경 (필요성)

- 1단계에서 구현한 수치 미분(numerical differentiation)은 변수 수 n에 비례해 함수를 2n번 호출해야 함. 신경망의 파라미터가 수백만 개라면 gradient 계산에만 수백만 번의 함수 호출이 필요함. 이는 실용적으로 불가능함.
- 신경망은 여러 층(layer)이 합성된 함수 구조임.

  ```
  f(x) = f_L(f_{L-1}(...f_2(f_1(x))...))
  ```

- 각 층의 함수가 단순하다면, 전체 함수의 미분을 각 층의 미분의 곱으로 분해할 수 있음. 이것이 chain rule(연쇄 법칙)이며, 이를 활용하면 gradient를 단 한 번의 순전파(forward pass)와 역전파(backward pass)로 계산할 수 있음. 이것이 backpropagation(역전파)의 수학적 본질임.

## 1.2 수학적 정의

단변수 chain rule

- 함수 h(x) = f(g(x))에 대해:

  ```
  dh/dx = df/dg · dg/dx = f'(g(x)) · g'(x)
  ```

다변수 chain rule

- z = f(x₁, x₂, ..., xₙ)이고 각 xᵢ = gᵢ(t)일 때:

  ```
  dz/dt = Σᵢ (∂f/∂xᵢ) · (dxᵢ/dt)
  ```

다층 합성 함수의 chain rule (backpropagation의 수학적 구조)

- L층 신경망을 다음과 같이 표기함.

  ```
  a⁽⁰⁾ = x                          ← 입력
  a⁽ˡ⁾ = fₗ(a⁽ˡ⁻¹⁾),  l = 1,...,L    ← 각 층의 변환
  Loss = L(a⁽ᴸ⁾)                    ← 손실 함수
  ```

- chain rule을 적용하면 1번째 층의 gradient는:

  ```
  ∂Loss/∂a⁽ˡ⁾ = (∂Loss/∂a⁽ˡ⁺¹⁾) · (∂a⁽ˡ⁺¹⁾/∂a⁽ˡ⁾)
  ```

- 즉 출력층에서 입력층 방향으로 gradient를 역방향으로 전달하는 구조임. 각 층에서의 미분값(local gradient)을 미리 저장해두고 곱해나가는 것이 backpropagation의 핵심임.

자동 미분(automatic differentiation)과의 관계

- chain rule을 계산 그래프(computational graph) 위에서 체계적으로 적용하는 것이 자동 미분임. PyTorch의 autograd, JAX의 grad가 이를 구현함.
- 수치 미분(2n번 함수 호출)과 달리 단 1번의 역방향 패스로 모든 파라미터의 gradient를 동시에 계산함.

## 1.3 순수 Python으로 구현 및 테스트

- [[구현 코드 바로가기](./pure.py)]
- [[테스트 코드 바로가기](./test.py)]

## 1.4 NumPy와 비교 및 실행 결과 분석

- [분석 코드 바로가기](./benchmark.py)

- 실행 명령어

  ```bash
  (.venv) python3 benchmark.py
  ```

- 실행 결과

표 2. Value 자동 미분 vs PyTorch autograd 비교
| 함수 | 검증 항목 | Value gradient | PyTorch gradient | 일치 |
|---|---|---|---|---|
| x²y + y³ (x=2, y=3) | ∂f/∂x = 2xy | 12.0 | 12.0 | ✓ |
| x²y + y³ (x=2, y=3) | ∂f/∂y = x²+3y² | 31.0 | 31.0 | ✓ |
| ReLU(2x+1)² (x=1) | ∂f/∂x (활성화 구간) | 12.0 | 12.0 | ✓ |
| ReLU(2x+1)² (x=-1) | ∂f/∂x (비활성화 구간) | 0.0 | 0.0 | ✓ |
| (x-y)² (x=3, y=1) | ∂f/∂x = 2(x-y) | 4.0 | 4.0 | ✓ |
| (x-y)² (x=3, y=1) | ∂f/∂y = -2(x-y) | -4.0 | -4.0 | ✓ |

표 2에서 세 가지 특징을 확인할 수 있음.

- **수치 미분과의 본질적 차이**: 1단계의 수치 미분은 변수 수 n에 비례해 함수를
  2n번 호출해야 했음. `Value` 클래스는 forward pass 1회와 backward pass 1회만으로
  모든 변수의 gradient를 동시에 계산함. 이것이 자동 미분이 신경망 학습에 사용되는
  근본 이유임.

- **gradient 누적(accumulate)의 중요성**: `Value` 클래스에서 `self.gradient +=`로
  누적하는 이유는, 동일 노드가 여러 연산 경로에 등장할 때 각 경로의 gradient를 모두
  더해야 하기 때문임. `test_backward_gradient_accumulates`에서 f(x) = x² + x의
  gradient가 2x + 1 = 7로 올바르게 계산된 것이 이를 검증함.

- **PyTorch와의 관계**: PyTorch의 `autograd`는 `Value` 클래스와 동일한 원리
  (계산 그래프 + chain rule)로 동작하되, C++ 레벨 구현과 CUDA 가속을 추가한 것임.
  표 2에서 6개 케이스 모두 허용 오차(1e-5) 이내로 일치함을 확인함.

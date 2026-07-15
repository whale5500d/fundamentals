# Linear System & Gaussian Elimination

## 1.1 배경 (필요성)

- 선형 시스템(linear system, 또는 연립 선형 방정식, system of linear equations)은 m개의 선형 방정식으로 이루어진 집합을 의미합니다. 선형 방정식은 변수 x₁, ..., xₙ와 계수 a₁, ..., aₙ, 그리고 상수 b에 대한 관계식을 표현한 방정식입니다.
  ```
  a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ = b₁
  a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ = b₂
  ⋮
  aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ = bₘ
  ```
- 선형(linear)라는 이름으로 불리려면 아래 두 가지 조건을 만족해야 합니다.
  1. 각 변수의 차수(degree)가 정확히 1이어야 한다.
  2. 각 변수에 곱해지는 계수(coefficient) a_i는 상수이므로, 변수에 의존하면 안 된다.
- 이 선형 시스템을 행렬 표기(matrix notation)으로 압축하면 Ax = b입니다.

  ```
  Ax = b

  A ∈ ℝ^(m×n)  ← 계수 행렬 (coefficient matrix)
  x ∈ ℝⁿ       ← 미지수 벡터 (unknown vector)
  b ∈ ℝᵐ       ← 우변 벡터 (right-hand side vector)
  ```

- AI에서 선형 시스템이 등장하는 주요 맥락은 아래 두 가지입니다.
  1. **정규 방정식(normal equation)**: 선형 회귀(linear regression)에서 손실 함수(loss function)를 최소화하는 해석적 해(closed-form solution)는 $AᵀAx = Aᵀb$ 형태의 선형 시스템으로 귀결됨. gradient descent를 쓰지 않고 직접 풀 수 있음.
  2. **수치 최적화의 내부**: Newton's Method(뉴턴법) 등 2차 최적화 알고리즘은 매 iteration(반복)마다 Hessian(헤시안) 행렬을 계수 행렬로 갖는 선형 시스템을 풀어 update direction(갱신 방향)을 구함.

- 선형 시스템 Ax = b의 해는 반드시 아래 세 가지 경우 중 하나에 해당합니다.

  **선형 시스템 조건**
  | 경우 | 조건 | 예시 |
  |---|---|---|
  | 해가 유일(unique solution) | A가 정방(square)이고 비특이(non-singular) | n = m, det(A) ≠ 0 |
  | 해가 없음(no solution) | 방정식이 모순(inconsistent) | x = 1이면서 동시에 x = 2인 경우 |
  | 해가 무한(infinitely many solutions) | 방정식이 선형 종속(linearly dependent) | 두 방정식이 동일한 직선을 표현 |

  세 경우는 상호 배타적(mutually exclusive)이며 전체를 포괄합니다. "해가 정확히 2개"인 경우는 선형 시스템에서 존재하지 않습니다.

  > 현재 구현(`solve()`)은 **해가 유일한 경우**만 처리합니다. 피벗(pivot)이 0에 가까워 singular(특이)로 판단되면 `SingularMatrixError`를 발생시킵니다. 나머지 두 경우는 이후 단계(역행렬·행렬식, SVD)에서 다룹니다.

- 가우스 소거법은 이 선형 시스템(Ax = b)을 푸는 가장 기본적인 알고리즘입니다. 역행렬(inverse matrix)을 직접 구하지 않고도 해를 구할 수 있으며, 역행렬 계산 자체도 가우스 소거법을 확장(가우스-조던 소거법)해서 처리됩니다.

## 1.2 수학적 정의

1. 전방 소거(forward elimination)

첨가 행렬(augmented matrix) [A|b]에 행 연산(row operation)을 반복 적용해 상삼각 행렬(upper triangular matrix) 형태 [U|c]로 변환하는 방식입니다.

허용되는 행 연산은 세 가지입니다.

- 행 스케일링(row scaling): Rᵢ ← k·Rᵢ (k ≠ 0)
- 행 교환(row swap): Rᵢ ↔ Rⱼ
- 행 치환(row replacement) Rᵢ ← Rᵢ − m·Rⱼ, 여기서 `m = A_{ij} / A_{jj}`

각 열 j에서 피벗(pivot, 기준 원소)은 A\_{jj}입니다. 피벗 아래의 원소를 전부 0으로 만드는 것이 전방 소거의 목표입니다.

```
[A|b]  →  전방 소거  →  [U|c]

예: 3×3 시스템
[ 2  1 -1 |  8 ]       [ 2   1  -1 |  8  ]
[-3 -1  2 | -11]  →→   [ 0  0.5  0.5| 1  ]
[-2  1  2 | -3 ]       [ 0   0   1 | -1  ]
```

2. 후방 대입(back substitution)

[U|c]에서 xₙ부터 역순으로 해를 구합니다.

```
xₙ     = cₙ / U_{nn}
xₙ₋₁   = (cₙ₋₁ − U_{n-1,n}·xₙ) / U_{n-1,n-1}
⋮
x₁     = (c₁ − Σ_{j=2}^{n} U_{1j}·xⱼ) / U_{11}
```

일반화하면:

```
xᵢ = (cᵢ − Σ_{j=i+1}^{n} U_{ij}·xⱼ) / U_{ii}
```

3. 부분 피벗팅(partial pivoting)

전방 소거 중 피벗이 0이거나 매우 작으면 수치 불안정이 발생합니다. 이를 방지하기 위해 열 j에서 절댓값이 가장 큰 원소가 있는 행을 피벗 행으로 교환하는 전략이 부분 피벗팅입니다. 실용적인 구현에서 항상 적용합니다.

4. 시간 복잡도(time complexity)

전방 소거: O(n³), 후방 대입: O(n²) → 전체 O(n³)

5. 가우스 소거법에서 두 단계(전방 소거, 후방 대입)가 알고리즘 구조상 필요한 이유

- 가우스 소거법의 목표는 Ax = b를 푸는 것입니다. 그런데 Ax = b를 있는 그대로 풀기가 어려운 이유는 변수들이 방정식 전체에 얽혀있기 때문입니다.

```
2x₁ +  x₂ - x₃ =  8   ... (1)
     - x₂ + 2x₃ = -11  ... (2)
             x₃ = -1   ... (3)
```

- 이 형태는 풀려면, (3)에서 x₃ = -1을 구하고 → (2)에 대입해 x₂를 구하고 → (1)에 대입해 x₁을 구합니다. 이게 "후방 대입(back substitution)"입니다.

```
2x₁ +  x₂ -  x₃ =  8   ... (1)
-3x₁ -  x₂ + 2x₃ = -11  ... (2)
-2x₁ +  x₂ + 2x₃ = -3   ... (3)
```

- 실제 선형 시스템은 이러한 형태로 주어집니다. (2), (3)에 모든 변수가 얽혀 있어서 바로 대입할 수 없습니다. 그래서 먼저 이 형태를 "풀기 쉬운 형태"로 변환하기 위해 "전방 소거(forward elimination)"합니다.

- 두 단계의 역할
  - 전방 소거는 풀기 쉬운 형태(상삼각 행렬, upper triangular matrix)로 변환시킵니다.
  - 후방 대입은 변환된 상삼각 시스템을 역순으로 풀어서 해를 구합니다.
  - 두 단계는 독립적인 작업이 아니라, 하나의 알고리즘으로 구성되며 이를 가우스 소거법이라고 합니다.

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

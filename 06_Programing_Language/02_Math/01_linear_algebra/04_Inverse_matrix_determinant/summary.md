# 역행렬(Inverse Matrix)과 행렬식(Determinant)

## 1.1 배경 (필요성)

- 3단계에서 구현한 가우스 소거법은 특정 우변 벡터(right-hand side vector) b가 주어진 Ax = b를 푸는 알고리즘입니다. 그런데 동일한 계수 행렬(coefficient matrix) A에 대해 b가 다른 여러 시스템을 반복해서 풀어야 하는 상황이 생깁니다.
- 예를 들어 신경망의 Newton's Method(뉴턴법) 기반 최적화에서 매 iteration(반복)마다 동일한 Hessian(헤시안) 행렬 H에 대해 서로 다른 gradient(기울기 벡터) g로 Hx = g를 반복해서 풀어야 할 경우입니다. 이때 H의 역행렬 H^{-1}을 미리 구해두면 이후 풀이는 행렬-벡터곱(matrix-vector multiplication) x = H^{-1}g는 한 번으로 끝납니다.

- inverse matrix는 이 반복 풀이를 한 번의 사전 계산으로 대체합니다.
- determinant는 역행렬의 존재 여부를 판단하는 스칼라(scalar) 지표입니다. det(A) = 0이면 A는 특이 행렬(singular matrix)이고 역행렬이 존재하지 않습니다. 3단계 구현의 `SingularMatrixError`가 이 조건에 대응합니다.

- AI에서 구체적 등장 맥락은 아래 두 가지입니다.
  1. 정규 방정식(normal equation): 선형 회귀(linear regression)의 해석적 해(closed-form solution)는 x = $(A^T*A)^{-1}*A^T*b$입니다. A^{T}\*A의 역행렬이 직접 등장합니다.
  2. 공분산 행렬(covariance matrix) 역행렬: 가우시안 분포(Gaussian distribution) 기반 모델(예: Gaussian Process)에서 log-likeihood(로그 우도) 계산 시 공분산 행렬의 역행렬과 행렬식이 동시에 필요합니다.

## 1.2 수학적 정의

**역행렬**

- 정방 행렬(square matrix) A ∈ ℝ^(n×n)에 대해, A · A⁻¹ = A⁻¹ · A = I 조건을 만족하는 행렬 A⁻¹ ∈ ℝ^(n×n)을 A의 역행렬이라 합니다.
  - I: 단위 행렬(identity matrix) — 대각 원소가 1, 나머지가 0인 정방 행렬
  - 역행렬은 det(A) != 0인 경우에만 존재합니다.

**가우스-조던 소거법(Gauss-Jordan elimination)으로 역행렬 계산**

- 3단계의 가우스 소거법(전방 소거, 후방 대입)은 [U|c]에서 해를 꺼냅니다. 가우스-조던 소거법은 전방 소거에 더해 후방 소거(backward elimination)까지 수행하여 계수 행렬을 단위 행렬 I로 변환하는 방법입니다.

**행렬식**

- 라플라스 전개
  $$
  det(A) = Σ_{j=1}^{n} (-1)^{i+j} · A_{ij} · det(M_{ij})
  $$
  - $M_{ij}$: A에서 i번째 행과 j번째 열을 제거한 (n-1)\*(n-1) 부분 행렬
- 라플라스 전개는 재귀적(recursive) 정의이며, 시간 복잡도가 O(n!)로 비효율적입니다.

- 가우스 소거법
  $$
  det(A) = (-1)^s · Π_{i=1}^{n} U_{ii}
  $$
  - $s$: 행 교환(row swap) 횟수 (부분 피벗팅 과정에서 발생)
  - 실용적 구현에서는 가우스 소거법으로 상삼각 행렬 U를 구한 뒤, 대각 원소의 곱으로 행렬식을 계산합니다.

## 1.3 순수 Python으로 구현 및 테스트

- [[구현 코드 바로가기](./pure.py)]
- [[테스트 코드 바로가기](./test.py)]

## 1.4 NumPy와 비교 및 실행 결과 분석

- [분석 코드 바로가기](./benchmark.py)

- 실행 명령어

  ```bash
  (.venv) python benchmark.py
  ```

- 실행 결과

세 가지 특징을 확인할 수 있음.

- **inverse가 determinant보다 일관되게 느림**: inverse는 [A|I] 구성으로 열이 2n개인 확장 행렬을 처리하므로 루프 횟수가 determinant의 약 2배임. NumPy에서도 동일한 경향이 나타나며, 내부적으로 dgetrf (LU 분해) 이후 inverse는 dgetri를 추가 호출하기 때문임.
- **n=500에서 inverse speedup이 843x**: O(n³) 복잡도에서 3단계 선형 시스템(solve)의 n=500 speedup 645x보다 높음. inverse는 [A|I]의 오른쪽 절반(n열)에도 동일한 행 연산을 적용하므로 Python 루프가 더 많이 발생해 순수 Python 구현의 절대 비용이 더 크기 때문임.
- **RuntimeWarning — overflow in det (n=500)**: NumPy의 det 경고는 n=500 대각 우세 행렬의 행렬식이 float64 (배정밀도 부동소수점, 64비트) 표현 범위(~1.8×10³⁰⁸)를 초과할 만큼 매우 크기 때문에 발생함. 실용 코드에서는 numpy.linalg.slogdet (행렬식의 로그(log) 값과 부호를 반환)를 사용해 overflow(오버플로)를 회피함.

## 1.5 한계: 역행렬 직접 계산의 비효율성

- 역행렬을 구한 뒤 선현 시스템을 푸는 방식은 수치적으로 비효율적입니다. 역행렬 계산은 O(n^3)이고 이후 행렬-벡터곱도 O(n^2)인 반면, 3단계의 solve()는 O(n^3) 한 번으로 동일한 결과를 얻습니다. 역행렬은 b가 자주 바뀌는 반폭 풀이 맥락에서 사전 계산(precomputation)할 때만 효율적입니다.

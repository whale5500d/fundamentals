# Eigenvalue(고유값)과 Eigenvector(고유벡터)

## 1.1 배경 (필요성)

- 고유값과 고유벡터는 행렬이 표현하는 선형 변환(linear transformation)의 본질적인 방향과 크기를 드러내는 도구입니다. 선형 변환 A를 임의의 벡터 v에 적용하면 일반적으로 방향과 크기가 모두 바뀝니다. 그런데 특정 벡터들은 변환 후에도 방향이 유지되고 크기만 스칼라 배로 변합니다. 이 벡터가 고유벡터(eigenvector)이고, 그 스칼라 배율을 고유값(eigenvalue)이라 합니다.

- AI에서 등장하는 주요 맥락은 두 가지입니다.
  - PCA(Principal Component Analysis, 주성분 분석): 데이터의 공분산 행렬(covariance matrix)을 고유값 분해(eigendecomposition)하면, 고유벡터는 데이터가 가장 많이 퍼진 방향(principal component)을 나타내고, 고유값은 그 방향의 분산(variance) 크기를 나타냅니다. 가장 큰 고유값에 대응하는 고유벡터 방향으로 데이터를 투영(projection)하면 정보 손실을 최소화하여 차원을 축소할 수 있습니다.
  - Spectral Graph Theory(스펙트럴 그래프 이론): 그래프의 Laplacian(라플라시안) 행렬의 고유값, 고유벡터는 그래프의 연결 구조를 분석하는 데 사용됩니다. GNN(Graph Neural Network, 그래프 신경망)의 이론적 기반이 됨.

## 1.2 수학적 정의

- 정방 행렬(square matrix) A ∈ ℝ^(n×n)에 대해 다음 조건을 만족하는 스칼라 λ ∈ ℝ와 영벡터가 아닌 벡터 v ∈ ℝⁿ의 쌍을 고유쌍(eigenpair)이라 합니다.

```
Av = λv

λ: 고유값(eigenvalue)
v: 고유벡터(eigenvector), v ≠ 0
```

- 이 식의 의미: 행렬 A가 벡터 v에 작용했을 때 방향은 유지되고 크기만 λ배가 됩니다.

**고유값 방정식(characteristic equation)**
Av = λv를 정리하면:

```
Av - λv = 0
(A - λI)v = 0
```

v ≠ 0인 해가 존재하려면 (A - λI)가 singular(특이 행렬)이어야 합니다.

따라서:

```
det(A - λI) = 0
```

이를 고유값 방정식(characteristic equation) 또는 특정 방정식이라 합니다.n×n 행렬의 경우 이 방정식은 λ에 대한 n차 다항식이므로 최대 n개의 고유값이 존재함.

**거듭제곱법(power iteration)**
고유값 방정식을 직접 풀면 O(n³) 이상의 비용이 들고 구현이 복잡합니다. 거듭제곱법은 절댓값이 가장 큰 고유값(지배 고유값, dominant eigenvalue)과 대응하는 고유벡터를 반복적으로 근사하는 알고리즘입니다.

- 거듭제곱법 과정
  1. 임의의 초기 벡터 v₀ 선택 (단, 지배 고유벡터와 직교하지 않아야 함)
  2. 반복:
     ```
      w_{k+1} = A · v_k       ← 행렬-벡터곱 적용
      v_{k+1} = w_{k+1} / ‖w_{k+1}‖  ← 정규화(normalization)
     ```
  3. 수렴 시 v_k → 지배 고유벡터, λ = vᵀAv (레일리 지수, Rayleigh quotient)
- 수렴 속도는 |λ₁/λ₂|에 의존합니다. λ₁이 지배 고유값, λ₂가 두 번째로 큰 고유값일 때 이 비율이 클수록 빠르게 수렴합니다.

시간 복잡도

- 반복 1회당 행렬-벡터곱 O(n^2), 수렴까지 k회 반복 -> 전체 O(k\*n^2)

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

  ```bash
  ※ 순수 Python은 지배 고유값 1개, NumPy는 전체 고유값 계산

  n=   10 | 순수 Python(power iteration):      2.754 ms | NumPy(eig, 전체):    0.096 ms | speedup:    28.6x
  n=   50 | 순수 Python(power iteration):    327.200 ms | NumPy(eig, 전체):    1.489 ms | speedup:   219.7x
  n=  100 | 순수 Python(power iteration):   1293.943 ms | NumPy(eig, 전체):    6.738 ms | speedup:   192.0x
  n=  200 | 순수 Python(power iteration):   5050.166 ms | NumPy(eig, 전체):   26.047 ms | speedup:   193.9x
  ```

두 가지 특징을 확인할 수 있음.

- **알고리즘 목적의 비대칭성**: 순수 Python의 `power_iteration`은 지배 고유값 1개만 근사하는 반면, NumPy의 `numpy.linalg.eig`는 LAPACK의 `dgeev` 루틴을 통해 QR 알고리즘(QR algorithm — 수치선형대수 알고리즘, 행렬을 반복적으로 QR 분해해 모든 고유값을 구하는 방법)으로 전체 고유값·고유벡터를 한 번에 계산함. 즉 NumPy가 더 많은 결과를 내면서도 더 빠른 것임. speedup 수치가 이전 단계들보다 상대적으로 낮은 이유는 순수 Python이 계산량이 적은 단일 고유값만 추적하기 때문임.

- **n=50에서 speedup 정점(219.7x) 후 감소**: `power_iteration`의 수렴 속도는 |λ₁/λ₂| 비율에 의존함. n이 커질수록 고유값들이 밀집(clustering — 수치해석 용어, 고유값들이 서로 가까운 값을 가지는 현상)되어 수렴에 더 많은 반복이 필요해짐. 반면 NumPy의 QR 알고리즘은 O(n³) 복잡도로 n 증가에 따라 예측 가능하게 증가함. n이 클수록 두 알고리즘의 실제 반복 횟수 차이가 줄어들어 speedup이 감소하는 것임.

## 한계: 거듭제곱법의 적용 범위

거듭제곱법은 지배 고유값 하나만 구할 수 있음. PCA에서 상위 k개의 주성분(principal component)이 필요한 경우에는 deflation (디플레이션 — 수치선형대수 용어, 이미 구한 고유벡터 방향을 제거하고 다음 고유값을 구하는 방법)을 반복 적용하거나, 처음부터 QR 알고리즘 또는 SVD (특이값 분해)를 사용해야 함. 이것이 6단계(SVD)로 이어지는 연결점임.

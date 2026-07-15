# 행렬

## 1.1 배경 (필요성)

행렬(matrix)은 개별 벡터를 2차원의 구조로 만든 형태입니다. AI에서는 행렬이 필요한데, 그 이유는 아래 세 가지입니다.

1. 데이터 표현: n개의 샘플, 각 샘플이 d차원 벡터라면 전체 데이터셋은 n\*d 행렬로 표현합니다. 실제로 배치 학습(batch training)에서 입력 데이터는 항상 행렬 단위로 처리합니다.

2. 선형 변환(linear transformation) 표현: 신경망의 각 층(layer)은 $y = W*x$로 정의합니다. matrix multiplication이 선형 변환의 composition을 표현하기 때문입니다.

3. transpose의 역할: backpropagation에서 gradient를 앞 층으로 전달할 때 가중치 행렬의 전치 Wᵀ가 등장합니다. 또한 Gram matrix AᵀA 형태는 공분산 행렬(covariance matrix), attention(어텐션) 스코어 계산 등에 반복적으로 사용

## 1.2 수학적 정의

행렬 A ∈ ℝ^(m×n), B ∈ ℝ^(m×n), C ∈ ℝ^(n×p) (인덱스 i = 1,...,m / j = 1,...,n / k = 1,...,p)

행렬 덧셈(matrix addition)
$(A + B){ij} = A{ij} + B\_{ij}$
→ 두 행렬의 shape(형태)이 동일해야 정의됨.

전치(transpose)
$(Aᵀ){ij} = A{ji}$
→ m×n 행렬의 전치는 n×m 행렬. 행과 열을 교환하는 연산.

행렬곱(matrix multiplication)
$(A · C){ik} = Σ(j=1 to n) A{ij} × C\_{jk}$
→ A의 열 수(n)와 C의 행 수(n)가 일치해야 정의됨. 결과는 m×p 행렬.
→ 시간 복잡도(time complexity): O(m × n × p). 정방 행렬(square matrix, n×n)이면 O(n³).

행렬곱은 교환법칙(commutative law)이 성립하지 않음: A·C ≠ C·A (일반적으로).

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

  ```bash
  ======================================================================
  행렬 연산 속도 비교 (n×n 정방 행렬, 반복 횟수 = 5)
  ======================================================================

  --- n×n = 10×10 (O(n²) 연산) ---
  연산                  순수 Python (ms)     NumPy (ms)    speedup
  -------------------------------------------------------------
  matrix_add                  0.0078         0.0008       9.4x
  transpose                   0.0045         0.0010       4.4x

  --- n×n = 100×100 (O(n²) 연산) ---
  연산                  순수 Python (ms)     NumPy (ms)    speedup
  -------------------------------------------------------------
  matrix_add                  0.5964         0.0045     133.3x
  transpose                   0.3097         0.0010     317.6x

  --- n×n = 500×500 (O(n²) 연산) ---
  연산                  순수 Python (ms)     NumPy (ms)    speedup
  -------------------------------------------------------------
  matrix_add                 17.4918         0.4099      42.7x
  transpose                   9.3941         0.0039    2440.0x

  --- n×n = 1000×1000 (O(n²) 연산) ---
  연산                  순수 Python (ms)     NumPy (ms)    speedup
  -------------------------------------------------------------
  matrix_add                 67.1600         0.7064      95.1x
  transpose                  33.8988         0.0041    8184.6x

  --- matmul (O(n³) 연산) ---
  연산                  순수 Python (ms)     NumPy (ms)    speedup   크기
  ----------------------------------------------------------------------
  matmul                      0.1040         0.0106       9.8x   ← n=10
  matmul                      9.4592         0.0240     393.9x   ← n=50
  matmul                     71.9549         0.0259    2780.9x   ← n=100
  matmul                    561.4228         0.0850    6606.3x   ← n=200
  ```

두 가지 특징을 확인할 수 있음.

1. **transpose의 극단적 speedup**: n=1,000에서 33,8988로 다른 연산과 비교할 수 없는 수준임. 순수 Python의 transpose는 n²번의 원소 접근과 리스트 생성을 수행하는 반면, NumPy의 transpose는 실제로 데이터를 복사하지 않음. 내부적으로 stride(스트라이드, 메모리 접근 간격)만 교환하는 O(1) 연산으로 처리되기 때문임. 즉 NumPy의 .T는 메모리 레이아웃 자체는 그대로 두고 "행과 열을 어떻게 읽을지"에 대한 메타데이터만 변경함.

2. **matmul의 speedup이 n에 따라 급격히 증가**: O(n³) 복잡도로 인해 순수 Python은 n=200에서 이미 660ms가 소요됨. NumPy는 내부적으로 BLAS(Basic Linear Algebra Subprograms)의 DGEMM(Double General Matrix Multiply) 루틴을 호출하여 캐시(cache) 친화적 블록 행렬 분해와 SIMD(Single Instruction Multiple Data) 명령어를 결합해 처리함. 이것이 n이 클수록 speedup이 누적되는 이유임.

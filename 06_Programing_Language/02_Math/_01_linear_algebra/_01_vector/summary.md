# 벡터

## 1.1 배경 (필요성)

벡터는 AI 모델에서 데이터를 표현하는 기본 단위입니다. 이미지 한 장, 단어 하나의 임베딩, 신경망 한 층의 출력 모두 벡터로 표현합니다.

벡터 연산이 필요한 이유는 다음과 같습니다.

- 덧셈과 스칼라곱은 신경망의 "가중치 갱신"에 사용되는 연산
- 내적은 "두 벡터의 유사도"를 측정하거나, 신경망 한 뉴런의 "가중합"에 사용되는 연산
- norm은 벡터의 크기(magnitude)를 측정하며, graident clipping(크기 비교) 또는 regularization에서 가중치 크기 제한에 사용

## 1.2 수학적 정의

벡터 a, b ∈ ℝⁿ에 대해 (n차원 실수 벡터, 인덱스 i = 1, ..., n):

1. addition: $(a + b)_i = a_i + b_i$
2. scalar multiplication: $(c · a)_i = c · a_i$
3. dot product(내적): $a · b = Σ(i=1 to n) a_i × b_i$
4. norm(L2 norm 기준): $‖a‖ = √(Σ(i=1 to n) a_i²) = √(a · a)$
   - (L2 norm은 내적으로부터 정의되는 종속 관계)

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
  벡터 연산 속도 비교 (n = 벡터 차원 수, 반복 횟수 = 10)

   --- n = 10 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                       0.0009         0.0006       1.6x
   scalar_multiply                  0.0007         0.0008       0.8x
   dot_product                      0.0012         0.0008       1.5x
   norm                             0.0012         0.0015       0.8x

   --- n = 100 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                       0.0041         0.0004       9.3x
   scalar_multiply                  0.0038         0.0006       6.7x
   dot_product                      0.0061         0.0005      12.1x
   norm                             0.0061         0.0010       5.8x

   --- n = 1,000 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                       0.0478         0.0007      65.9x
   scalar_multiply                  0.0429         0.0008      53.4x
   dot_product                      0.0630         0.0010      64.6x
   norm                             0.0625         0.0016      39.6x

   --- n = 10,000 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                       0.4765         0.0050      95.9x
   scalar_multiply                  0.4473         0.0052      86.0x
   dot_product                      0.6542         0.0029     228.5x
   norm                             0.6419         0.0034     187.2x

   --- n = 100,000 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                       5.0875         0.0486     104.8x
   scalar_multiply                  4.3674         0.0274     159.4x
   dot_product                      7.4945         0.0079     949.2x
   norm                             7.0342         0.0097     722.7x

   --- n = 1,000,000 ---
   연산                       순수 Python (ms)     NumPy (ms)    speedup
   ------------------------------------------------------------------
   vector_add                      53.0379         0.6146      86.3x
   scalar_multiply                 51.8171         0.2452     211.3x
   dot_product                     73.8856         0.1256     588.4x
   norm                            73.5488         0.1359     541.1x
  ```

1. 주요 특징

n이 커질수록 NumPy의 우위가 뚜렷해고, n=1,000,000에서는 무려 54.5배 빠릅니다. 순수 Python의 dot_product는 Python 인터프리터가 매 반복마다 바이트코드(bytecode)를 해석하는 오버헤드를 가지는 반면, NumPy는 내부적으로 C로 구현된 BLAS(Basic Linear Algebra Subprograms) 루틴을 호출하여 반복문 없이 메모리 연속 블록에 대해 SIMD(Single Instruction Multiple Data)로 연산을 수행합니다. 이것이 vectorization의 본질입니다.

이 결과는 신경망에서 왜 항상 NumPy, PyTorch 같은 벡터화 라이브러리를 사용하는지 보여주는 근거입니다. 신경망의 벡터 차원은 보통 수백~수만 단위이므로, 순수 Python 구현만으로는 실용적이지 않습니다.

2. 부수 특징

n=10처럼 매우 작은 차원에서는 NumPy가 더 느리기도 합니다. 이는 NumPy 호출 자체에 고정 오버해드(array 생성, 타입 체크 등)가 있어, 데이터가 작을 때는 이 오버헤드가 실제 연산 시간보다 클 수 있기 때문입니다.

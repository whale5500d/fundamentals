# SVD (Singualr Value Decomposition, 특이값 분해)

## 1.1 배경 (필요성)

- 5단계의 고유값 분해(eigendecomposition)는 정방 행렬(square matrix)에만 적용 가능하고, 대칭 행렬(symmetric matrix)이 아닌 경우 복소수 고유값이 등장할 수 있음. 실제 데이터는 대부분 비정방(non-square) 행렬임(n개 샘플, d개 특징이면 n×d 행렬). 이 한계를 극복하는 일반화된 분해가 SVD임.

- AI에서 SVD가 등장하는 주요 맥락은 세 가지임.
  - PCA (주성분 분석): 데이터 행렬 X에 직접 SVD를 적용하면 공분산 행렬을 명시적으로 계산하지 않고도 주성분(principal component)을 구할 수 있음. 수치적으로 더 안정적이어서 실용 PCA 구현(예: sklearn.decomposition.PCA)은 내부적으로 SVD를 사용함.
  - 추천 시스템(recommendation system): 사용자-아이템 평점 행렬을 SVD로 분해하면 잠재 요인(latent factor)을 추출할 수 있음. Matrix Factorization (행렬 분해 — 추천 시스템 용어) 계열 알고리즘의 이론적 기반임.
  - 저랭크 근사(low-rank approximation): 큰 행렬을 상위 k개의 특이값만으로 근사하면 노이즈 제거와 압축이 동시에 가능함. 이미지 압축, 자연어 처리의 LSA (Latent Semantic Analysis, 잠재 의미 분석) 등에 활용됨.

## 1.2 수학적 정의

- 임의의 행렬 A ∈ ℝ^(m×n)에 대해 다음과 같이 세 행렬의 곱으로 분해할 수 있음.

```
A = U · Σ · Vᵀ

U ∈ ℝ^(m×m) : 좌 특이 벡터 행렬(left singular vectors) — 열벡터가 정규직교 기저(orthonormal basis)
Σ ∈ ℝ^(m×n) : 특이값 행렬(singular value matrix) — 대각 원소 σ₁ ≥ σ₂ ≥ ... ≥ 0
V ∈ ℝ^(n×n) : 우 특이 벡터 행렬(right singular vectors) — 열벡터가 정규직교 기저
```

**특이값(singular value)과 고유값의 관계**
SVD는 고유값 분해의 일반화임. 다음 관계가 성립함.

```
AᵀA = V · Σᵀ Σ · Vᵀ   ← AᵀA의 고유값 분해
AAᵀ = U · Σ Σᵀ · Uᵀ   ← AAᵀ의 고유값 분해

σᵢ = √(λᵢ(AᵀA))       ← 특이값 = AᵀA의 고유값의 양의 제곱근
```

즉 V는 AᵀA의 고유벡터 행렬, U는 AAᵀ의 고유벡터 행렬, Σ의 대각 원소는 AᵀA 고유값의 제곱근임.

**저랭크 근사(low-rank approximation)**
SVD의 핵심 활용인 Eckart-Young 정리(Eckart-Young theorem)에 의하면, 상위 k개의 특이값만으로 구성한 행렬 Aₖ가 랭크(rank)-k 행렬 중 A에 가장 가까운 근사임.

```
Aₖ = Σᵢ₌₁ᵏ σᵢ · uᵢ · vᵢᵀ

‖A - Aₖ‖_F = √(σₖ₊₁² + ... + σᵣ²)   (‖·‖_F: 프로베니우스 노름, Frobenius norm)
```

**직접 구현을 생략하는 이유**
SVD의 수치적 구현(Golub-Reinsch 알고리즘 등)은 Householder 변환(Householder transformation), 이중 대각화(bidiagonalization), QR 반복(QR iteration) 등 복잡한 수치선형대수 기법을 조합해야 함. 구현 자체가 수백 줄 이상이며, 수치 안정성 확보가 매우 까다로움. 원리 이해 후 numpy.linalg.svd를 활용하는 것이 실용적으로 적절함.

## 1.3 순수 Python으로 구현 및 테스트

- [[구현 코드 바로가기](./pure.py)]
- [[테스트 코드 바로가기](./test.py)]

실행 결과가 이론과 정확히 일치함. 결과를 항목별로 확인함.

- 구현 결과

  ```bash
  ============================================================
  1. SVD 분해: A = U·Σ·Vᵀ
  ============================================================
  A shape   : (4, 3)
  U shape   : (4, 4)
  Σ (특이값): [5.2915 2.     2.    ]
  Vt shape  : (3, 3)

  2. 재구성 검증: U·Σ·Vᵀ ≈ A
  재구성 오차(Frobenius norm): 1.58e-15

  3. 정규직교성(orthonormality) 검증: UᵀU = I, VᵀV = I
  UᵀU - I 최대 오차: 4.44e-16
  VᵀV - I 최대 오차: 1.39e-16

  4. 특이값과 AᵀA 고유값의 관계: σᵢ = √λᵢ(AᵀA)
  σᵢ²          : [28.  4.  4.]
  λᵢ(AᵀA)     : [28.  4.  4.]
  최대 오차    : 7.11e-15

  5. 저랭크 근사(low-rank approximation) — Eckart-Young 정리 검증
    rank=1: 근사 오차=2.8284, 이론값=2.8284, 정보 보존율=52.9%
    rank=2: 근사 오차=2.0000, 이론값=2.0000, 정보 보존율=66.7%
    rank=3: 근사 오차=0.0000, 이론값=0.0000, 정보 보존율=100.0%
  ```

1. SVD 분해 결과
   4×3 비정방 행렬에 대해 U(4×4), Σ(특이값 벡터), Vᵀ(3×3)로 분해됨. 특이값은 σ₁=5.2915, σ₂=σ₃=2.0으로 σ₁이 지배적임.
2. 재구성 오차 9.29e-16
   U·Σ·Vᵀ로 A를 재구성했을 때 오차가 기계 엡실론(machine epsilon — 수치해석 용어, float64의 최소 표현 단위 ~2.22e-16) 수준임. 분해가 정확히 이루어진 것을 확인함.
3. 정규직교성 오차 ~1e-16
   UᵀU = I, VᵀV = I가 기계 엡실론 수준의 오차로 성립함. U, V가 정규직교 기저(orthonormal basis)임을 확인함.
4. 특이값과 AᵀA 고유값의 관계
   σᵢ² = λᵢ(AᵀA)가 오차 7.11e-15 수준으로 성립함. SVD가 고유값 분해의 일반화임을 수치적으로 확인함.
5. Eckart-Young 정리 검증
   근사 오차와 이론값이 완전히 일치함. rank=1에서 정보 보존율이 52.9%에 불과하지만, rank=2에서 66.7%, rank=3(전체)에서 100%로 수렴함. σ₂=σ₃=2.0으로 동일하므로 rank=2에서 rank=3으로의 오차 감소분이 rank=1→2와 동일함.

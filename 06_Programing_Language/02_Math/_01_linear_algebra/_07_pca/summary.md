# PCA (Principal Component Analysis, 주성분 분석)

## 1.1 배경 (필요성)

- 고차원 데이터는 두 가지 문제를 가짐.
  - 차원의 저주(curse of dimensionality): 차원이 늘어날수록 데이터 포인트 간 거리가 균등해지고, 모델 학습에 필요한 샘플 수가 기하급수적으로 증가함. 머신러닝 모델의 일반화(generalization) 성능이 저하됨.
  - 특징 간 상관관계(correlation): 실제 데이터의 특징(feature)들은 서로 독립적이지 않고 상관관계를 가짐. 예를 들어 키와 몸무게, 광고 지출과 매출은 강한 상관관계를 가짐. 이 중복된 정보를 제거하면 더 적은 차원으로 데이터를 표현할 수 있음.

- PCA는 데이터의 분산(variance)을 최대한 보존하는 방향(주성분, principal component)으로 좌표계를 회전시켜 저차원으로 투영(projection)하는 기법임. 6단계에서 확인했듯이 실용 구현은 SVD를 사용하며, 이론적 기반은 공분산 행렬의 고유값 분해임.

- AI에서의 주요 활용 맥락은 다음 두 가지임.
  - 전처리(preprocessing): 고차원 입력 데이터를 저차원으로 압축해 모델 학습 비용을 줄임. 특히 이미지, 유전체(genomics) 데이터처럼 특징 수가 샘플 수보다 많은 경우에 유효함.
  - 시각화(visualization): 고차원 데이터를 2~3차원으로 압축해 클러스터(cluster — 군집) 구조를 시각적으로 확인함. t-SNE, UMAP 같은 비선형 차원 축소 기법의 전처리 단계로도 사용됨.

## 1.2 수학적 정의

**입력**: 데이터 행렬 X ∈ ℝ^(n×d) — n개 샘플, d개 특징

**전체 파이프라인**

```
1. 평균 중심화(mean centering):
   μ = (1/n) · Σᵢ xᵢ           ← 각 특징의 평균
   X_centered = X - μ          ← 평균을 빼서 원점 중심으로 이동

2. 공분산 행렬(covariance matrix) 계산:
   C = (1/(n-1)) · X_centeredᵀ · X_centered    ← shape = d×d

3. 고유값 분해(eigendecomposition):
   C = V · Λ · Vᵀ
   V = [v₁ | v₂ | ... | vd]   ← 고유벡터(주성분 방향)
   Λ = diag(λ₁, λ₂, ..., λd)  ← 고유값(각 주성분의 분산 크기), λ₁ ≥ λ₂ ≥ ...

4. 차원 축소(dimensionality reduction):
   W = V[:, :k]                ← 상위 k개 주성분 벡터, shape = d×k
   X_reduced = X_centered · W  ← 투영(projection), shape = n×k

5. 분산 설명 비율(explained variance ratio):
   explained_ratio_i = λᵢ / Σⱼ λⱼ
```

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
  PCA 속도 비교 — 순수 Python vs sklearn (단위: ms, number_of_components=2)
  | n | d | 순수 Python (ms) | sklearn (ms) | speedup |
  |---|---|---|---|---|
  | 100 | 10 | 1.271 | 0.371 | 3.4x |
  | 100 | 50 | 20.903 | 1.695 | 12.3x |
  | 500 | 50 | 100.900 | 0.877 | 115.0x |
  | 500 | 100 | 380.586 | 3.664 | 103.9x |
  | 1,000 | 100 | 780.421 | 1.186 | 658.1x |
  | 1,000 | 200 | 2,991.196 | 3.073 | 973.3x |

세 가지 특징을 확인할 수 있음.

- **병목은 공분산 행렬 계산(covariance matrix computation)**: 순수 Python 구현에서
  가장 비용이 큰 단계는 `matmul(X_centeredᵀ, X_centered)`임. 이 연산은 O(n·d²) 복잡도이며, d가 커질수록 비용이 급격히 증가함. n=500, d=50→100 전환 시 순수 Python이 100.9ms→380.6ms(약 3.8배)로 늘어난 반면 sklearn은 0.877ms→3.664ms(약 4.2배)로 유사한 증가율을 보임. sklearn은 내부적으로 SVD를 직접 데이터 행렬 X에 적용하므로 공분산 행렬을 명시적으로 계산하지 않아 수치적으로도 더 안정적임.

- **n이 d보다 속도에 더 큰 영향**: d=100으로 고정했을 때 n=500→1000 전환 시 순수 Python은 380.6ms→780.4ms(약 2.1배)로 증가함. 반면 sklearn은 3.664ms→1.186ms로 오히려 감소함. sklearn 내부의 randomized SVD (확률적 SVD — 대규모 행렬에 대해 근사 SVD를 빠르게 계산하는 알고리즘)는 n이 클수록 샘플링 효율이 높아지기 때문임.

- **한계: 전체 고유값 분해의 비효율성**: 순수 Python 구현은 공분산 행렬의 전체 고유값을 구한 뒤 상위 k개만 선택함. k가 d보다 훨씬 작은 경우(예: d=200, k=2) 대부분의 고유값 계산이 낭비됨. n=1000, d=200에서 speedup이 973.3x에 달하는 것이 이를 단적으로 보여줌. 실용 구현에서는 상위 k개만 구하는 truncated SVD (절단 SVD — scikit-learn의 `TruncatedSVD`, scipy의 `svds`)를 사용해 이 낭비를 제거함.

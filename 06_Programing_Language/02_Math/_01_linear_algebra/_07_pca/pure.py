"""
7. PCA(주성분 분석, Principal Component Analysis) - 순수 Python 구현

파이프라인:
    1. 평균 중심화(mean centering)
    2. 공분산 행렬(covariance matrix) 계산
    3. 고유값 분해(eigendecomposition) — numpy.linalg.eigh 사용
       (대칭 행렬 전용 고유값 분해. eig보다 수치적으로 안정적이고 빠름)
    4. 차원 축소(dimensionality reduction) — 상위 k개 주성분으로 투영(projection)
    5. 분산 설명 비율(explained variance ratio) 계산

의존성:
    numpy: 공분산 행렬 고유값 분해에만 사용 (행렬 연산은 순수 Python 구현 활용)
"""

import numpy as np

from _01_linear_algebra._02_matrix.pure import matmul, transpose


def mean_center(X: list) -> tuple:
    """평균 중심화(mean centering): X_centered = X - μ

    Args:
        X: 데이터 행렬, shape = n×d

    Returns:
        (X_centered, mean_vector) 튜플
            X_centered  : 평균이 제거된 데이터 행렬, shape = n×d
            mean_vector : 각 특징의 평균 벡터, shape = d
    """
    number_of_samples = len(X)
    number_of_features = len(X[0])

    mean_vector = [
        sum(X[i][j] for i in range(number_of_samples)) / number_of_samples
        for j in range(number_of_features)
    ]

    X_centered = [
        [X[i][j] - mean_vector[j] for j in range(number_of_features)]
        for i in range(number_of_samples)
    ]

    return X_centered, mean_vector


def covariance_matrix(X_centered: list) -> list:
    """공분산 행렬(covariance matrix) 계산: C = (1/(n-1)) · X_centeredᵀ · X_centered

    Args:
        X_centered: 평균 중심화된 데이터 행렬, shape = n×d

    Returns:
        공분산 행렬 C, shape = d×d
    """
    number_of_samples = len(X_centered)
    X_transposed = transpose(X_centered)               # d×n
    XtX = matmul(X_transposed, X_centered)             # d×d

    d = len(XtX)
    return [
        [XtX[i][j] / (number_of_samples - 1) for j in range(d)]
        for i in range(d)
    ]


def fit(X: list, number_of_components: int) -> dict:
    """PCA 학습: 주성분 방향과 분산 설명 비율 계산

    Args:
        X                    : 데이터 행렬, shape = n×d
        number_of_components : 축소할 목표 차원 수 k (k ≤ d)

    Returns:
        다음 키를 포함하는 dict:
            components          : 주성분 벡터 행렬 W, shape = d×k (열이 주성분 방향)
            explained_variance  : 각 주성분의 분산(고유값), shape = k
            explained_variance_ratio: 각 주성분의 분산 설명 비율, shape = k
            mean_vector         : 평균 벡터, shape = d
    """
    number_of_features = len(X[0])
    assert number_of_components <= number_of_features, (
        f"number_of_components({number_of_components})는 "
        f"특징 수({number_of_features}) 이하이어야 함"
    )

    # 1. 평균 중심화
    X_centered, mean_vector = mean_center(X)

    # 2. 공분산 행렬 계산
    C = covariance_matrix(X_centered)

    # 3. 고유값 분해 (공분산 행렬은 대칭 행렬이므로 eigh 사용)
    #    eigh: 대칭(Hermitian) 행렬 전용. 고유값을 오름차순으로 반환함.
    eigenvalues, eigenvectors = np.linalg.eigh(np.array(C))

    # 내림차순 정렬 (분산이 큰 주성분부터)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # 4. 상위 k개 주성분 선택
    components = eigenvectors[:, :number_of_components].tolist()  # d×k

    # 5. 분산 설명 비율 계산
    total_variance = float(np.sum(eigenvalues))
    explained_variance = eigenvalues[:number_of_components].tolist()
    explained_variance_ratio = [v / total_variance for v in explained_variance]

    return {
        "components":               components,
        "explained_variance":       explained_variance,
        "explained_variance_ratio": explained_variance_ratio,
        "mean_vector":              mean_vector,
    }


def transform(X: list, pca_model: dict) -> list:
    """PCA 변환: X_reduced = X_centered · W

    Args:
        X        : 변환할 데이터 행렬, shape = n×d
        pca_model: fit()의 반환값

    Returns:
        저차원으로 투영된 데이터 행렬, shape = n×k
    """
    mean_vector = pca_model["mean_vector"]
    components = pca_model["components"]   # d×k

    number_of_samples = len(X)
    number_of_features = len(X[0])

    # 평균 중심화
    X_centered = [
        [X[i][j] - mean_vector[j] for j in range(number_of_features)]
        for i in range(number_of_samples)
    ]

    # X_centered(n×d) · components(d×k) → n×k
    return matmul(X_centered, components)


def fit_transform(X: list, number_of_components: int) -> tuple:
    """PCA 학습 및 변환을 한 번에 수행

    Args:
        X                    : 데이터 행렬, shape = n×d
        number_of_components : 축소할 목표 차원 수 k

    Returns:
        (X_reduced, pca_model) 튜플
    """
    pca_model = fit(X, number_of_components)
    X_reduced = transform(X, pca_model)
    return X_reduced, pca_model
"""
7. PCA(주성분 분석, Principal Component Analysis) - 테스트 코드

검증 방식: 순수 Python 구현 결과 vs sklearn.decomposition.PCA 결과 비교

고유벡터 부호(sign) 주의:
    주성분 벡터는 방향만 의미 있고 부호는 임의적임. (+v와 -v는 동일한 주성분)
    따라서 투영 결과의 열(column)별로 부호를 맞춘 뒤 비교함.
"""

import math
import numpy as np
import pytest
from sklearn.decomposition import PCA as SklearnPCA

from pure import mean_center, covariance_matrix, fit, transform, fit_transform


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def sign_corrected_allclose(
    result: list,
    expected: np.ndarray,
    tolerance: float = 1e-6,
) -> bool:
    """열별 부호를 보정한 뒤 근사 일치 여부 반환"""
    result_np = np.array(result)
    for column_index in range(result_np.shape[1]):
        if np.dot(result_np[:, column_index], expected[:, column_index]) < 0:
            result_np[:, column_index] *= -1
    return np.allclose(result_np, expected, atol=tolerance)


# ── 평균 중심화(mean centering) 검증 ─────────────────────────────────────────

def test_mean_center_removes_mean():
    X = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    X_centered, mean_vector = mean_center(X)

    # 중심화 후 각 열의 평균이 0이어야 함
    number_of_samples = len(X_centered)
    number_of_features = len(X_centered[0])
    for j in range(number_of_features):
        column_mean = sum(X_centered[i][j] for i in range(number_of_samples)) / number_of_samples
        assert math.isclose(column_mean, 0.0, abs_tol=1e-12)


def test_mean_vector_values():
    X = [[1.0, 4.0], [3.0, 2.0], [5.0, 6.0]]
    _, mean_vector = mean_center(X)
    assert math.isclose(mean_vector[0], 3.0, abs_tol=1e-12)
    assert math.isclose(mean_vector[1], 4.0, abs_tol=1e-12)


# ── 공분산 행렬(covariance matrix) 검증 ──────────────────────────────────────

def test_covariance_matrix_is_symmetric():
    X = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [2.0, 4.0, 1.0]]
    X_centered, _ = mean_center(X)
    C = covariance_matrix(X_centered)
    d = len(C)
    for i in range(d):
        for j in range(d):
            assert math.isclose(C[i][j], C[j][i], abs_tol=1e-12), (
                f"C[{i}][{j}] != C[{j}][{i}]"
            )


def test_covariance_matrix_matches_numpy():
    X = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]
    X_centered, _ = mean_center(X)
    C = covariance_matrix(X_centered)
    expected = np.cov(np.array(X).T)
    assert np.allclose(np.array(C), expected, atol=1e-10)


# ── fit / transform 검증 ─────────────────────────────────────────────────────

def test_fit_explained_variance_ratio_sums_to_one():
    # 전체 주성분을 사용하면 분산 설명 비율의 합이 1이어야 함
    X = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 1.0], [2.0, 3.0, 9.0]]
    pca_model = fit(X, number_of_components=3)
    total_ratio = sum(pca_model["explained_variance_ratio"])
    assert math.isclose(total_ratio, 1.0, abs_tol=1e-10)


def test_fit_explained_variance_descending():
    # 분산 설명 비율이 내림차순이어야 함
    X = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 1.0], [2.0, 3.0, 9.0]]
    pca_model = fit(X, number_of_components=3)
    ratios = pca_model["explained_variance_ratio"]
    for i in range(len(ratios) - 1):
        assert ratios[i] >= ratios[i + 1]


def test_transform_shape():
    X = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 1.0], [2.0, 3.0, 9.0]]
    X_reduced, _ = fit_transform(X, number_of_components=2)
    assert len(X_reduced) == 4       # n
    assert len(X_reduced[0]) == 2    # k


def test_fit_transform_matches_sklearn():
    # sklearn.decomposition.PCA와 투영 결과 비교
    X = [[1.0, 2.0, 3.0],
         [4.0, 5.0, 6.0],
         [7.0, 8.0, 1.0],
         [2.0, 3.0, 9.0],
         [5.0, 1.0, 4.0]]

    X_reduced, _ = fit_transform(X, number_of_components=2)

    sklearn_pca = SklearnPCA(n_components=2)
    expected = sklearn_pca.fit_transform(np.array(X))

    assert sign_corrected_allclose(X_reduced, expected)


def test_transform_on_new_data():
    # fit으로 학습한 모델을 새로운 데이터에 transform 단독 적용
    # 훈련 데이터와 테스트 데이터의 투영 결과가 동일한 주성분 방향을 사용해야 함
    X_train = [[1.0, 2.0, 3.0],
               [4.0, 5.0, 6.0],
               [7.0, 8.0, 1.0],
               [2.0, 3.0, 9.0],
               [5.0, 1.0, 4.0]]
    X_test  = [[2.0, 3.0, 4.0],
               [6.0, 7.0, 2.0]]

    pca_model = fit(X_train, number_of_components=2)
    X_test_reduced = transform(X_test, pca_model)

    # shape 검증: 테스트 샘플 수 × number_of_components
    assert len(X_test_reduced) == 2
    assert len(X_test_reduced[0]) == 2

    # sklearn과 비교: 동일한 훈련 데이터로 fit 후 테스트 데이터에 transform 적용
    sklearn_pca = SklearnPCA(n_components=2)
    sklearn_pca.fit(np.array(X_train))
    expected = sklearn_pca.transform(np.array(X_test))

    assert sign_corrected_allclose(X_test_reduced, expected)


def test_number_of_components_exceeds_features_raises():
    X = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    with pytest.raises(AssertionError):
        fit(X, number_of_components=3)


if __name__ == "__main__":
    test_mean_center_removes_mean()
    test_mean_vector_values()
    test_covariance_matrix_is_symmetric()
    test_covariance_matrix_matches_numpy()
    test_fit_explained_variance_ratio_sums_to_one()
    test_fit_explained_variance_descending()
    test_transform_shape()
    test_fit_transform_matches_sklearn()
    test_number_of_components_exceeds_features_raises()
    print("모든 테스트 통과")
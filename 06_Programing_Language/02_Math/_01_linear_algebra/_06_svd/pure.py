"""
6. SVD(특이값 분해, Singular Value Decomposition) - NumPy 구현 및 저랭크 근사 실습

직접 구현 생략 이유:
    수치적 SVD 구현(Golub-Reinsch 알고리즘)은 Householder 변환,
    이중 대각화(bidiagonalization), QR 반복(QR iteration)을 조합해야 하며
    수치 안정성 확보가 매우 까다로움. 원리 이해 후 numpy.linalg.svd 활용.

검증 항목:
    1. A = U·Σ·Vᵀ 재구성 검증
    2. U, V의 정규직교성(orthonormality) 검증
    3. 특이값과 AᵀA 고유값의 관계 검증
    4. 저랭크 근사(low-rank approximation) 오차 검증 (Eckart-Young 정리)
"""

import numpy as np


def svd_decompose(A: np.ndarray) -> tuple:
    """SVD 분해: A = U·Σ·Vᵀ

    Args:
        A: 임의 행렬, shape = m×n

    Returns:
        (U, singular_values, Vt) 튜플
            U               : 좌 특이 벡터 행렬, shape = m×m
            singular_values : 특이값 벡터(내림차순), shape = min(m,n)
            Vt              : 우 특이 벡터 행렬의 전치, shape = n×n
    """
    U, singular_values, Vt = np.linalg.svd(A, full_matrices=True)
    return U, singular_values, Vt


def low_rank_approximation(
    A: np.ndarray,
    rank: int,
) -> np.ndarray:
    """저랭크 근사(low-rank approximation): Aₖ = Σᵢ₌₁ᵏ σᵢ·uᵢ·vᵢᵀ

    Eckart-Young 정리: 랭크-k 행렬 중 A에 가장 가까운 근사.

    Args:
        A   : 원본 행렬, shape = m×n
        rank: 사용할 특이값 개수 k

    Returns:
        랭크-k 근사 행렬 Aₖ, shape = m×n
    """
    U, singular_values, Vt = np.linalg.svd(A, full_matrices=True)
    m, n = A.shape

    # Σ 행렬 구성 (m×n)
    Sigma = np.zeros((m, n))
    for i in range(min(m, n)):
        Sigma[i, i] = singular_values[i]

    # 상위 rank개만 유지, 나머지는 0으로 설정
    Sigma_rank = np.zeros_like(Sigma)
    for i in range(rank):
        Sigma_rank[i, i] = singular_values[i]

    return U @ Sigma_rank @ Vt


def frobenius_norm(A: np.ndarray) -> float:
    """프로베니우스 노름(Frobenius norm): ‖A‖_F = √(Σᵢⱼ Aᵢⱼ²)"""
    return float(np.sqrt(np.sum(A ** 2)))


if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)

    A = np.array([
        [3, 1, 1],
        [1, 3, 1],
        [1, 1, 3],
        [1, 1, 1],
    ], dtype=float)   # 4×3 비정방 행렬

    print("=" * 60)
    print("1. SVD 분해: A = U·Σ·Vᵀ")
    print("=" * 60)
    U, singular_values, Vt = svd_decompose(A)
    print(f"A shape   : {A.shape}")
    print(f"U shape   : {U.shape}")
    print(f"Σ (특이값): {singular_values}")
    print(f"Vt shape  : {Vt.shape}")

    print("\n2. 재구성 검증: U·Σ·Vᵀ ≈ A")
    m, n = A.shape
    Sigma = np.zeros((m, n))
    for i in range(min(m, n)):
        Sigma[i, i] = singular_values[i]
    A_reconstructed = U @ Sigma @ Vt
    print(f"재구성 오차(Frobenius norm): {frobenius_norm(A - A_reconstructed):.2e}")

    print("\n3. 정규직교성(orthonormality) 검증: UᵀU = I, VᵀV = I")
    print(f"UᵀU - I 최대 오차: {np.max(np.abs(U.T @ U - np.eye(m))):.2e}")
    V = Vt.T
    print(f"VᵀV - I 최대 오차: {np.max(np.abs(V.T @ V - np.eye(n))):.2e}")

    print("\n4. 특이값과 AᵀA 고유값의 관계: σᵢ = √λᵢ(AᵀA)")
    AtA_eigenvalues = np.sort(np.linalg.eigvalsh(A.T @ A))[::-1]
    sigma_squared = singular_values ** 2
    print(f"σᵢ²          : {sigma_squared}")
    print(f"λᵢ(AᵀA)     : {AtA_eigenvalues}")
    print(f"최대 오차    : {np.max(np.abs(sigma_squared - AtA_eigenvalues)):.2e}")

    print("\n5. 저랭크 근사(low-rank approximation) — Eckart-Young 정리 검증")
    original_norm = frobenius_norm(A)
    for k in range(1, min(m, n) + 1):
        A_k = low_rank_approximation(A, k)
        error = frobenius_norm(A - A_k)
        # 이론적 오차: √(σₖ₊₁² + ... + σᵣ²)
        theoretical_error = float(np.sqrt(np.sum(singular_values[k:] ** 2)))
        print(f"  rank={k}: 근사 오차={error:.4f}, 이론값={theoretical_error:.4f}, "
              f"정보 보존율={100*(1 - error/original_norm):.1f}%")
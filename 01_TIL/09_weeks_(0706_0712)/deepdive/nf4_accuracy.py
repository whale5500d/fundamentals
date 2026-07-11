"""
4장. NF4가 균등 격자(INT4) 대비 정확도 손실을 줄이는 원리 — 소스 코드 레벨 검증

1) 균등 INT4의 16개 레벨을 [-1, 1]에 균등 배치
2) NF4의 16개 레벨을 QLoRA 논문 Appendix E 값으로 하드코딩 (ground truth)
3) 정규분포(N(0,1))에서 뽑은 가중치 샘플을 각각 양자화 -> 복원 -> 오차(MSE) 비교
"""
import numpy as np

# QLoRA 논문 Appendix E, bitsandbytes 실제 quant_state에서도 동일하게 확인된 값
NF4_LEVELS = np.array([
    -1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453,
    -0.28444138169288635, -0.18477343022823334, -0.09105003625154495, 0.0,
    0.07958029955625534, 0.16093020141124725, 0.24611230194568634,
    0.33791524171829224, 0.44070982933044434, 0.5626170039176941,
    0.7229568362236023, 1.0
])


def uniform_int4_levels() -> np.ndarray:
    """균등 INT4: [-1, 1]을 16개 값으로 균등 분할."""
    return np.linspace(-1.0, 1.0, 16)


def quantize_to_levels(x: np.ndarray, levels: np.ndarray) -> np.ndarray:
    """x의 각 원소를 가장 가까운 level로 반올림(round-to-nearest)."""
    idx = np.abs(x[:, None] - levels[None, :]).argmin(axis=1)
    return levels[idx]


def normalize_to_unit_range(x: np.ndarray) -> tuple[np.ndarray, float]:
    """block(여기서는 샘플 전체)의 absmax로 나눠 [-1, 1] 범위로 정규화."""
    absmax = np.abs(x).max()
    return x / absmax, absmax


def quantization_mse(x: np.ndarray, levels: np.ndarray) -> float:
    """
    x(원본, 임의 스케일)를 absmax로 정규화 -> levels로 양자화 -> 다시 원래 스케일로 복원
    -> 원본과의 Mean Squared Error 계산.
    """
    x_norm, absmax = normalize_to_unit_range(x)
    quantized_norm = quantize_to_levels(x_norm, levels)
    reconstructed = quantized_norm * absmax
    return float(np.mean((x - reconstructed) ** 2))


def approximate_nf4_via_quantile(alpha: float = 0.9677083) -> np.ndarray:
    """
    논문이 서술한 절차(비대칭 분위수 기반)를 재현한 근사치.
    음수 7개 + 0 + 양수 8개 = 16개, alpha=0.9677083은 논문이 제시한 상수.
    (정확히 일치하지는 않는다는 게 커뮤니티에서 이미 확인된 사실 — 근사 재현이 목적)
    """
    from scipy.stats import norm
    Q = norm.ppf
    Z = Q(alpha)
    delta1 = (alpha - 0.5) / 7
    delta2 = (alpha - 0.5) / 8
    q = [0.0] * 16
    for i in range(7):
        q[i] = -Q(alpha - i * delta1) / Z
    q[7] = 0.0
    for i in range(8):
        q[i + 8] = Q(0.5 + (i + 1) * delta2) / Z
    return np.array(q)
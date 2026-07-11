import numpy as np
from nf4_accuracy import (
    NF4_LEVELS,
    uniform_int4_levels,
    quantize_to_levels,
    quantization_mse,
    approximate_nf4_via_quantile,
)


def test_nf4_levels_count_and_symmetry():
    """NF4는 16개 값, 정확히 하나(인덱스 7)가 0이어야 한다."""
    assert len(NF4_LEVELS) == 16
    assert NF4_LEVELS[7] == 0.0
    assert NF4_LEVELS.min() == -1.0
    assert NF4_LEVELS.max() == 1.0


def test_uniform_int4_is_evenly_spaced():
    """균등 INT4는 인접 레벨 간 간격이 모두 동일해야 한다."""
    levels = uniform_int4_levels()
    diffs = np.diff(levels)
    assert np.allclose(diffs, diffs[0]), "균등 격자는 간격이 일정해야 함"
    assert np.isclose(diffs[0], 2.0 / 15)


def test_nf4_is_denser_near_zero_than_uniform_int4():
    """
    NF4는 0 근처(인덱스 6~9 부근)의 레벨 간격이 균등 INT4보다 좁고,
    꼬리(양 끝) 쪽 간격은 더 넓어야 한다.
    """
    uniform = uniform_int4_levels()
    nf4_near_zero_gap = NF4_LEVELS[8] - NF4_LEVELS[7]   # 0 바로 위 레벨까지 간격
    uniform_near_zero_gap = uniform[8] - uniform[7]
    nf4_tail_gap = NF4_LEVELS[15] - NF4_LEVELS[14]      # 맨 끝 레벨 간격
    uniform_tail_gap = uniform[15] - uniform[14]

    assert nf4_near_zero_gap < uniform_near_zero_gap, "NF4가 0 근처에서 더 촘촘해야 함"
    assert nf4_tail_gap > uniform_tail_gap, "NF4가 꼬리에서 더 성겨야 함"
    print(f"0 근처 간격: NF4={nf4_near_zero_gap:.4f}, 균등INT4={uniform_near_zero_gap:.4f}")
    print(f"꼬리 간격: NF4={nf4_tail_gap:.4f}, 균등INT4={uniform_tail_gap:.4f}")


def test_approximate_nf4_reconstruction_close_to_official():
    """
    논문 절차(비대칭 분위수)를 재현한 근사치가 공식 NF4 값과 '대체로' 가까운지 확인.
    (커뮤니티에서도 완전히 일치하지 않는다고 보고된 사안이라, 느슨한 허용치를 둔다)
    """
    approx = approximate_nf4_via_quantile()
    max_diff = np.max(np.abs(approx - NF4_LEVELS))
    assert max_diff < 0.05, f"근사치가 공식값과 너무 다름: max_diff={max_diff}"
    print(f"근사 재현 vs 공식 NF4 최대 오차: {max_diff:.4f}")


def test_nf4_has_lower_mse_than_uniform_int4_on_gaussian_weights():
    """
    핵심 검증: 정규분포를 따르는 가중치 샘플에 대해,
    NF4로 양자화했을 때의 복원 오차(MSE)가 균등 INT4보다 작아야 한다.
    """
    rng = np.random.default_rng(42)
    weights = rng.normal(loc=0.0, scale=1.0, size=200_000)

    uniform_levels = uniform_int4_levels()
    mse_uniform = quantization_mse(weights, uniform_levels)
    mse_nf4 = quantization_mse(weights, NF4_LEVELS)

    assert mse_nf4 < mse_uniform, (
        f"NF4가 균등 INT4보다 오차가 커선 안 됨: NF4={mse_nf4}, uniform={mse_uniform}"
    )
    improvement = (1 - mse_nf4 / mse_uniform) * 100
    print(f"[Gaussian 20만개 샘플] 균등 INT4 MSE={mse_uniform:.6f}, "
          f"NF4 MSE={mse_nf4:.6f} ({improvement:.1f}% 개선)")


def test_uniform_int4_better_on_actually_uniform_data():
    """
    대조 실험: 데이터가 정규분포가 아니라 균등분포([-1,1])를 따른다면,
    오히려 균등 INT4가 NF4보다 유리해야 한다 (NF4가 항상 우월한 건 아니라는 것을 확인).
    """
    rng = np.random.default_rng(7)
    weights = rng.uniform(-1.0, 1.0, size=200_000)

    uniform_levels = uniform_int4_levels()
    mse_uniform = quantization_mse(weights, uniform_levels)
    mse_nf4 = quantization_mse(weights, NF4_LEVELS)

    assert mse_uniform < mse_nf4, "균등분포 데이터에서는 균등 격자가 유리해야 함"
    print(f"[Uniform 20만개 샘플] 균등 INT4 MSE={mse_uniform:.6f}, NF4 MSE={mse_nf4:.6f}")


if __name__ == "__main__":
    test_nf4_levels_count_and_symmetry()
    test_uniform_int4_is_evenly_spaced()
    test_nf4_is_denser_near_zero_than_uniform_int4()
    test_approximate_nf4_reconstruction_close_to_official()
    test_nf4_has_lower_mse_than_uniform_int4_on_gaussian_weights()
    test_uniform_int4_better_on_actually_uniform_data()
    print("모든 테스트 통과")
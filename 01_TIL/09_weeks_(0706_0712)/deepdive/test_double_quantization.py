from single_quantization import single_quantization_backbone_bytes
from double_quantization import (
    c1_storage_bytes_after_dq,
    c2_storage_bytes,
    double_quantization_constant_bytes,
    double_quantization_backbone_bytes,
)


def test_constant_overhead_matches_paper_0_127_bit():
    """
    QLoRA 논문 공식: 8/64 + 32/(64*256) = 0.126953125 bit/param (약 0.127)
    """
    num_params = 65_000_000_000
    result = double_quantization_constant_bytes(num_params)
    expected_bits = 8 / 64 + 32 / (64 * 256)
    assert abs(result["bits_per_param"] - expected_bits) < 1e-9
    assert abs(result["bits_per_param"] - 0.126953125) < 1e-6


def test_savings_matches_paper_0_373_bit_per_param():
    """
    Single Quantization(0.5 bit/param) -> Double Quantization(0.127 bit/param)
    절감량이 논문에서 밝힌 0.373 bit/param과 일치하는지 확인.
    """
    num_params = 65_000_000_000
    single_bits = 0.5  # 3-2에서 확인한 값
    double = double_quantization_constant_bytes(num_params)
    savings = single_bits - double["bits_per_param"]
    assert abs(savings - 0.373046875) < 1e-6
    print(f"절감량: {savings:.6f} bit/param (논문 수치: 0.37)")


def test_65b_constant_savings_matches_paper_3gb():
    """65B 모델 기준 constant 절감량이 논문이 밝힌 '약 3GB'와 일치하는지 확인."""
    num_params = 65_000_000_000
    single = single_quantization_backbone_bytes(num_params)
    double = double_quantization_backbone_bytes(num_params)

    single_constant_gb = single["constant_bytes"] if "constant_bytes" in single else None
    # single_quantization_backbone_bytes는 dict 키가 다르므로 직접 계산
    from single_quantization import quantization_constant_bytes
    single_constant_gb = quantization_constant_bytes(num_params) / 1e9
    double_constant_gb = double["constant_bytes"] / 1e9

    savings_gb = single_constant_gb - double_constant_gb
    assert abs(savings_gb - 3.0) < 0.1, f"expected ~3GB savings, got {savings_gb:.2f}GB"
    print(f"[65B] constant: {single_constant_gb:.2f}GB -> {double_constant_gb:.2f}GB "
          f"(절감 {savings_gb:.2f}GB)")


def test_c1_and_c2_breakdown():
    """c1(FP8), c2(FP32) 각각의 저장 비용이 개별적으로 맞게 계산되는지 확인."""
    num_params = 65_000_000_000
    c1 = c1_storage_bytes_after_dq(num_params)
    c2 = c2_storage_bytes(num_params)

    # c1: 65e9/64 개 * 1byte(FP8)
    expected_c1 = (num_params / 64) * 1
    assert abs(c1 - expected_c1) < 1

    # c2: (65e9/64)/256 개 * 4byte(FP32)
    expected_c2 = (num_params / 64 / 256) * 4
    assert abs(c2 - expected_c2) < 1

    print(f"c1 저장: {c1/1e9:.4f}GB, c2 저장: {c2/1e9:.4f}GB")


def test_backbone_total_65b_close_to_paper_34gb():
    """
    Double Quantization 적용 후 backbone(가중치+constant) 총량이
    QLoRA 관련 자료가 밝힌 65B 기준 약 34GB에 근접하는지 확인.
    """
    num_params = 65_000_000_000
    result = double_quantization_backbone_bytes(num_params)
    total_gb = result["total_bytes"] / 1e9
    assert 33.0 < total_gb < 34.0, f"expected ~33-34GB, got {total_gb:.2f}GB"
    print(f"[Double-Quant backbone, 65B] {total_gb:.2f}GB "
          f"(bits/param={result['bits_per_param']:.4f})")


if __name__ == "__main__":
    test_constant_overhead_matches_paper_0_127_bit()
    test_savings_matches_paper_0_373_bit_per_param()
    test_65b_constant_savings_matches_paper_3gb()
    test_c1_and_c2_breakdown()
    test_backbone_total_65b_close_to_paper_34gb()
    print("모든 테스트 통과")
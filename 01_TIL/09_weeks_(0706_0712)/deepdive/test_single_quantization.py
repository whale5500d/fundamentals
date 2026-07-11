from single_quantization import (
    nf4_weight_bytes,
    quantization_constant_bytes,
    single_quantization_backbone_bytes,
    single_quantization_total_vram,
)


def test_nf4_weight_bytes_is_half_byte_per_param():
    """NF4는 4bit = 0.5byte/param. 65B 모델이면 32.5GB."""
    num_params = 65_000_000_000
    result_gb = nf4_weight_bytes(num_params) / 1e9
    assert abs(result_gb - 32.5) < 0.01, f"expected 32.5GB, got {result_gb}GB"


def test_quantization_constant_overhead_matches_paper_0_5_bit():
    """
    block_size=64, FP32 constant일 때 파라미터당 오버헤드는 32/64 = 0.5bit.
    65B 모델 기준 약 4GB라는 QLoRA 관련 자료 수치 재현.
    """
    num_params = 65_000_000_000
    constant_bytes = quantization_constant_bytes(num_params, block_size=64, constant_dtype="fp32")
    bits_per_param = constant_bytes * 8 / num_params
    assert abs(bits_per_param - 0.5) < 1e-9, f"expected 0.5 bit/param, got {bits_per_param}"

    result_gb = constant_bytes / 1e9
    assert abs(result_gb - 4.0625) < 0.01, f"expected ~4GB, got {result_gb}GB"


def test_backbone_total_bits_per_param_is_4_5():
    """NF4(4bit) + constant overhead(0.5bit) = 4.5bit/param이어야 한다."""
    num_params = 65_000_000_000
    result = single_quantization_backbone_bytes(num_params)
    assert abs(result["bits_per_param"] - 4.5) < 1e-9


def test_65b_backbone_total_matches_expected_36_5gb():
    """
    65B 모델의 backbone(가중치+constant) 총량이 약 36.56GB인지 확인.
    (32.5GB 가중치 + 4.06GB constant)
    """
    num_params = 65_000_000_000
    result = single_quantization_backbone_bytes(num_params)
    total_gb = result["total_bytes"] / 1e9
    assert abs(total_gb - 36.5625) < 0.01, f"expected ~36.56GB, got {total_gb}GB"


def test_no_quant_vs_single_quant_reduction_ratio():
    """
    3-1(No Quantization) 대비 3-2(Single Quantization)의 backbone 감소율 확인.
    130GB -> 36.56GB, 약 71.9% 감소해야 한다.
    """
    num_params = 65_000_000_000
    no_quant_gb = 130.0  # 3-1에서 검증한 값
    single_quant = single_quantization_backbone_bytes(num_params)
    single_quant_gb = single_quant["total_bytes"] / 1e9

    reduction_ratio = 1 - (single_quant_gb / no_quant_gb)
    assert 0.70 < reduction_ratio < 0.73, f"expected ~71.9% reduction, got {reduction_ratio*100:.1f}%"
    print(f"[No-Quant -> Single-Quant, 65B] {no_quant_gb}GB -> {single_quant_gb:.2f}GB "
          f"({reduction_ratio*100:.1f}% 감소)")


def test_total_vram_with_qlora_style_adapter():
    """
    QLoRA 실제 설정(r=64, 모든 linear layer)을 적용한 전체 VRAM 계산.
    Double Quantization 적용 전이므로 3-3보다는 큰 값이 나와야 한다.
    """
    num_params = 65_000_000_000
    hidden = 8192
    ffn_hidden = 22016
    layers = 80
    layer_dims = (
        [(hidden, hidden)] * 4 * layers
        + [(ffn_hidden, hidden), (hidden, ffn_hidden), (ffn_hidden, hidden)] * layers
    )
    result = single_quantization_total_vram(num_params, layer_dims, rank=64)
    print(f"[Single-Quant, QLoRA adapter, 65B] backbone={result['backbone_total_GB']:.2f}GB "
          f"(weight={result['backbone_weight_GB']:.2f}GB + constant={result['backbone_constant_GB']:.2f}GB), "
          f"adapter={result['adapter_mem_GB']:.2f}GB, total={result['total_GB']:.2f}GB")
    # Double Quantization을 적용하면 constant가 줄어들 것이므로, 이 total은 3-3보다 커야 한다
    assert result["total_GB"] > 40.0


if __name__ == "__main__":
    test_nf4_weight_bytes_is_half_byte_per_param()
    test_quantization_constant_overhead_matches_paper_0_5_bit()
    test_backbone_total_bits_per_param_is_4_5()
    test_65b_backbone_total_matches_expected_36_5gb()
    test_no_quant_vs_single_quant_reduction_ratio()
    test_total_vram_with_qlora_style_adapter()
    print("모든 테스트 통과")
from no_quantization import (
    base_weight_bytes,
    adapter_param_count,
    adapter_training_bytes,
    no_quantization_total_vram,
)


def test_base_weight_65b_matches_paper_130gb():
    """
    65B 모델을 FP16으로 그대로 올리면 130GB가 필요하다는
    QLoRA 관련 자료의 수치(65e9 * 2byte = 130GB)를 재현하는지 확인.
    """
    num_params = 65_000_000_000
    result_gb = base_weight_bytes(num_params, "fp16") / 1e9
    assert abs(result_gb - 130.0) < 0.1, f"expected ~130GB, got {result_gb}GB"


def test_adapter_param_count_matches_lora_formula():
    """
    ΔW = B @ A, A:(r, d_in), B:(d_out, r)
    layer 하나(d_out=4096, d_in=4096), rank=64일 때
    파라미터 수 = r*d_in + d_out*r = 64*4096*2 = 524288
    """
    layer_dims = [(4096, 4096)]
    rank = 64
    result = adapter_param_count(layer_dims, rank)
    expected = rank * 4096 + 4096 * rank
    assert result == expected == 524_288


def test_adapter_training_bytes_breakdown():
    """
    adapter_training_bytes() 자체를 직접 검증한다.
    파라미터 1000개, bf16(2byte) 기준:
    - param_bytes = 1000 * 2 = 2000
    - grad_bytes = 1000 * 2 = 2000  (param과 동일 precision 가정)
    - optimizer_bytes = 1000 * 4 * 2 = 8000  (Adam: FP32 momentum + variance)
    - total = 12000
    """
    result = adapter_training_bytes(adapter_params=1000, adapter_precision="bf16")
    assert result["param_bytes"] == 2000
    assert result["grad_bytes"] == 2000
    assert result["optimizer_bytes"] == 8000
    assert result["total_bytes"] == 12000


def test_adapter_training_bytes_fp32_precision():
    """adapter를 fp32로 저장하는 경우도 공식이 맞게 스케일되는지 확인."""
    result = adapter_training_bytes(adapter_params=1000, adapter_precision="fp32")
    assert result["param_bytes"] == 4000
    assert result["grad_bytes"] == 4000
    assert result["optimizer_bytes"] == 8000  # optimizer state는 precision 인자와 무관, 항상 FP32
    assert result["total_bytes"] == 16000


def test_original_lora_adapter_memory_is_negligible():
    """
    LoRA의 핵심 주장: 학습 파라미터(A,B) 메모리는 base weight 대비 무시할 수준이어야 한다.
    단, 이건 '원본 LoRA' 설정(Q, V projection에만, 작은 rank)일 때 성립하는 주장이다.
    LLaMA-65B 근사 구조 + 원본 LoRA 기본 설정(r=8, Query/Value만)으로 검증.
    """
    num_params = 65_000_000_000
    hidden = 8192
    layers = 80
    # 원본 LoRA: attention의 Q, V projection에만 적용 (K, O, FFN은 미적용)
    layer_dims = [(hidden, hidden)] * 2 * layers  # q, v projection만
    result = no_quantization_total_vram(num_params, layer_dims, rank=8)

    ratio = result["adapter_mem_GB"] / result["base_weight_GB"]
    assert ratio < 0.01, f"adapter memory ratio too high: {ratio:.4f}"
    print(f"[원본 LoRA, 65B] base={result['base_weight_GB']:.1f}GB, "
          f"adapter={result['adapter_mem_GB']:.4f}GB, "
          f"total={result['total_GB']:.1f}GB, ratio={ratio*100:.3f}%")


def test_qlora_style_adapter_is_no_longer_negligible():
    """
    대조군: QLoRA가 채택한 설정(r=64, 모든 linear layer)을 원본 LoRA와 동일한 No-Quantization
    조건에 대입하면 adapter 비율이 더 이상 무시할 수준이 아님을 확인.
    (QLoRA는 이 대신 base weight를 4bit로 낮춰서 총량을 줄이는 전략을 택한다 — 4장에서 다룰 내용)
    """
    num_params = 65_000_000_000
    hidden = 8192
    ffn_hidden = 22016
    layers = 80
    layer_dims = (
        [(hidden, hidden)] * 4 * layers
        + [(ffn_hidden, hidden), (hidden, ffn_hidden), (ffn_hidden, hidden)] * layers
    )
    result = no_quantization_total_vram(num_params, layer_dims, rank=64)
    ratio = result["adapter_mem_GB"] / result["base_weight_GB"]

    assert ratio > 0.05, f"expected non-negligible ratio, got {ratio:.4f}"
    print(f"[QLoRA 설정, 65B, No-Quant 상태] adapter 비율={ratio*100:.2f}% "
          f"(원본 LoRA 대비 rank 8x, 적용 layer 3.5x)")


def test_7b_model_base_weight():
    """7B 모델 기준 FP16 base weight가 약 14GB인지 확인 (7e9 * 2byte)."""
    num_params = 7_000_000_000
    result_gb = base_weight_bytes(num_params, "fp16") / 1e9
    assert abs(result_gb - 14.0) < 0.1


if __name__ == "__main__":
    test_base_weight_65b_matches_paper_130gb()
    test_adapter_param_count_matches_lora_formula()
    test_adapter_training_bytes_breakdown()
    test_adapter_training_bytes_fp32_precision()
    test_original_lora_adapter_memory_is_negligible()
    test_qlora_style_adapter_is_no_longer_negligible()
    test_7b_model_base_weight()
    print("모든 테스트 통과")
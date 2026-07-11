"""
3-1. No Quantization (원본 LoRA) VRAM 계산기

가정:
- base model: 원래 정밀도(기본 FP16=2byte)로 고정, gradient/optimizer state 없음
- adapter: 지정한 linear layer들에 rank r의 LoRA(A, B) 적용
- optimizer: Adam 계열 (파라미터당 momentum + variance = FP32 2개 = 8byte)
"""

BYTES = {
    "fp32": 4,
    "fp16": 2,
    "bf16": 2,
}


def base_weight_bytes(num_params: int, precision: str = "fp16") -> int:
    """Base model 가중치가 차지하는 바이트 수. Frozen이므로 이게 전부다."""
    return num_params * BYTES[precision]


def adapter_param_count(layer_dims: list[tuple[int, int]], rank: int) -> int:
    """
    layer_dims: [(d_out, d_in), ...] LoRA를 적용할 각 linear layer의 (출력, 입력) 차원
    각 layer마다 A: (r, d_in), B: (d_out, r) 두 행렬이 추가된다.
    """
    total = 0
    for d_out, d_in in layer_dims:
        total += rank * d_in  # A
        total += d_out * rank  # B
    return total


def adapter_training_bytes(adapter_params: int, adapter_precision: str = "bf16") -> dict:
    """
    학습 가능한 A, B에 대해서만 필요한 메모리:
    - 파라미터 저장(bf16)
    - gradient 저장(보통 파라미터와 동일 precision)
    - Adam optimizer state (momentum, variance, 보통 FP32 유지)
    """
    param_bytes = adapter_params * BYTES[adapter_precision]
    grad_bytes = adapter_params * BYTES[adapter_precision]
    optimizer_bytes = adapter_params * BYTES["fp32"] * 2  # momentum + variance
    return {
        "param_bytes": param_bytes,
        "grad_bytes": grad_bytes,
        "optimizer_bytes": optimizer_bytes,
        "total_bytes": param_bytes + grad_bytes + optimizer_bytes,
    }


def no_quantization_total_vram(num_params: int, layer_dims: list[tuple[int, int]], rank: int) -> dict:
    base = base_weight_bytes(num_params, "fp16")
    adapter_params = adapter_param_count(layer_dims, rank)
    adapter_mem = adapter_training_bytes(adapter_params)
    total = base + adapter_mem["total_bytes"]
    return {
        "base_weight_GB": base / 1e9,
        "adapter_params": adapter_params,
        "adapter_mem_GB": adapter_mem["total_bytes"] / 1e9,
        "total_GB": total / 1e9,
    }
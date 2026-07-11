"""
3-2. Single Quantization (NF4 적용) VRAM 계산기

가정:
- base model 가중치: NF4(4bit)로 저장
- block_size(기본 64)개 가중치마다 quantization constant(scale factor) 1개, FP32(32bit)로 저장
- adapter(A, B)는 이전 단계와 동일하게 bf16으로 유지 (양자화 대상 아님)
"""
from no_quantization import BYTES, adapter_param_count, adapter_training_bytes

NF4_BITS = 4


def nf4_weight_bytes(num_params: int) -> float:
    """NF4로 저장된 가중치 자체의 바이트 수. 4bit = 0.5byte/param."""
    return num_params * NF4_BITS / 8


def quantization_constant_bytes(num_params: int, block_size: int = 64,
                                 constant_dtype: str = "fp32") -> float:
    """
    block_size개 파라미터마다 constant 1개가 필요.
    constant 1개 크기 = constant_dtype 바이트 수.
    파라미터당 오버헤드 = constant_bytes / block_size
    """
    constant_bytes = BYTES[constant_dtype]
    num_blocks = num_params / block_size
    return num_blocks * constant_bytes


def single_quantization_backbone_bytes(num_params: int, block_size: int = 64,
                                        constant_dtype: str = "fp32") -> dict:
    weight_bytes = nf4_weight_bytes(num_params)
    constant_bytes = quantization_constant_bytes(num_params, block_size, constant_dtype)
    return {
        "weight_bytes": weight_bytes,
        "constant_bytes": constant_bytes,
        "total_bytes": weight_bytes + constant_bytes,
        "bits_per_param": (weight_bytes + constant_bytes) * 8 / num_params,
    }


def single_quantization_total_vram(num_params: int, layer_dims: list[tuple[int, int]],
                                    rank: int, block_size: int = 64) -> dict:
    backbone = single_quantization_backbone_bytes(num_params, block_size)
    adapter_params = adapter_param_count(layer_dims, rank)
    adapter_mem = adapter_training_bytes(adapter_params)
    total = backbone["total_bytes"] + adapter_mem["total_bytes"]
    return {
        "backbone_weight_GB": backbone["weight_bytes"] / 1e9,
        "backbone_constant_GB": backbone["constant_bytes"] / 1e9,
        "backbone_total_GB": backbone["total_bytes"] / 1e9,
        "bits_per_param": backbone["bits_per_param"],
        "adapter_mem_GB": adapter_mem["total_bytes"] / 1e9,
        "total_GB": total / 1e9,
    }
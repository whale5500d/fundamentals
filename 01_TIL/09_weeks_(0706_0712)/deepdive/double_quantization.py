"""
3-3. Double Quantization VRAM 계산기

가정:
- 1단계 constant(c1): block_size1(기본 64)개 파라미터마다 1개, 원래 FP32였음
- Double Quantization 적용: c1을 다시 양자화
    - c1 값 자체 -> FP8(8bit)로 저장 (block_size1 파라미터당 1개)
    - c1을 복원하기 위한 2단계 constant(c2) -> FP32(32bit), block_size2(기본 256)개의 c1마다 1개
"""
from no_quantization import BYTES
from single_quantization import nf4_weight_bytes


def c1_storage_bytes_after_dq(num_params: int, block_size1: int = 64,
                               c1_dtype: str = "fp8") -> float:
    """c1 값 자체를 c1_dtype(기본 FP8)으로 저장하는 총 바이트."""
    if c1_dtype not in BYTES:
        BYTES["fp8"] = 1  # 8bit = 1byte, 최초 1회만 등록
    num_c1 = num_params / block_size1
    return num_c1 * BYTES[c1_dtype]


def c2_storage_bytes(num_params: int, block_size1: int = 64, block_size2: int = 256,
                      c2_dtype: str = "fp32") -> float:
    """c1들을 다시 묶어 만든 c2를 c2_dtype(기본 FP32)으로 저장하는 총 바이트."""
    num_c1 = num_params / block_size1
    num_c2 = num_c1 / block_size2
    return num_c2 * BYTES[c2_dtype]


def double_quantization_constant_bytes(num_params: int, block_size1: int = 64,
                                        block_size2: int = 256) -> dict:
    c1_bytes = c1_storage_bytes_after_dq(num_params, block_size1)
    c2_bytes = c2_storage_bytes(num_params, block_size1, block_size2)
    total = c1_bytes + c2_bytes
    return {
        "c1_bytes": c1_bytes,
        "c2_bytes": c2_bytes,
        "total_bytes": total,
        "bits_per_param": total * 8 / num_params,
    }


def double_quantization_backbone_bytes(num_params: int, block_size1: int = 64,
                                        block_size2: int = 256) -> dict:
    weight_bytes = nf4_weight_bytes(num_params)  # NF4 가중치 자체는 변화 없음
    constant = double_quantization_constant_bytes(num_params, block_size1, block_size2)
    total = weight_bytes + constant["total_bytes"]
    return {
        "weight_bytes": weight_bytes,
        "constant_bytes": constant["total_bytes"],
        "total_bytes": total,
        "bits_per_param": total * 8 / num_params,
    }
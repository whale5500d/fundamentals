import math
import numpy as np
import pytest

from _01_linear_algebra._01_vector.pure import vector_add, scalar_multiply, dot_product, norm

def test_vector_add():
    a, b = [1, 2, 3], [4, 5, 6]
    expected = (np.array(a) + np.array(b)).tolist()
    result = vector_add(a, b)
    assert result == expected, f"불일치: {result} != {expected}"

def test_vector_add_dimension_mismatch():
    # 차원(dimension)이 다른 벡터를 더하면 AssertionError가 발생해야 함
    with pytest.raises(AssertionError):
        vector_add([1, 2], [1, 2, 3])

def test_scalar_multiply():
    c, a = 3, [1, 2, 3]
    expected = (c * np.array(a)).tolist()
    result = scalar_multiply(c, a)
    assert result == expected, f"불일치: {result} != {expected}"

def test_dot_product():
    a, b = [1, 2, 3], [4, 5, 6]
    expected = float(np.dot(a, b))
    result = dot_product(a, b)
    assert math.isclose(result, expected), f"불일치: {result} != {expected}"

def test_norm():
    a = [3, 4]  # 3-4-5 직각삼각형 -> norm = 5
    expected = float(np.linalg.norm(a))
    result = norm(a)
    assert math.isclose(result, expected), f"불일치: {result} != {expected}"
    assert math.isclose(result, 5.0)

def test_norm_relation_to_dot_product():
    # norm은 내적(dot product)으로부터 정의됨: ||a|| = sqrt(a · a)
    a = [1, 2, 3, 4]
    assert math.isclose(norm(a), math.sqrt(dot_product(a, a)))

test_vector_add()
test_vector_add_dimension_mismatch()
test_scalar_multiply()
test_dot_product()
test_norm()
test_norm_relation_to_dot_product()
print("모든 테스트 통과")

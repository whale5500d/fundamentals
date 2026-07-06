import math

def vector_add(a: list, b: list) -> list:
    assert len(a) == len(b), "The dimensions of the two vectors must match"
    
    # 기초 방법
    # result = []
    # for i in range((len(a))):
    #     result.append(a[i] + b[i])
    # return result

    # 컴프리헨션
    return [a[i] + b[i] for i in range(len(a))]

def scalar_multiply(c: float, a: list) -> list:
    # 기초 방법
    # result = []
    # for i in range(len(a)):
    #     result.append(c * a[i])
    # return result

    # 컴프리헨션
    return [c*a[i] for i in range(len(a))]

def dot_product(a: list, b: list) -> float:
    assert len(a) == len(b), "The dimension of the two vectors must match"
    
    # 기초 방법
    # result = 0
    # for i in range(len(a)):
    #     result += a[i] * b[i]
    # return result

    # 컴프리헨션
    return sum(a[i] * b[i] for i in range(len(a)))

def norm(a: list) -> float:
    # 기초 방법
    # result = 0
    # for i in range(len(a)):
    #     result += a[i] * a[i]
    # return math.sqrt(result)

    # 간단한 방법
    return math.sqrt(dot_product(a, a))
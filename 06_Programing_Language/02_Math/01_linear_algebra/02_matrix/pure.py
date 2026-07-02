def shape(A: list) -> tuple:
    """행렬의 (행 개수 m, 열 개수 n) 반환"""
    m = len(A)
    n = len(A[0])
    return m, n

def matrix_add(A: list, B: list) -> list:
    """행렬의 덧셈"""
    m_A, n_A = shape(A)
    m_B, n_B = shape(B)
    assert (m_A, n_A) == (m_B, n_B), f"shape 불일치: {(m_A, n_A)} != {(m_B, n_B)}"

    return [
        [A[i][j] + B[i][j] for j in range(n_A)]
        for i in range(m_A)
    ]

def transpose(A: list) -> list:
    """
        전치(transpose): (A^T)_{ij} = A_{ji}
        m*n 행렬을 n*m 행렬로 전치
    """
    m, n = shape(A)
    return [
        [A[j][i] for i in range(m)]
        for j in range(n)
    ]

def matmul(A: list, C: list) -> list:
    """
        행렬곱(matrix multiplication): (A·C)_{ik} = Σ_j A_{ij} × C_{jk}
        조건: A의 열 수(n) == C의 행 수(n)
        결과: m*p 행렬
        시간 복잡도: O(m * n * p)
    """
    m, n_A = shape(A)
    n_C, p = shape(C)
    assert n_A == n_C, f"shape 불일치: A의 열 수({n_A}) != C의 행 수({n_C})"

    return [
        [
            sum(A[i][j] * C[j][k] for j in range(n_A))
            for k in range(p)
        ]
        for i in range(m)
    ]
import copy
from _01_linear_algebra._03_linear_system_gaussian_elimination.pure import SingularMatrixError

def _identity(n: int) -> list:
    """n*n 단위 행렬(identity matrix) 생성"""
    # 기초 방법
    # result = []
    # for i in range(n):
    #     row = []
    #     for j in range(n):
    #         if i == j:
    #             row.append(1.0)
    #         else:
    #             row.append(0.0)
    #     result.append(row)
    # return result

    # 컴프리헨션
    return [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]

def inverse(A: list, tol: float = 1e-12) -> list:
    """
        Gauss-Jordan elimination으로 역행렬 계산

        Args:
            A: square matrix, shape = n*n
            tol: pivot 최소 절대값. 이 값 미만이면 singular(특이 행렬)로 간주

        Returns:
            A^{-1}
    """
    n = len(A)
    assert len(A[0]) == n, "A는 square matrix(정방 행렬)이어야 함"

    # 기초 방법
    # [A|I] 구성
    # 기초 방법
    # AI = []
    # for i in range(n):
    #     AI.append(A[i][:] + _identity(n)[i])
    # 컴프리헨션
    AI = [A[i][:] + _identity(n)[i] for i in range(n)]

    # 1. forward elimination(전방 소거) -> [U|L]
    for j in range(n):
        # partial pivoting
        max_row = max(range(j, n), key=lambda i: abs(AI[i][j]))
        AI[j], AI[max_row] = AI[max_row], AI[j]

        pivot = AI[j][j]
        if abs(pivot) < tol:
            raise SingularMatrixError(
                f"열 {j}의 피벗(pivot) 값이 {tol} 미만: A는 singular(특이 행렬)입니다."
            )
        
        for i in range(j+1, n):
            m = AI[i][j] / pivot
            for k in range(2 * n):
                AI[i][k] -= m * AI[j][k]

    # 2. backward elimination(후방 소거) -> [D|M]
    for j in range(n-1, -1, -1):
        for i in range(j-1, -1, -1):
            m = AI[i][j] / AI[j][j]
            for k in range(2*n):
                AI[i][k] -= m * AI[j][k]

    # 3. normalization -> [I|A^{-1}]
    for i in range(n):
        pivot = AI[i][i]
        for k in range(2*n):
            AI[i][k] /= pivot

    # 4. 오른쪽 절반(A^{-1}) return
    # 기초 방법
    # result = []
    # for i in range(n):
    #     sliced_row = AI[i][n:]
    #     result.append(sliced_row)
    # return result
    # 컴프리핸션
    return [AI[i][n:] for i in range(n)]

def determinant(A: list, tol: float = 1e-12) -> float:
    """
        가우스 소거법 기반 행렬식(determinant) 계산

        상삼각 행렬 U의 대각 원소 곱으로 계산:
            det(A) = (-1)^s · Π U_{ii}   (s: 행 교환 횟수)

        Args:
            A: square matrix, shape = n*n
            tol: pivot 최소 절댓값

        Returns:
            det(A) (float)
    """
    n = len(A)
    assert len(A[0]) == n, "A는 정방 행렬(square matrix)이어야 함"

    M = copy.deepcopy(A)
    sign = 1 # 행 교환 횟수에 따른 부호(sign) 추적

    for j in range(n):
        # partial pivoting
        max_row = max(range(j, n), key=lambda i: abs(M[i][j]))
        if max_row != j:
            M[j], M[max_row] = M[max_row], M[j]
            sign *= -1 # 행 교환 1회 -> 부호 반전

        if abs(M[j][j]) < tol:
            return 0.0 # singular(특이 행렬) -> det = 0
        
        for i in range(j+1, n):
            m = M[i][j] / M[j][j]
            for k in range(j, n):
                M[i][k] -= m * M[j][k]

    # 대각 원소의 곱
    det = sign * 1.0
    for i in range(n):
        det *= M[i][i]

    return det
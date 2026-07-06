"""
3. 선형 시스템(linear system) - 가우스 소거법(Gaussian elimination) 순수 Python 구현

알고리즘:
    1. 전방 소거(forward elimination): [A|b] → [U|c], 부분 피벗팅(partial pivoting) 포함
    2. 후방 대입(back substitution): [U|c] → x

시간 복잡도(time complexity): O(n³)
"""

import copy


class SingularMatrixError(Exception):
    """피벗(pivot)이 0에 가까워 역행렬이 존재하지 않는 경우 발생"""
    pass


def _augmented(A: list, b: list) -> list:
    """첨가 행렬(augmented matrix) [A|b] 생성"""
    n = len(A)
    return [A[i][:] + [b[i]] for i in range(n)]


def forward_elimination(Ab: list, tol: float = 1e-12) -> list:
    """전방 소거(forward elimination) with 부분 피벗팅(partial pivoting)

    Args:
        Ab  : 첨가 행렬 [A|b], shape = n×(n+1)
        tol : 피벗(pivot)의 최소 절댓값. 이 값 미만이면 singular(특이 행렬)로 판단

    Returns:
        상삼각 형태로 변환된 첨가 행렬 [U|c]
    """
    Ab = copy.deepcopy(Ab)
    n = len(Ab)

    for j in range(n):  # j: 현재 처리 중인 열(pivot column)

        # 부분 피벗팅: 열 j에서 절댓값이 가장 큰 행을 찾아 교환
        max_row = max(range(j, n), key=lambda i: abs(Ab[i][j]))
        Ab[j], Ab[max_row] = Ab[max_row], Ab[j]

        pivot = Ab[j][j]
        if abs(pivot) < tol:
            raise SingularMatrixError(
                f"열 {j}의 피벗(pivot) 값이 {tol} 미만: 행렬이 singular(특이)하거나 수치적으로 불안정함"
            )

        # 열 j의 피벗 아래 원소를 전부 0으로 만듦
        for i in range(j + 1, n):
            m = Ab[i][j] / pivot              # 소거 인수(elimination factor)
            for k in range(j, n + 1):
                Ab[i][k] -= m * Ab[j][k]

    return Ab


def back_substitution(Ab: list) -> list:
    """후방 대입(back substitution)

    Args:
        Ab: 전방 소거 완료된 상삼각 첨가 행렬 [U|c]

    Returns:
        해 벡터(solution vector) x, shape = n
    """
    n = len(Ab)
    x = [0.0] * n

    for i in range(n - 1, -1, -1):   # xₙ부터 역순으로
        x[i] = Ab[i][n]              # cᵢ
        for j in range(i + 1, n):
            x[i] -= Ab[i][j] * x[j]  # Σ U_{ij}·xⱼ 차감
        x[i] /= Ab[i][i]             # U_{ii}로 나눔

    return x


def solve(A: list, b: list) -> list:
    """선형 시스템 Ax = b 를 가우스 소거법으로 풀어 해 벡터 x 반환

    Args:
        A: 계수 행렬(coefficient matrix), shape = n×n
        b: 우변 벡터(right-hand side vector), shape = n

    Returns:
        해 벡터 x, shape = n
    """
    n = len(A)
    assert len(A[0]) == n, "A는 정방 행렬(square matrix)이어야 함"
    assert len(b) == n,    "b의 길이는 A의 행 수와 같아야 함"

    Ab = _augmented(A, b)
    Ab = forward_elimination(Ab)
    return back_substitution(Ab)
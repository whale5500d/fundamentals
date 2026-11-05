# 격자 경로(grid path)
# m * n 격자의 왼쪽 위 칸에서 오른쪽 아래 칸까지 오른쪽 또는 아래로만 이동할 때
# 도달하는 서로 다른 경로의 수를 구하는 유형이다.
# 앞에서 정리한 표 2의 유형 구분에서 인덱스 2개(위치)를 쓰는 2차원 격자 DP에 해당한다.
# 이 문제부터 상태가 dp[i]가 아니라 dp[row][col] 두 인덱스로 표현된다.

# 계단 오르기와의 관계
# 계단 오르기에서는 i번째 계단에 도착하는 마지막 동작이 두 가지였고 방법 수를 합산했다.
# 이 문제도 같은 구조다. (row, col) 칸에 도착하는 마지막 이동은 위 칸에서 아래로 내려오거나,
# 왼쪽 칸에서 오른쪽으로 오는 두 가지뿐이다.
# 달라지는 점은 직전 상태가 i-1, i-2가 아니라 (row-1, col), (row, col-1)이라는 것이다.

# 기초 문제
# 정수 m(행 수)과 n(열 수)이 주어질 때,
# m * n 격자의 왼쪽 위 칸(0, 0)에서 오른쪽 아래 칸(m-1, n-1)까지
# 오른쪽 또는 아래로만 이동하는 경로의 수를 반환하라.

m_value, n_value = 3, 2
output_result = 3

def solution(m: int, n: int) -> int:
    # 상태 정의: dp[row][col]은 row, col 지점의 도착지로 이동하는 경우의 수 ❌
    # 상태 정의: (0, 0)에서 (row, col)까지 도달하는 경우의 수

    # 점화식: (0, 0)에서 (row-1, col)로 이동하는 경우의 수와 (row, col-1)로 이동하는 경우의 수의 합산    

    # 초기값: 첫 번째 행과 첫 번째 열의 값이 얼마인지 직접 나열해서 확인한다.
    # 이 칸들은 직전 상태가 하나뿐이다.
    # dp = [[0] * n for _ in range(m)]
    dp = []
    for _ in range(m):
        row = [0] * n
        dp.append(row)
    
    # 반복문: 위에서 아래로, 각 행에서는 왼쪽에서 오른쪽으로 채움
    for row in range(m):
        for col in range(n):
            # 초기값: 첫 번째 행 또는 첫 번째 열은 직전 상태가 하나뿐이므로 1
            if row == 0 or col == 0:
                dp[row][col] = 1
            # 점화식: 위 칸에서 내려오는 경우 + 왼쪽 카에서 오는 경우
            else:
                dp[row][col] = dp[row-1][col] + dp[row][col-1]

    return dp[m-1][n-1]
    
    # 2차원 배열 초기화
    # dp = [[0] * n] * m 으로 만들면 안되는 이유: 모르겠음
    return -1

print(solution(m_value, n_value))
print(output_result)

m_value, n_value = 3, 7
output_result = 28
print(solution(m_value, n_value))
print(output_result)

m_value, n_value = 1, 1
output_result = 1
print(solution(m_value, n_value))
print(output_result)

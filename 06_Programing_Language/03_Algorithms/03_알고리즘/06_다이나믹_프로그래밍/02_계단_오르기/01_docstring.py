# 계단 오르기(climbing stairs)
# 꼭대기까지 계단이 N개 있고, 한 번에 1칸 또는 2칸을 오를 수 있을 때
# 꼭대기에 도달하는 서로 다른 방법의 수를 구하는 유형이다.
# 앞서 배운 피보나치와 달리 점화식이 문제에 주어져 있지 않다.
# 상태 정의를 직접 세우고 점화식을 유도하는 과정이 이 문제의 핵심이다.

# 점화식 유도하는 관점
# N번째 계단에 도착하는 마지막 동작은 두 가지뿐이다. N-1번째에서 1칸 오르거나, N-2번째에서 2칸 오른다.
# 이 두 경우는 서로 겹치지 않으므로 각 경우의 방법 수를 더하면 된다.
# 앞서 정리한 DP 핵심 조건 중 상태 정의, 점화식, 초기값을 모두 스스로 채워야 한다.

# 기초 문제 예시
# 정수 n이 주어질 때, n개의 계단을 한 번에 1칸 또는 2칸씩 올라 꼭대기에 도달하는 방법의 수를 반환하라.

input_value = 3
output_result = 3

def solution(n: int) -> int:
    # 상태 정의: dp[i]는 i번째 계단에 도달하는 방법의 수

    # 초기값 처리: n이 1 또는 2이면 dp 배열 범위를 벗어나므로 별도 반환
    dp = [0] * (n+1)
    # (dp[1], dp[2]의 값은 직접 나열해서 확인)
    if n <= 2:
        return n

    # 초기값 대입: dp[1], dp[2]
    dp[1] = 1
    dp[2] = 2

    # 반복문: 3번째 계단부터 n번째 계단까지 순회
    for stair in range(3, n+1):
        # 점화식: i번째 계단에 도착하는 마지막 동작은 두 가지
        # (i-1번째에서 1칸, i-2번째에서 2칸) -> 두 경우의 방법 수를 합산
        dp[stair] = dp[stair-1] + dp[stair-2]

    # n번째 계단의 방법 수 반환
    return dp[n]

print(solution(input_value))
print(output_result)

input_value = 5
output_result = 8

print(solution(input_value))
print(output_result)
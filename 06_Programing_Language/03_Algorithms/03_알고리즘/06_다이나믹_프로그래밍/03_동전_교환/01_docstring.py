# 동전 교환(coin change)
# 동전 단위 목록과 목표 금액이 주어질 때, 목표 금액을 만드는 최소 동전 개수를 구하는 문제
# 그리디로 풀었는 때는 큰 단위가 작은 단위의 배수 관계라는 조건이 필요했고
# [400, 300, 1], 목표 금액 600에서 201을 반환해 최적해 2를 놓쳤다.
# DP는 첫 선택을 번복해야 하는 이 경우를 모든 선택을 비교해 해결한다.

# 계단 오르기와 달라지는 지점
# 계단 오르기에서는 마지막 동작이 2가지였고 방법 수를 합산했다.
# 이 문제는 마지막에 사용하는 동전이 동전 단위 개수만큼 있고
# 합산이 아니라 최소값을 고른다.
# 앞서 정리한 유형 구분으로는 인덱스 + 금액 상태를 쓰는 배낭형 DP에 해당한다.

# 기초 문제 예시
# 정수 리스트 coins(동전 단위)와 정수 target(목표 금액)이 주어질 때,
# target을 만드는 데 필요한 최소 동전 개수를 반환하라.
# 각 동전은 무제한 사용할 수 있고
# 만들 수 없으면 -1을 반환한다.
# 동전 단위는 서로 배수 관계가 아닐 수 있다.

input_coins = [400, 300, 1]
input_target = 600
output_result = 2

def solution(coins: list[int], t: int) -> int:
    # 상태 정의: dp[t]는 t원을 만드는 데 필요한 최소 동전의 개수
    
    # 초기값 처리: dp[0] = 0, dp[1] ~ dp[t]은 무한
    dp = [float('inf')] * (t+1)
    dp[0] = 0

    # ⚠️ 반복문: 금액을 1원부터 t원까지 순회
    for amount in range(1, t+1):
        # ⚠️ 반복문: 동전 단위 순회
        for coin in coins:
            # 범위 조건: 동전이 현재 금액 이하일 때만 사용 가능
            if coin <= amount:
                # ⚠️ 점화식: 마지막에 이 동전을 썼다면, 직전 상태는 (금액 - 동전)
                # ⚠️ dp[금액]을 기존 값와 dp[금액-동전]+1 중 더 작은 값으로 갱신
                dp[amount] = min(dp[amount], dp[amount-coin]+1)

    # 반환: dp[t]가 무한대면 만들 수 없으므로 -1, 아니면 dp[t]
    if dp[t] == float('inf'):
        return -1
    else:
        return int(dp[t])


print(solution(input_coins, input_target))
print(output_result)

input_coins = [1, 5, 12]
input_target = 15
output_result = 3
print(solution(input_coins, input_target))
print(output_result)

input_coins = [2]
input_target = 3
output_result = -1
print(solution(input_coins, input_target))
print(output_result)


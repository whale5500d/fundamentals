# 동전 교환(coin change, 그리디 기능 조건 한정)
# 주어진 금액을 만들 때 사용하는 동전 개수를 최소화하는 문제
# 그리디 전략은 가장 큰 단위의 동전부터 최대한 많이 사용하고
# 남은 금액을 다음으로 큰 단위로 처리하는 것이다.

# 그리디 성립 조건
# 동전 단위가 큰 단위를 작은 단위로 나누어 떨어지는 배수 관계(예: 500, 100, 50, 10)일 때만 탐욕적 선택 속성(greedy choice property)이 보장된다.
# 배수 관계가 아니면 그리디가 최적해를 놓치며, 이 경우 DP로 접근해야 한다.
# 반례는 풀이 후 직접 만들어보는 것을 권장한다.

# 문제
# 동전 단위 목록과 목표 금액이 주어질 때
# 목표 금액을 만들기 위해 필요한 최소 동전 개수를 반환하라.
# 동전 단위는 큰 단위가 작은 단위의 배수 관계이며
# 각 동전은 무제한 사용 가능하다.

# 1. 동전 단위가 배수 관계일 때
input_list = [500, 100, 50, 10]
input_target = 1260
output_result = 6

# 2. 동전 단위가 배수 관계가 아닐 때
# input_list = [400, 300, 1]
# input_target = 600
# output_result = 2

def solution(input_list: list[int], target: int) -> int:
    # 동전 목록, 잔여 액수, 개수 초기화
    sorted_coins = sorted(input_list, reverse=True)
    rest = target
    count = 0

    # 반복문: 동전 목록 전체 순회
    for coin in sorted_coins:
        # 몫(횟수), 나머지(남은 액수) 계산
        count += rest // coin
        rest = rest % coin

    return count

print(solution(input_list, input_target))
print(output_result)

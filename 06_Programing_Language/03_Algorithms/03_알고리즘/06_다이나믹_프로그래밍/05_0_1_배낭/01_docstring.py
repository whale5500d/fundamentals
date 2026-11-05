# 0/1 배낭 (0/1 knapsack)
# 물건마다 무게와 가치가 주어지고, 배낭의 용량 안에서 물건을 고를 때 가치의 합을 최대화하는 문제다.
# 각 물건은 넣거나, 넣지 않거나 둘 중 하나만 선택할 수 있고, 한 물건을 여러 번 넣을 수 없다.

# 앞서 배운 유형과의 관계
# 정리한 그리디의 분할 가능 배낭은 물건을 쪼갤 수 있어서 가치/무게 비율 순으로 담으면 최적해가 보장됐다.
# 하지만, 0/1 배낭은 쪼갤 수 없으므로 이 전략이 통하지 않는다.
# 앞서 정리한 "그리디로 안 풀리는 문제와 짝지어 보기"에 해당된다.
# 동전 교환(DP)과도 구조가 다르다. 동전은 각 단위를 무제한 쓸 수 있었지만
# 이 문제는 각 물건을 한 번만 쓸 수 있다.

# 기초 문제
# 물건의 무게 리스트 weights, 가치 리스트 values, 배낭의 용량 capacity가 주어질 때
# 용량을 넘지 않게 물건을 골라 얻을 수 있는 가치의 최대값을 반환하라.
# 각 물건은 한 번만 고를 수 있고, weights[i]와 values[i]는 i번째 물건의 무게와 가치다.

def solution(weights, values, capacity) -> int:
    # 상태 정의: dp[i][w]는 i번째 물건의 용량이 w일 때 ??
    # 상태 정의: dp[i][w]는 앞에서부터 i개의 물건만 고려하고 배낭 용량이 w일 때 얻을 수 있는 가치의 최대값
        # i: 고려하는 물건의 범위(1~i)
        # w: 배낭의 용량
        # 값: 그 조건에서 가능한 가치의 최대값
        # 최종적으로 알고 싶은 것: dp[N][capacity] - 1~N까지 물건을 고려하고 배낭 용량이 capacity일 때 얻을 수 있는 가치의 최대값
    
    # 초기값
        # dp[0][w] = 0: 물건을 고려하지 않고 용량이 얼마든 가치는 0이다.
        # dp[i][0] = 0: 용량이 0이면 무게가 양수인 물건을 담을 수 없으므로 가치는 0이다.
    item_count = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(item_count + 1)]

    # 반복문: 물건을 1번부터 item_count번까지 순서대로 고려
    # (물건 번호는 1번부터 센다. 그래서 i번째 물건은 weights[i-1], values[i-1]이다. 이 한 칸이 off-by-one 오류가 자주 나는 지점이다.)
    for item_number in range(1, item_count+1):
        # i번째 물건은 weights[i-1], values[i-1]
        weight = weights[item_number-1]
        value = values[item_number-1]

        # 반복문: 용량을 0부터 capacity까지 순회
        # 점화식: i번째 물건에 대한 선택은 담는 경우, 담지 않는 경우 2가지이다.
        # 범위 조건: 현재 용량 w보다 크면 담을 수 없다. 이 경우 후보는 "담지 않는 경우" 하나만 남는다.
                # 무게 <= w: 두 후보를 비교한다.
                # 무게 > w: dp[i][w] = dp[i-1][w]이다.
        for current_capacity in range(capacity+1):
            # 담지 않는 경우: 이전 행의 같은 용량 값
            not_token = dp[item_number-1][current_capacity]

            # 범위 조건: 물건의 무게가 현재 용량 이하일 때만 담을 수 있음
            # 담는 경우: 이 물건의 무게만큼 용량이 줄어든 상태에서 앞의 i-1개 물건으로 얻은 최댓값에 이 물건의 가치를 더한다. dp[i-1][w-무게]+가치
            if weight <= current_capacity:
                # 담는 경우: 이전 행에서 (용량-무게)의 값 + 물건의 가치
                taken = dp[item_number-1][current_capacity-weight]+value

                # 두 후보 중 큰 값을 선택: dp[i][w] = max(담지 않는 경우, 담는 경우)
                dp[item_number][current_capacity]=max(not_token, taken)
            # 담지 않는 경우: 앞의 i-1개 물건만으로 같은 용량을 채운 결과와 같으므로 dp[i-1][w]이다.
            else:
                dp[item_number][current_capacity]=not_token

    # 사용 횟수 제한: 각 물건은 한 번만 사용한다는 조건은 '담는 경우'가 dp[i-1] 행을 참조하는 것으로 표현된다. i번째 물건을 담기 전의 상태는 i번째 물건이 아직 고려되지 않은 상태여야 하기 때문이다.

    # 같은 행인 dp[i][w-무게]를 참조하면 이미 i번째 물건을 담은 상태에서 또 담을 수 있게 되어 한 물건을 여러 번 사용하는 무제한 배낭 문제가 된다. 동전 교환(DP)이 단위당 무제한이었던 것과 같은 구조이다.

    return dp[item_count][capacity]

input_weights=[1, 3, 4, 5]
input_values=[1, 4, 5, 7]
input_capacity=7
output_result=9
print(solution(input_weights, input_values, input_capacity))
print(output_result)

input_weights=[10, 20, 30]
input_values=[60, 100, 120]
input_capacity=50
output_result=220 # 그리디의 반례
print(solution(input_weights, input_values, input_capacity))
print(output_result)

input_weights=[5]
input_values=[10]
input_capacity=3
output_result=0 # 물건이 용량보다 무거워서 담을 수 없음
print(solution(input_weights, input_values, input_capacity))
print(output_result)
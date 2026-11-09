# 최장 증가 부분 수열(LIS, Longest Increasing Subsequence)
# 수열에서 원소의 순서를 유지하며 일부를 뽑아 만든 부분 수열 중,
# 값이 순증가(strictly increasing)하는 가장 긴 것의 길이를 구하는 문제다.

# 부분 수열과 부분 배열의 구분
# 부분 수열(subsequence)은 원소를 건너뛰어 뽑아도 되고, 부분 배열(subarray)은 연속된 구간이다.
# 앞서 푼 슬라이딩 윈도우는 연속 구간을 다뤘다.
# 이 문제는 건너뛰기가 허용되므로 윈도우 방식이 적용되지 않는다.

# 앞서 배운 1차원 DP와 달라지는 지점
# 직전 상태를 참조하는 방식이 바뀐다.
# 계단 오르기는 고정된 두 칸을
# 동전 교환은 동전 종류 수만큼의 칸을 참조했다.
# 이 문제는 현재 원소보다 앞에 있고 값이 더 작은 모든 원소가 후보다.

# 기초 문제 제시
# 정수 리스트 nums가 주어질 때, 가장 긴 순증가 부분 수열의 길이를 반환하라.
# nums의 길이는 1 이상이다.

def solution(nums_list: list[int]) -> int:
    # 상태 정의: i번째 원소로 끝나는 LIS 길이
    length = len(nums_list)

    # 초기값: 모든 원소는 혼자서 길이 1인 수열이 될 수 있다.
    dp = [1] * length

    # 점화식: 두 번째 원소부터 순서대로 dp[current_index]를 계산
    for current_index in range(1, length):
        # 반복문: current_index보다 앞의 모든 원소가 후보
        for previous_index in range(current_index):
            # 조건문: 값이 더 작아야 뒤에 붙일 수 있다. (순증가)
            if nums_list[previous_index] < nums_list[current_index]:
                # 점화식: 후보들 중 가장 긴 수열 뒤에 붙임 (최댓값 선택)
                dp[current_index] = max(dp[current_index], dp[previous_index]+1)

    # 반환값: 수열이 어느 위치에서 끝나도 되므로 dp 전체의 최댓값
    return max(dp)

input_list = [3, 4, 1, 2]
output_result = 2
print(solution(input_list))
print(output_result)

input_list = [10, 9, 2, 5, 3, 7, 101, 18]
output_result = 4 # (2, 5, 7, 101 또는 2, 3, 7, 101)
print(solution(input_list))
print(output_result)

input_list = [0, 1, 0, 3, 2, 3]
output_result = 4 # (0, 1, 2, 3)
print(solution(input_list))
print(output_result)

input_list = [7, 7, 7, 7]
output_result = 1 # 순증가이므로 같은 값은 이어 붙일 수 없음
print(solution(input_list))
print(output_result)
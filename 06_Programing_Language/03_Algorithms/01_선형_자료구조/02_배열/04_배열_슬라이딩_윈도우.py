# 슬라이딩 윈도우(sliding window)
# 고정 또는 가변 크기의 구간(윈도우)을 배열 위에서 이동시키며
# 구간 내 값을 누적 계산하는 기법
# 구간이 이동할 때마다 전체를 다시 계산하지 않고,
# 빠지는 값을 빼고 들어오는 값만 더해 O(N)으로 처리한다.
# 이중 반복문으로 모든 구간을 계산하던 O(NxK) 문제를 O(N)으로 줄이는 데 사용

# 문제
# 정수 배열과 정수 K가 주어질 때, 연속된 K개 요소의 합 중 최댓값을 반환하라.

input_list = [2, 1, 5, 1, 3, 2]
input_int = 3
output_result = 9

def solution(input_list: list[int], k: int) -> int:
    # 0. edge case
    # list[int]의 int가 음수라면?

    # 1. 최대값 초기화
    window_sum = 0

    index = 0
    while index < k:
        window_sum += input_list[index]
        index += 1

    max_sum = window_sum

    # # 2. 반복문: 마지막 인덱스에서 K를 제외한 길이만큼 반복
    # # (연속된 K까지 합산하므로, 그 뒤에 값은 어짜피 계산될 거라 거기까지 반복하지 않아도 됨)
    # for i in range(len(input_list)-k-1):
    #     # 지금 계산한 값이 다음에 계산한 값보다 큰지 작은지 어떻게 알지?
    #     # 최대값 추적(running maximum): 최대값을 별도 변수(result)에 저장해두고,
    #     # 매 계산마다 그 변수와 비교해 갱신(누적 비교 변수)
        
    #     # O(NxK) 방법
    #     # # i부터 i+k-1까지 합산한다.(new_result)
    #     # # 합산 어떻게 함?
    #     # new_result = 0
    #     # # 합산한 결과가 별도 변수(result)와 큰지 비교한다.
    #     # if result < new_result:
    #     #     # 크면, result를 업데이트한다.
    #     #     result = new_result

    #     # O(N) 방법(슬라이딩 윈도우)
    #     # i(첫 번째)의 값과 i+k-1(마지막)의 값 중 누가 큰지 비교한다.
    #     # 마지막 값이 더 크다면, 현재 최대값보다 합산할 값이 커짐
    #     if input_list[i] < input_list[i+k-1]:
    #         # 커질 것이므로 업데이트
    #         result = result - input_list[i] + input_list[i+k-1]

    # 2. 반복문: 마지막 인덱스에서 k를 제외한 길이만큼 반복
    i = 1 # 초기화 합산 이후 부터 시작

    while i <= len(input_list)-k:
        # 3. 신규 합산 산출
        window_sum = window_sum - input_list[i-1] + input_list[i+k-1]

        # 4. 기존 합산과 신규 합산을 비교(신규 합산이 더 큰지 확인)
        if max_sum < window_sum:
            # 5. 신규 합산이 더 크면 재할당
            max_sum = window_sum

        i += 1

    return max_sum

print(solution(input_list, input_int))
print(output_result)
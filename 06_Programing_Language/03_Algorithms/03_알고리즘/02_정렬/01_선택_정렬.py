# 선택 정렬(selection sort)
# 배열을 순회하며 남은 범위(미정렬 구간)에서 최솟값을 찾아, 그 값을 미정렬 구간의 맨 앞과 교환(swap)하는 과정을 반복하는 정렬 방식이다.
# 시간복잡도는 O(N^2)이며, 비교 횟수는 버블 정렬과 동일하지만 교환 횟수가 최대 N번으로 훨씬 적다는 점이 차이다.
# 값이 같은 요소의 상대 순서가 바뀔 수 있어 불안정 정렬(unstable sort)에 해당한다.

# 문제
# 정수 배열이 주어질 때, 선택 정렬을 사용해 오름차순으로 정렬한 결과를 반환하라.
# 내정 정렬 함수는 사용하지 않는다.

input_list = [5, 2, 4, 1, 3]
output_result = [1, 2, 3, 4, 5]

def solution(input_list: list[int]) -> list[int]:
    # 반복문: 배열을 순서대로 순회
    for i in range(len(input_list)):
        # 남은 범위에서 최소값을 갖는 인덱스 초기화
        min_index = i
        # 반복문: 남은 범위 순회
        for j in range(i+1, len(input_list)):
            # 최소값을 갖는 인덱스 찾기
            if input_list[min_index] > input_list[j]:
                min_index = j
        # 미정렬 구간의 첫 번째 값과 교환(swap)
        input_list[i], input_list[min_index] = input_list[min_index], input_list[i]

    return input_list

print(solution(input_list))
print(output_result)
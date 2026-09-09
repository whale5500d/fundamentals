# 순회 및 탐색(traversal / linear search)
# 배열의 처음부터 끝까지 순서대로 요소에 접근하는 것이 순회
# 순회 중 특정 조건을 만족하는 요소를 찾는 것이 선형 탐색
# 정렬 여부와 부관하게 적용 가능
# 시간복잡도는 O(N)

# 정수 배열과 목표값이 주어질 때, 배열 내에서 목표값과 일치하는 첫 번째 요소의 인덱스를 반환하라.
# 존재하지 않으면 -1을 반환하라.
input_array = [4, 2, 7, 1, 9]
target = 7
output_result = 2

def solution(input_array: list[int], target: int) -> int:
    # 엣지 케이스(edge case) 1
    # 빈 배열일 경우, 반복문을 돌지 않고 -1 반환
    if len(input_array) == 0:
        return -1

    # 반복문: 배열을 순회하며 조건에 부합하는 목표값 탐색
    for index in range(len(input_array)):
        # 조건문: 목표값과 일치하는 첫 번째 값이 있는지 탐색
        if input_array[index] == target:
            # 조건 만족 시: 해당 인덱스 반환
            # 반환 처리를 통해 중복값 여부 판단을 해결
            return index

    # 반복을 종료까지 목표값을 탐색하지 못했다면, -1 반환
    return -1

import time

start = time.perf_counter()
print(solution(input_array, target))
print(output_result)
end = time.perf_counter()

print(f"실행 시간: {end - start}초") # 2.5874999999999856e-05초, 지수 표기법
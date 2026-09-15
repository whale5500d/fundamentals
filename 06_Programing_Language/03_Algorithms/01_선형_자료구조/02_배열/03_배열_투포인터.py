# 투 포인터(two pointer)
# 배열 내에서 두 개의 인덱스를 동시에 움직이며 조건을 검사하는 기법
# 한 번의 순회(O(N))로 두 지점 간의 관계를 비교할 수 있고
# 이중 반복문(O(N^2))으로 처리하던 문제를 O(N)으로 줄이는 데 주로 사용됨.

# 문제
# 오름차순으로 정렬된 정수 배열과 목표값(target)이 주어질 때,
# 두 요소의 합이 목표값과 정확히 일치하는 인덱스 쌍을 반환하라.
# 존재하지 않으면 빈 리스트를 반환하라.

input_list = [1, 2, 4, 7, 11]
input_target = 9
output_result = [1, 3]

def solution(input_list: list[int], input_target: int) -> list[int]:
    # 왼쪽 포인터 선언: 배열의 시작 인덱스
    left = 0
    
    # 오른쪽 포인터 선언: 배열의 마지막 인덱스
    right = len(input_list) - 1
    
    # 반복문: 왼쪽 포인터가 오른쪽 포인터보다 작은 동안 반복
    while left < right:
        # 두 포인터가 가리키는 값의 합 계산
        total = input_list[left] + input_list[right]

        # 조건문: 합이 목표값과 일치하는지 확인
        if total == input_target:
            # 조건 만족 시: 두 인덱스를 리스트로 반환
            return [left, right]
        # 조건문: 합이 목표값보다 작은지 확인
        elif total < input_target:
            # 조건 만족 시: 왼쪽 포인터를 오른쪽으로 이동(합을 늘리기 위함)
            left += 1
        # 그 외의 경우(합이 목표값보다 큰 경우)
        else:
            # 오른쪽 포인터를 왼쪽으로 이동(합을 줄이기 위함)
            right -= 1
    # 반복문 종료까지 찾지 못한 경우: 빈 리스트 반환
    return []

print(solution(input_list, input_target))
print(output_result)
# 회전된 배열 탐색(rotated sorted array)
# 원래 오름차순으로 정렬되어 있던 배열이 특정 지점에서 순환 이동(rotation)되어,
# 배열 전체는 정렬되어 있지 않지만 특정 지점을 기준으로 나눈 두 부분은
# 각각 정렬 상태를 유지하는 배열에서 목표값을 찾는 이진 탐색 변형
# 중간값(mid)을 기준으로 왼쪽 절반과 오른쪽 절반 중 어느 쪽이 정렬되어 있는지 먼저 판별한 뒤
# 그 정렬된 절반에 목표값이 포함되는지 확인하여 탐색 방향을 결정한다.

# 문제
# 원래 오름차순 정렬되어 있던 정수 배열이 특정 지점에서 회전된 상태로 주어지고
# 목표값(target)이 주어질 때, target의 인덱스를 반환하라.
# 존재하지 않으면 -1을 반환하라.

input_list = [4, 5, 6, 7, 0, 1, 2]
input_target = 0
output_result = 4

def solution(input_list, t):
    # 시작, 끝 인덱스 설정
    start = 0
    end = len(input_list) - 1
    
    # 반복문: start가 end보다 작거나 같은 동안 반복
    while start <= end:
        # 중간 인덱스 설정
        mid = (start + end) // 2
        # 조건문: 중간값이 목표값과 일치하는가
        if t == input_list[mid]:
            # 만족 시: 해당 인덱스 반환
            return mid
            
        # 조건문: 왼쪽 절반(start ~ mid)이 정렬되어 있는가
        elif input_list[start] <= input_list[mid]:
            # 조건문: 목표값이 정렬된 왼쪽 절반의 범위 안에 있는가
            if input_list[start] <= t < input_list[mid]:
                # 만족 시: 끝 인덱스를 mid-1로 이동
                end = mid-1
            # 아닐 경우: 시작 인덱스를 mid+1로 이동
            else:
                start = mid+1
        # 아닐 경우(오른쪽 절반(mid ~ end)이 정렬되어 있음)
        else:
            # 조건문: 목표값이 정렬된 오른쪽 절반의 범위 안에 있는가
            if input_list[mid] < t <= input_list[end]:
                # 만족 시: 시작 인덱스를 mid+1로 이동
                start = mid+1
            # 아닐 경우: 끝 인덱스를 mid-1로 이동
            else:
                end = mid-1
    
    # 반복문 종료까지 찾지 못한 경우: -1 반환
    return -1

print(solution(input_list, input_target))
print(output_result)
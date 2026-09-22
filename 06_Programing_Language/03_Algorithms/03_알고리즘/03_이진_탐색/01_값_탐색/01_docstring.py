# 값 탐색(exact value search)
# 정렬된 배열에서 특정 목표값(target)이 존재하는지
# 존재한다면 그 인덱스를 찾는 이진 탐색의 기본형
# 왼쪽/오른쪽 경계(left, right)를 설정하고,
# 중간 인덱스(mid)의 값과 목표값을 비교해 탐색 범위를 절반씩 좁혀간다.

# 문제
# 오름차순으로 정렬된 정수 배열과 목표값(target)이 주어질 때,
# 목표값의 인덱스를 반환하라.
# 존재하지 않으면 -1을 반환하라.

input_list = [1, 3, 5, 7, 9, 11, 13]
input_target = 7
output_result = 3

def solution(input_list: list[int], t: int) -> int:
    # 1. 완전 탐색
    # # 반복문: 배열의 마지막까지 순회
    # for i in range(len(input_list)):
    #     # 조건문: 목표값과 일치하는지
    #     if input_list[i] == t:
    #         # 만족할 경우, 목표값의 인덱스 반환
    #         return i

    # # 없을 경우 -1 반환
    # return -1

    # 2. 이진 탐색
    # 시작, 끝 인덱스 설정
    start = 0
    end = len(input_list)-1

    # 반복문: start가 end보다 커질 때까지 반복
    while start <= end:
        # 중간 인덱스 설정
        mid = (start + end) // 2

        # 조건문: 중간값이 목표값과 일치한가
        if input_list[mid] == t:
            # 만족할 경우, 해당 인덱스 반환
            return mid

        # 조건문: 중간값이 목표값보다 작은가
        elif input_list[mid] < t:
            # 만족할 경우, 시작 인덱스를 중간 인덱스+1로 재할당
            start = mid+1

        # 조건문: 중간값이 목표값보다 큰가
        else:
            # 만족할 경우, 종료 인덱스를 중간 인덱스-1로 재할당
            end = mid-1

    # 없을 경우 -1 반환
    return -1

print(solution(input_list, input_target))
print(output_result)
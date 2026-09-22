# 경계값 탐색(lower bound / upper bound)
# 정렬된 배열에서 특정 값 이상(또는 이하)이 처음(또는 마지막) 나타나는 위치를 찾는 이진 탐색 변형.
# 중복값이 존재하는 배열에서 값이 정확히 일치하는 인덱스가 여러 개일 때 그 경계를 찾는 데 사용
# 값 탐색과 달리 값을 찾아도 즉시 종료하지 않고 탐색 범위를 좁혀나가는 것이 핵심.

# 문제
# 정렬된 정수 배열과 목표값(target)이 주어질 때, target이 처음 나타나는 인덱스(lower bound)를 반환하라.
# target이 배열에 없으면, target보다 크면서 가장 작은 값이 위치할 인덱스를 반환하라.

input_list = [1, 2, 2, 2, 3, 4, 5]
input_target = 2
output_result = 1

def solution(input_list, t):
    # 시작, 끝 인덱스 설정
    start = 0
    end = len(input_list)-1

    # 결과 초기화
    result = 0

    # 반복문: start보다 end가 작거나 같아질 때까지 순회
    while start <= end:
        # 중간 인덱스 선언
        mid = (start + end) // 2

        # 조건문: 중간값이 목표값 이상인가
        if input_list[mid] >= t:
            # 만족할 경우, 이 위치가 lower bound 후보이므로 결과에 저장
            result = mid
            # 왼쪽에 더 있을 수 있으므로 끝 인덱스를 중간 인덱스-1로 변환
            end = mid-1

        # 만족하지 않을 경우,
        else:
            # 시작 인덱스를 중간 인덱스+1로 이동
            start = mid+1

    return result

print(solution(input_list, input_target))
print(output_result)
# 매개변수 탐색(parametric search)
# 배열의 인덱스가 아니라 "답이 될 수 있는 값의 범위(정답 후보)"에 이진 탐색을 적용하는 유형
# 정렬된 배열이 없어도 되며, "이 값이 조건을 만족하는가"라는 판별 함수(decision function)가
# 단조성(monotonicity)을 가질 때 적용 가능하다.
# 즉 어떤 값 X가 조건을 만족하면, X보다 큰(또는 작은) 모든 값도 조건을 만족한다는 성질을 이용해
# 최적값을 이진 탐색으로 좁혀나간다.

# 문제

input_list = [5, 10, 6]
input_target = 4
output_result = 5

# A B C
# 0 1 0
# 0 1 0
# 0 1 0
# 0 1 0
# 0 1 1
# 1 1 1 <-
# 1 1 1
# 1 1 1
# 1 1 1
# 1 1 1
# -----
# 5 10 6

def solution(input_list, t):
    # 바이너리를 사용해야 하는 근거
    # 초기화 (개수, 시작, 종료)

    # 반복문: 시작 <= 종료

        # 전체 개수 파악

        # 조건문: 줄 수 있는 값이 k보다 크면, 시작값 올려야 함
        사탕알의 개수 = mid
        start = mid + 1

        # 아닐 경우(mid 값이 k보다 작으면), 종료값 줄여야 함
        end = mid - 1

    return 사탕알의 개수


print(solution(input_list, input_target))
print(output_result)
# 매개변수 탐색(parametric search)
# 배열의 인덱스가 아니라 "답이 될 수 있는 값의 범위(정답 후보)"에 이진 탐색을 적용하는 유형
# 정렬된 배열이 없어도 되며, "이 값이 조건을 만족하는가"라는 판별 함수(decision function)가
# 단조성(monotonicity)을 가질 때 적용 가능하다.
# 즉 어떤 값 X가 조건을 만족하면, X보다 큰(또는 작은) 모든 값도 조건을 만족한다는 성질을 이용해
# 최적값을 이진 탐색으로 좁혀나간다.

# 문제
# 나무들의 높이가 담긴 배열과 필요한 나무 길이(target)가 주어질 때
# 절단기의 높이(H)를 설정해 모든 나무를 H 높이에서 자를 때
# 얻을 수 있는 나무 길이의 합이 target 이상이 되는 가장 큰 H를 구하라.
# (H보다 낮은 나무는 잘리지 않는다.)

input_list = [20, 15, 10, 17]
input_target = 7
output_result = 15

def solution(input_list, t):
    # 현재 절단기 높이(h) 초기화
    h = 0

    # h를 하나씩 올리면서, 이번에 얻을 수 있는 나무 길이가 얼마인지 파악한다.
    # 현재 나무 길이가 필요한 나무 길이(t)보다 커지면 멈추고, h를 하나 올린다.
    # (반복)
    # 만약 나무들의 높이 리스트를 모두 돌았을 때, t와 일치하면 해당 h를 반환한다.
    
    # 가장 긴 나무를 이분 탐색의 시작, 끝 기준으로 잡는다.
    start = 0
    end = sorted(input_list, reverse=True)[0]

    # 반복문: start가 end보다 커지기 전까지 반복
    while start <= end:
        # 중간 길이
        mid = (start + end) // 2

        # 나무 길이 합산하기
        total_tree_length = 0
        for tree_length in input_list:
            total_tree_length += max(0, tree_length - mid)

        # 조건문: 나무 길이의 합산이 t보다 큰가
        if total_tree_length >= t:
            # 만족할 경우, 중간 길이를 더 높게 설정(시작 인덱스를 중간 값보다 크게 설정)
            h = mid
            start = mid + 1
        
        # 나무 길이의 합산이 t보다 작은가
        else:
            # 만족할 경우, 중간 길이를 더 낮게 설정(종료 인덱스를 중간 값보다 작게 설정)
            end = mid - 1

    return h

print(solution(input_list, input_target))
print(output_result)
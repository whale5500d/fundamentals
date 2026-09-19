# 배열 회전/뒤집기(array rotatin/reversal)
# 배열 요소의 위치를 순환적으로 이동시키거나(회전, rotation)
# 순서를 역순으로 바꾸는(뒤집기, reversal) 인덱스 조작 기법
# 추가 배열 없이 원본 배열 내에서 처리(in-place)하는 것이 핵심
# 모듈러 연산(modulo operation)으로 순환 인덱스를 계산하는 개념이 함께 쓰임.

# 문제
# 정수 배열과 정수 K가 주어질 때,
# 배열을 오른쪽으로 K칸 회전시킨 결과를 반환하기

input_list = [1, 2, 3, 4, 5]
input_int = 7
output_result_1 = [4, 5, 1, 2, 3]

def solution_1(input_list: list[int], k:int) -> list[int]:
    # # edge case
    # # 모듈러 연산: 함수 시작 부분에서 k = k % len(list)로 k를 배열 길이 범위 내로 정규화
    # k = k % len(input_list)
    # # 같은 배열 두 개를 연결
    # result = input_list + input_list
    # # 첫 인덱스는 list 길이 - k
    # first_index = len(input_list) - k
    # # 마지막 인덱스는 첫 인덱스 + list 길이
    # last_index = first_index + len(input_list)
    # # 첫 인덱스부터 마지막 인덱스까지 slice
    # result = result[first_index:last_index]

    # return result

    # 반환 값 타입: list[int]
    result = []
    
    # (edge case 1) 조건문: k가 배열 길이보다 큰 경우 처리(순환 회전이므로 나머지 연산 필요)
    k = k % len(input_list) if len(input_list) < k else k
    
    # 회전 결과를 담을 새로운 배열 구성
    # (오른쪽 K칸 회전 = 뒤에서 K개를 앞으로, 나머지를 뒤로)
    # (edge case 2) 파이썬은 -0 == 0으로 취급하므로, 의도한대로 동작하지만
    # 다른 언어의 경우로 이식할 때는 별도 엣지 케이스로 명시적으로 처리하는 것이 안전하다.
    result = input_list[-k:] + input_list[:-k] if k != 0 else input_list
    
    # 최종 배열 반환
    return result

print(solution_1(input_list, input_int))
print(output_result_1)

# 배열 뒤집기(array reversal): 배열 요소의 순서를 역순으로 바꾸는 인덱스 조작 깁법

# 문제
# 정수 배열이 주어질 때, 배열 전체를 뒤집은 결과를 반환하라.
# 단, 추가 배열을 생성하지 않고 원본 배열 내에서 처리(in-place)해야 한다.
# 앞서 다룬 투 포인터 개념을 적용할 수 있는 문제(?)

output_result_2 = [5, 4, 3, 2, 1]

def solution_2(input_list: list[int]) -> list[int]:
    # left 인덱스
    left = 0
    # right 인덱스
    right = len(input_list)-1

    # 반복문: 전체 길이의 중간 전까지만 반복
    while left < len(input_list)//2:
        # 스왑
        input_list[left], input_list[right] = input_list[right], input_list[left]

        left += 1
        right -= 1

    return input_list

print(solution_2(input_list))
print(output_result_2)
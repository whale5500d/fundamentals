# 배열에서 특정 값을 삽입하되, 정렬 상태(오름차순)을 유지해야 한다.
# 정수 배열과 삽입할 값이 주어질 때, 정렬을 유지하며 값을 삽입한 결과 배열을 반환하는 함수를 작성하라.

input_array = [1,3,5,7]
input_value = 4
output_result = [1,3,4,5,7]

def solution(array: list[int], value: int) -> list[int]:
    # 결과를 담을 새로운 배열 선언 (또는 기존 배열 복사본)
    result = array[:]
    
    # 반복문: 배열을 순회하며 삽입 위치 탐색
    for index in range(len(array)):
        # 조건문: 현재 요소가 삽입값보다 큰지 확인 (삽입 위치 판단)
        if array[index] > value:
            # 조건 만족 시: 해당 위치에 값을 삽입하고 종료
            result.insert(index, value)
            break
        
    # 반복문 종료까지 삽입 못한 경우: 배열 끝에 값 추가
    if len(array) == len(result):
        result.append(value)
    
    # 최종 배열 반환
    return result

print(solution(input_array, input_value))
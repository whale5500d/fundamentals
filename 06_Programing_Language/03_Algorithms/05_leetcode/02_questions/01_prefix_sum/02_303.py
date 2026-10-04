# https://leetcode.com/problems/range-sum-query-immutable/

# Example
input_list = [3, 1, 4, 1, 5]
output_result = 6

class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def sumRange_completSearch(self, left: int, right: int) -> int:
        # 누적합 결과 초기화
        accumulated = 0

        # 반복문: left부터 right까지 순회
        for index in range(left, right+1):
            num_value = self.nums[index]
            # 순회한 결과 value를 accumulated에 합산
            accumulated += num_value

        # 누적합 결과 반환
        return accumulated

class NumArray2:
    def __init__(self, nums: list[int]):
        self.prefix = [0]

        accumulated = 0
        for value in nums:
            accumulated += value
            self.prefix.append(accumulated)

    def sumRange_prefixSum(self, left: int, right: int) -> int:
        return self.prefix[right+1] - self.prefix[left]


num_array = NumArray(input_list)
num_array2 = NumArray2(input_list)

print(num_array.sumRange_completSearch(1, 3))
print(num_array2.sumRange_prefixSum(1, 3))
print(output_result)

# prefix[right] - prefix[left-1]가 아닌 prefix[right+1] - prefix[left]를 하는 이유
# "prefix를 초기화할 때, []이 아닌 [0]로 초기화하는 이유"가 원인
# left <= range < right+1 이므로
# prefix 초기화를 []로 할 경우, left == 0일 때는 첫 번째까지 합산한 결과가 된다.
# 이는 합산하지 않은 초기값을 생략하므로, sumRange(0, 1)와 같은 첫 번째까지 합산 결과 반환에 실패한다.
# 초기화할 때 의도적으로 [0]을 추가함으로서, 첫 번째까지 합산 결과를 성공시킨다.

# 기존 사고 방식
# prefix[i]: nums[0 ... i]의 합
# 구간 합의 일반형: sum(left ... right) = nums[0...right]의 합 - num[0...left-1]의 합
# 일반형이 요구하는 값: left == 0 이면 원소 0개인 구간의 합임.
# 정의의 한계: 기존 사고 방식은 원소가 1개 이상인 구간의 합만 저장되므로, 원소 0개인 구간의 합을 담을 인덱스가 없음.
# 결과: 일반형의 두 번째 항이 left == 0일 때만 배열 밖의 값이 되어, left에 따라 식이 둘로 갈라진다.

# 놓친 점: left-1까지 합은 left == 0일 때 값이 저장 대상이 되지 못함.
# 원인: prefix를 '원소가 있는 구간의 합'으로만 정의함. 빈 구간을 값으로 취급하지 않음.
# 수정: 빈 구간의 합 0도 하나의 값으로 보고 prefix[0]에 저장

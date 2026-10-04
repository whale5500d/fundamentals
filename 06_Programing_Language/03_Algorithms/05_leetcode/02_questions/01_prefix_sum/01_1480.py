# https://leetcode.com/problems/running-sum-of-1d-array/

# Example 1
# input_list = [1, 2, 3, 4]
# output_result = [1, 3, 6, 10]

# Example 2
# input_list = [1, 1, 1, 1, 1]
# output_result = [1, 2, 3, 4, 5]

# Example 3
input_list = [3, 1, 2, 10, 1]
output_result = [3, 4, 6, 16, 17]

# 완전 탐색
class Solution:
    def runningSum_completeSearch(self, nums: list[int]) -> list[int]:
        # 누적합 결과를 담을 배열 선언
        results = []

        # 반복문: nums 배열 전체 순회
        for i in range(len(nums)):
            accumulated = 0
            # 반복문: 처음부터 i까지 value 합산
            for j in range(i+1):
                accumulated += nums[j]

            results.append(accumulated)

        return results
    
    def runningSum_prefixSum(self, nums: list[int]) -> list[int]:
        # 누적합 결과를 담을 배열, 누적합 변수 초기화
        results = []
        accumulated = 0

        # 반복문: nums 배열 전체 순회
        for value in nums:
            # 이전 누적합에 현재 value만 합산
            accumulated += value

            # 현재 합산 결과를 바로 results에 추가
            results.append(accumulated)

        return results

solution = Solution()
print(solution.runningSum_completeSearch(input_list))
print(solution.runningSum_prefixSum(input_list))
print(output_result)

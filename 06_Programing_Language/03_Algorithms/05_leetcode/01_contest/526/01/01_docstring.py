# Q1. Minimum Value of Merged Integers

# You are given an integer array nums of even length n.
# You have to merge the elements of nums in pairs by merging nums[0] with nums[1], nums[2] with nums[3], and so on, until nums[n - 2] with nums[n - 1].
# Return the minimum value among all the resulting merged integers.
# To merge two integers, concatenate all the decimal digits of the first integer followed by all the decimal digits of the second integer.

# Example 1:
# Input: nums = [23,55,42,21]
# Output: 2355
# Explanation:
# Merging nums[0] = 23 and nums[1] = 55 gives 2355.
# Merging nums[2] = 42 and nums[3] = 21 gives 4221.
# The minimum value among the merged numbers is min(2355, 4221) = 2355.

# Example 2:
# Input: nums = [34,7,11,11]
# Output: 347
# Explanation:
# Merging nums[0] = 34 and nums[1] = 7 gives 347.
# Merging nums[2] = 11 and nums[3] = 11 gives 1111.
# The minimum value among the merged numbers is min(347, 1111) = 347.

# Example 3:
# Input: nums = [9,20]
# Output: 920
# Explanation:
# Merging nums[0] = 9 and nums[1] = 20 gives 920.
# There is only one merged number, so the minimum value is 920.

# Constraints:
# 2 <= n == nums.length <= 100
# n is even
# 1 <= nums[i] <= 1000

class Solution:
    def minMergedInteger(self, nums: list[int]) -> int:
        # 1. 병합 결과 배열 초기화
        merges = []
        
        # 2. 배열의 길이는 항상 짝수이므로, 인덱스를 2씩 건너뛰면서 순회
        for index in range(0, len(nums), 2):
            # 3. 첫 번째와 두 번째 값을 병합한 결과를 외부 변수에 담는다.
            merges.append(int(str(nums[index]) + str(nums[index+1])))

        # 4. 배열 내 결과 중 최소값을 반환한다.
        min_value = float("inf")
        for merge in merges:
            min_value = min(min_value, merge)

        return int(min_value)
# Q2. Minimize the Maximum Value of GCD-Connected Array

# You are given three integers n, index, and value.
# An integer array nums of length n is called GCD-Connected if:

# nums[i] > 0 for 0 <= i <= n - 1.
# nums[i] < nums[i + 1] for 0 <= i <= n - 2.
# nums[index] = value.
# gcd(nums[i], nums[i + 1]) > 1 for 0 <= i <= n - 2.

# Return the minimum possible maximum value, nums[n - 1], among all GCD-Connected arrays nums. If no such array exists, return -1.

# Example 1:
# Input: n = 4, index = 2, value = 8
# Output: 10
# Explanation:
# The GCD-Connected array will look like: ​​​​​​​nums = [?, ?, 8, ?] since nums[2] = 8.
# Since nums[3] > 8 and gcd(8, 9) = 1, every valid GCD-Connected array must have nums[3] >= 10.
# One optimal array satisfying all conditions is [2, 4, 8, 10].
# Thus, the minimum possible value of nums[3] is 10.

# Example 2:
# Input: n = 2, index = 1, value = 3
# Output: -1
# Explanation:
# The GCD-Connected array will look like: nums = [?, 3] since nums[1] = 3.
# Since we need 0 < nums[0] < nums[1] = 3, there are only two possible arrays: [1, 3] and [2, 3]. Neither of them satisfies gcd(nums[0], nums[1]) > 1.
# Therefore, no valid GCD-Connected array exists, and the answer is -1.

# Example 3:
# Input: n = 2, index = 0, value = 3
# Output: 6
# Explanation:
# The GCD-Connected array will look like: nums = [3, ?] since nums[0] = 3.
# Since nums[1] > 3 and gcd(3, 4) = gcd(3, 5) = 1, every valid GCD-Connected array must have nums[1] >= 6.
# One optimal array is [3, 6].
# Thus, the minimum possible value of nums[1] is 6.

# Constraints:
# 2 <= n <= 109
# 1 <= value <= 109
# 0 <= index <= n - 1

class Solution:
    def minimumMaxValue(self, n: int, index: int, value: int) -> int:
        # (edge) 1은 어떤 수와도 gcd가 1이므로 이웃할 수 없다.
        if value == 1:
            return -1

        left_count = index
        right_count = n-1-index
        prime_factor = self.smallest_prime_factor(value)

        # 1. 왼쪽 구간 가능 여부 판정
            # - value가 짝수일 경우, 2, 4, ..., value-2가 사슬이므로 최대 value//2-1개
            # - value가 홀수일 경우, 바로 앞은 value-p(짝수), 그 아래는 짝수 사슬이므로 최대 (value-p)//2
        if value % 2 == 0:
            maximum_left_count = value//2-1
        else:
            maximum_left_count = (value-prime_factor)//2

        if left_count > maximum_left_count:
            return-1

        # 오른쪽 구간 최소값 계산
            # - right_count == 0이면 value를 반환함
        if right_count == 0:
            return value

            # - value가 짝수일 경우, 이후 모두 +2씩 증가
        if value % 2 == 0:
            return value + 2 * right_count

            # - value가 홀수일 경우, 첫 칸은 value+p(짝수), 이후 +2씩 증가
        return value + prime_factor + 2 * (right_count - 1)
            
    def smallest_prime_factor(self, number: int) -> int:
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                return divisor
            divisor += 1
        return number
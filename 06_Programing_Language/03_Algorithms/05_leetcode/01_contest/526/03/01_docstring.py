# Q3. Minimum Operations to Sort With Locked Indices

# You are given an integer array nums of length n, where nums is a permutation of the integers in the range [1, n].
# You are also given a binary array locked of length n and an integer k.

# locked[i] = 1 means index i is locked.
# locked[i] = 0 means index i is unlocked.

# You may perform the following operations in any order:
# Swap: Choose an index i such that both indices i and i + 1 are currently unlocked, and swap nums[i] and nums[i + 1].
# Unlock: Choose an index i such that locked[i] = 1 and permanently unlock it by setting locked[i] = 0.
# You may perform any number of swap operations but at most k unlock operations.

# Return the minimum total number of operations required to sort nums in strictly increasing order. If it is impossible, return -1.

# Example 1:
# Input: nums = [2,1,3,4], locked = [0,1,0,1], k = 1
# Output: 2
# Explanation:
# Unlock index 1. The array locked becomes [0,0,0,1].
# Swap nums[0] and nums[1]. The array nums becomes [1,2,3,4].
# The total number of operations is 1 + 1 = 2.

# Example 2:
# Input: nums = [3,1,2], locked = [1,0,1], k = 2
# Output: 4
# Explanation:
# Unlock indices 0 and 2. All indices are now unlocked.
# Swap indices 0 and 1. The array nums becomes [1,3,2].
# Swap indices 1 and 2. The array nums becomes [1,2,3].
# The total number of operations is 2 + 2 = 4.

# Example 3:
# Input: nums = [2,3,1], locked = [1,0,0], k = 0
# Output: -1
# Explanation:
# Index 0 is locked, so its value cannot be moved. Since k = 0, no indices can be unlocked. Therefore, sorting the array is impossible.

# Constraints:
# 1 <= n == nums.length == locked.length <= 2000
# 1 <= nums[i] <= n
# 0 <= locked[i] <= 1
# nums is a permutation of the integers in the range [1, n].
# 0 <= k <= n

class Solution:
    def minOperations(self, nums: list[int], locked: list[int], k: int) -> int:
        # 0. 핵심 성질
        #    - 정렬 목표는 [1, 2, ..., n]이므로 인덱스 i의 목표 값은 i + 1임
        #    - 이웃 교환은 연속으로 풀린 구간 안에서만 값을 이동시킴
        #    - 따라서 "값 집합이 목표와 일치하는 가장 작은 구간(블록)"으로 나누면 블록끼리는 독립임
        n = len(nums)

        # 1. 블록 나누기
        #    - prefix_maximum == i + 1이면 nums[0..i]가 {1..i+1}의 순열이므로 여기서 블록을 끊음
        block_list = []
        block_start = 0
        prefix_maximum = 0

        for index in range(n):
            prefix_maximum = max(prefix_maximum, nums[index])
            if prefix_maximum == index + 1:
                block_list.append((block_start, index))
                block_start = index + 1

        unlock_count = 0
        swap_count = 0

        # 2. 블록별 처리
        for start, end in block_list:
            # 2-1. 블록 크기가 1이면 이미 제자리이므로 해제와 교환이 모두 필요 없음
            if start == end:
                continue

            # 2-2. 블록 크기가 2 이상이면 블록 안의 모든 잠긴 칸을 해제해야 함
            for index in range(start, end + 1):
                if locked[index] == 1:
                    unlock_count += 1

            #      블록 안의 역순 쌍(inversion) 개수 = 이웃 교환으로 정렬하는 최소 교환 횟수
            for left in range(start, end + 1):
                for right in range(left + 1, end + 1):
                    if nums[left] > nums[right]:
                        swap_count += 1

        # 3. 불가능 판정
        if unlock_count > k:
            return -1

        # 4. 결과 반환
        return unlock_count + swap_count
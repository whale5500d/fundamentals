# You are given an integer n and a string s of length n consisting of digits.
# The dial contains the digits 0 through 9 in order and is circular,
# so 0 and 9 are adjacent.
# The pointer initially points to 0.

# To dial each digit of s in order, rotate the pointer until it points to that digit.
# Each rotation moves the pointer to an adjacent digit,
# and you may rotate in either direction.
# Dialing a digit that the pointer already points to requires no rotations.

# Before dialing, you may perform the following operation at most once:
# Choose an index k such that 0 <= k < n and reverse the suffix s[k ... n-1].
# Return the minimum total number of rotations needed to dial the string
# after optimally choosing whether to perform the operation
# and which suffix to reverse.

# A suffix of a string is a contiguous of characters
# that begins at any position in the string and extends to its end.

test_s1 = "1502"
length_s1 = len(test_s1)
output_s1 = 9

test_s2 = "2916"
length_s2 = len(test_s2)
output_s2 = 12

test_s3 = "4219"
length_s3 = len(test_s3)
output_s3 = 6

class Solution1:
    def minRotations(self, n: int, s: str) -> int:
        # O(n^2)
        # Number of cases
        # 1. No reverse cases, 1
        # 2. Reverse cases, n (0, 1, ..., n-1)
        # Total, n+1

        # 1. 전체 횟수 계산 함수 선언
        def calculate_total_rotations(s: str) -> int:
            current_digit = 0
            total_rotations = 0

            # 반복문: s 전체 순회
            for character in s:
                # target_digit 선언
                target_digit = int(character)
                distance = abs(current_digit - target_digit)
                step = min(distance, 10-distance)
                total_rotations += step
                current_digit = target_digit

            return total_rotations

        # 2. 최소값 초기화
        min_rotations = calculate_total_rotations(s)

        # 3. 후보 순회
        # 반복문: n-1까지 순회
        for k in range(n):
            # 후보 문자열 생성
            candidate_string = s[:k] + s[k:][::-1]
            
            # 후보 문자열의 최소 회전 횟수
            candidate_rotations = calculate_total_rotations(candidate_string)

            # 조건문: 후보 회전 수가 기존 회전 수보다 적은가
            if candidate_rotations < min_rotations:
                min_rotations = candidate_rotations

        # 4. 최소값 반환
        return min_rotations

solution = Solution1()
print(solution.minRotations(length_s1, test_s1))
print(output_s1)
print(solution.minRotations(length_s2, test_s2))
print(output_s2)
print(solution.minRotations(length_s3, test_s3))
print(output_s3)

failed_case_length = 10_000
failed_case_string = '0123456789' * 1000


import time
start_time = time.perf_counter()
result = solution.minRotations(failed_case_length, failed_case_string)
elapsed_seconds = time.perf_counter() - start_time

print(result) # 9998
print(f"elaped={elapsed_seconds: .3f}s") # 24.621s

# class Solution2:
#     def minRotations(self, n: int, s: str) -> int:

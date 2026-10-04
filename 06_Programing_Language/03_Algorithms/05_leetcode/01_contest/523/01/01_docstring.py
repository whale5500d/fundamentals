# Your are given a string s of length 10 consisting of digits.
# The dial contains the digits 0 through 9 in order and is circular
# so 0 and 9 are adjacent.
# The pointer initially points to 0.
# To dial each digit of s in order, rotate the pointer until it points to that digit.
# Each rotation moves the pointer to an adjacent digit,
# and you may rotate in either direction.
# Dialing a digit that the pointer already points to requires no rotations.
# Return the minimum total number of rotations needed to dial every digit of s.

test_s1 = "0192837465"
test_s2 = "1200210200"

class Solution:
    def minRotations(self, s: str) -> int:
        # current_digit, total_rotations init
        current_digit = 0
        total_rotations = 0

        # loop: until last target_digit:
        for character in s:
            # target_digit init
            target_digit = int(character)

            # distance init
            distance = abs(current_digit - target_digit)
            step = min(distance, 10-distance)
            
            # add total_rotations
            total_rotations += step

            # current_digit update
            current_digit = target_digit

        # return total_rotations
        return total_rotations

solution = Solution()
print(solution.minRotations(test_s1))
print(solution.minRotations(test_s2))
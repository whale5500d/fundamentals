# 피보나치 수열(Fibonacci sequence)
# fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)로 정의되는 수열
# DP 핵심 조건 중 상태 정의, 점화식, 초기값이 모두 문제 정의 안에 드러나 있다.
# DP의 구성 요소를 확인하기에 적합하다.

# 중복 계산이 발생하는 구조: 단순 재귀로 fib(5)를 구하면 fib(3)이 2번, fib(2)가 3번 반복 계산된다.
# 호출 횟수는 n이 커질수록 지수적으로 늘어나 시간복잡도가 O(2^n)이 된다.
# 계산한 값을 저장해 재사용하면 각 fib(k)를 한 번만 계산하므로 O(n)으로 줄어든다.
# 앞서 배운 DFS의 재귀 구조에 저장 단계를 추가한 형태가 탑다운 DP다.

# 기초 문제
# 정수 n이 주어질 때, n번째 피보나치 수를 반환하라.
# 아래 세 가지 방식으로 각각 구현해 비교한다.
# 1. 단순 재귀: 저장 없이 점화식을 그대로 호출한다.
# 2. 탑다운(메모이제이션): 재귀에 계싼 결과 저장을 추가한다.
# 3. 바텀업(타뷸레이션): 반복문으로 dp[0]부터 dp[n]까지 채운다.

# 예시
# 입력: n = 10
# 출력: 55 (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55)

from typing import Optional
import time

# Basic
def solution_1(n: int) -> int:
    if n < 2:
        return n

    return solution_1(n-1) + solution_2(n-2)

# Memoization
def solution_2(n: int, memo: Optional[dict[int, int]] = None) -> int:
    if memo is None:
        memo = {}

    if n < 2:
        return n

    if n in memo:
        return memo[n]

    memo[n] = solution_2(n-1, memo) + solution_2(n-2, memo)
    return memo[n]

# Tabulation
def solution_3(n: int) -> int:
    if n < 2:
        return n

    dp = [0] * (n+1)
    dp[1] = 1

    for index in range(2, n+1):
        dp[index] = dp[index-1] + dp[index-2]

    return dp[n]

input_value = 10
output_result = 55

print(solution_1(input_value), solution_2(input_value), solution_3(input_value))
print(output_result)

# 비교 실험: n=35에서 단순 재귀와 메모이제이션의 실행 시간 측정
for solution in (solution_1, solution_2, solution_3):
    start = time.perf_counter()
    solution(35)
    end = time.perf_counter()
    print(f"{solution.__name__}: {end - start}초")
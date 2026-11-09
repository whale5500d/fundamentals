# 최장 공통 부분 수열(LCS, longest common subsequence)
# 두 문자열에서 각각 문자를 순서대로 뽑아(건너뛰기 허용) 만들 수 있는 공통 부분 수열 중 가장 긴 것의 길이를 구하는 문제
# 앞서 정리한 인덱스 2개(두 수열)를 쓰는 수열 비교 DP에 해당한다.
# 앞에서 푼 LIS가 수열 하나를 다뤘다면, 이 문제는 수열 두 개의 인덱스가 각각 상태의 한 축이 된다.

# 부분 수열과 부분 문자열의 구분
# 부분 수열(subsequence)은 문자를 건너뛰어도 되고
# 부분 문자열(substring)은 연속된 구간이다.
# "abcde"와 "ace"의 공통 부분 수열 "ace"는 연속이 아니므로 부분 문자열이 아니다.

# 앞에서 푼 2차원 DP와 달라지는 지점
# 격자 경로는 위치(행, 열), 0/1 배낭은 물건 번호와 용량이 두 인덱스였다.
# 이 문제는 각각의 앞부분 길이가 두 인덱스다.
# 직전 상태를 고르는 기준도 달라진다.
# 배낭은 담을지 말지, 격자 경로는 위와 왼쪽을 합산했다.
# 이 문제는 두 문자열의 마지막 문자가 같은지에 따라 점화식이 갈린다.

# 기초 문제
# 두 문자열 text1, text2가 주어질 때, 가장 긴 공통 부분 수열의 길이를 반환하라.
# 공통 부분 수열이 없으면 0을 반환한다. 두 문자열의 길이는 1 이상이다.

def solution(text1: str, text2: str) -> int:
    # 상태 정의: text1에서 처음부터 i번째까지 문자열과 text2에서 처음부터 j번째까지 문자열의 가장 긴 공통 부분 수열의 길이(LCS)
    text1_length = len(text1)
    text2_length = len(text2)

    # 초기값: 
    #   dp[0][j] = 0: text1의 앞 0개는 빈 문자열이다.
    #   dp[i][0] = 0: text2의 앞 0개는 빈 문자열이다.
    dp = [[0] * (text2_length+1) for _ in range(text1_length+1)]

    # 점화식:
    #   비교하는 마지막 문자열은 text1[i-1], text2[j-1]이다.
    #   두 문자열의 마지막 문자가 같을 때는 앞부분의 LCS에 1을 더한 값
    #   두 문자열의 마지막 문자가 다를 때는 두 후보 중 큰 값을 고른다.
    # 반복문: i와 j를 1부터 시작하여 위에서 아래오, 왼쪽에서 오른쪽으로 채움
    for i in range(1, text1_length+1):
        for j in range(1, text2_length+1):
            # 문자 인덱스: dp의 i, j는 앞에서 센 개수이고, 문자열의 인덱스는 0부터 시작한다.
            # dp[i][j]를 계산할 때 비교할 문자는 text1[i-1], text2[j-1]이다.
            
            # 조건문: 마지막 문자열이 같은가
            if text1[i-1] == text2[j-1]:
                # 성립한다면, 둘 다 제외한 상태의 LCS+1
                dp[i][j] = dp[i-1][j-1]+1
            else:
                # 다르면, 한쪽씩 버린 두 상태 중 최댓값
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 반환값: 답은 max 계산 없이 dp[m][n]이다.
    # LIS에서는 수열이 어느 위치에서 끝나도 max(dp)가 필요하다.
    # LCS에서는 '두 문자열 전체를 본 상태'가 정의에 이미 있어서 마지막 칸이 답이다.
    return dp[text1_length][text2_length]

input_text1 = "abcde"
input_text2 = "ace"
output_result = 3 # "ace"
print(solution(input_text1, input_text2))
print(output_result)

input_text1 = "abc"
input_text2 = "abc"
output_result = 3 # "abc"
print(solution(input_text1, input_text2))
print(output_result)

input_text1 = "abc"
input_text2 = "def"
output_result = 0 # 공통 문자 없음
print(solution(input_text1, input_text2))
print(output_result)

input_text1 = "AGGTAB"
input_text2 = "GXTXAYB"
output_result = 4 # "GTAB"
print(solution(input_text1, input_text2))
print(output_result)
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
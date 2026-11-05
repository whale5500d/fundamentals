input_list = ["NumArray", "sumRange", "update", "sumRange"]
input_factors = [[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
output_result = [None, 9, None, 8]

class NumArray:

    def __init__(self, nums: list[int]):
        # 1. 필드 준비
        #    - self.size: len(nums)
        #    - self.tree: 길이 4 * size (재귀 분할에서 노드 번호가 2 * size를 넘을 수 있어 4배로 잡음)
        self.size = len(nums)
        self.tree = [0] * (4 * self.size)

        # 2. 트리 구성: 루트(node = 1)가 전체 구간 [0, size - 1]을 담당
        self.build(1, 0, self.size - 1, nums)

    def build(self, node: int, start: int, end: int, nums: list[int]) -> None:
        # 1. 기저 조건: 구간 길이가 1이면 잎, 원소 값을 저장
        if start == end:
            self.tree[node] = nums[start]
            return

        # 2. 구간을 반으로 나눠 양쪽 자식을 먼저 구성
        middle = (start + end) // 2
        self.build(2 * node, start, middle, nums)
        self.build(2 * node + 1, middle + 1, end, nums)

        # 3. 현재 노드 = 두 자식의 합
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, index: int, val: int) -> None:
        self.updateNode(1, 0, self.size - 1, index, val)

    def updateNode(self, node: int, start: int, end: int, index: int, val: int) -> None:
        # 1. 기저 조건: 잎에 도달하면 값을 교체
        if start == end:
            self.tree[node] = val
            return

        # 2. index가 속한 쪽 자식으로만 내려감
        middle = (start + end) // 2
        if index <= middle:
            self.updateNode(2 * node, start, middle, index, val)
        else:
            self.updateNode(2 * node + 1, middle + 1, end, index, val)

        # 3. 돌아오면서 현재 노드를 다시 계산
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def sumRange(self, left: int, right: int) -> int:
        return self.query(1, 0, self.size - 1, left, right)

    def query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        # 1. 노드 구간이 조회 구간과 겹치지 않으면 0
        if right < start or end < left:
            return 0

        # 2. 노드 구간이 조회 구간에 완전히 포함되면 저장된 합을 그대로 반환
        if left <= start and end <= right:
            return self.tree[node]

        # 3. 일부만 겹치면 양쪽 자식에게 나눠 묻고 합침
        middle = (start + end) // 2
        return (self.query(2 * node, start, middle, left, right)
                + self.query(2 * node + 1, middle + 1, end, left, right))


obj = NumArray([1, 3, 5])
print(obj.sumRange(0, 2))   # 9
obj.update(1, 2)
print(obj.sumRange(0, 2))   # 8
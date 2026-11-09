# 뒤집기(reversal)
# 연결 리스트의 노드 순서를 반대로 바꾸는 유형
# 각 노드의 next_node 참조 방향을 반대로 돌려서, 마지막 노드가 새로운 head가 되게 한다.

# 배열 뒤집기와 달라지는 지점
# 배열 뒤집기는 투 포인터(two pointer)로 양 끝의 값을 교환했다.
# 연결 리스트는 두 가지 이유로 같은 방식을 사용할 수 없다.
# 단일 연결 리스트는 뒤로 이동할 수 없어서 오른쪽 포인터를 right = -1로 옮길 수 없고,
# 인덱스 접근이 O(N)이라 양 끝 교환이 비효율적이다.
# 대신 값은 그대로 두고 참조의 방향만 한 칸씩 바꾼다.
# 앞서 정리한 핵심 조건 중 포인터 재연결 순서가 이 문제의 전부다.

# 기초 문제
# 단일 연결 리스트의 head가 주어질 때, 리스트를 뒤집고 새로운 head를 반환하라.
# 새 노드를 만들지 않고 기존 노드의 next_node만 바꿔야 한다.(in-place)
# 노드 클래스와 변환 함수는 앞서 만든 것을 재사용한다.

# 정리해볼 지점
# 필요한 변수
# 재연결 순서
# 초기값
# 종료 조건과 반환값
# 경계 케이스

class ListNode:
    def __init__(self, value: int = 0, next_node: "ListNode | None" = None):
        self.value = value
        self.next_node = next_node

def list_to_linked_list(values: list[int]) -> ListNode | None:
    # 더미 노드 생성: 값이 없는 임시 노드 생성
    dummy_node = ListNode()

    # 꼬리 포인터 초기화: 지금까지 만든 리스트의 마지막 노드를 가리킴
    tail_node = dummy_node
    
    # 반복문: 파이썬 리스트의 값을 순서대로 순회
    for value in values:
        # 새 노드 생성
        new_node = ListNode(value)
        # 꼬리 노드의 next_node에 새 노드 연결
        tail_node.next_node = new_node
        # 꼬리 포인터를 새 노드로 이동
        tail_node = new_node
    
    # 더미 노드의 다음 노드를 반환 (빈 리스트면 None)
    return dummy_node.next_node

def linked_list_to_list(head: ListNode | None) -> list[int]:
    # 결과를 담을 파이썬 리스트 초기화
    result = []

    # 현재 노드 초기화: head에서 시작
    current_node = head
    
    # 반복문: 현재 노드가 None이 아닌 동안 반복
    while current_node is not None:
        # 현재 노드의 값을 결과에 추가
        result.append(current_node.value)
        # 현재 노드를 다음 노드로 이동
        current_node = current_node.next_node

    # 결과 반환
    return result


def reverse_linked_list(head: "ListNode | None") -> ListNode | None:
    # 이미 뒤집은 쪽의 맨 앞 초기화: 처음에는 뒤집은 노드가 없음
    previous_node = None

    # 현재 노드 초기화: head에서 시작
    current_node = head

    # 반복문: 현재 노드가 None이 아닌 동안 반복
    while current_node is not None:
        # 다음 노드 저장: 참조를 바꾸기 전에 나머지 리스트의 맨 앞을 보관
        saved = current_node.next_node
        # 재연결: 현재 노드의 next_node를 이미 뒤집은 쪽의 맨 앞으로 변경
        current_node.next_node = previous_node
        # 이동: 이미 뒤집은 쪽의 맨 앞을 현재 노드로 갱신
        previous_node = current_node
        # 이동: 현재 노드를 저장해 둔 다음 노드로 갱신
        current_node = saved

    # 새로운 head 반환: 반복이 끝났을 때 뒤집은 쪽의 맨 앞
    return previous_node

print(linked_list_to_list(reverse_linked_list(list_to_linked_list([1, 2, 3, 4, 5]))))
# [5, 4, 3, 2, 1]
print(linked_list_to_list(reverse_linked_list(list_to_linked_list([]))))
# []
print(linked_list_to_list(reverse_linked_list(list_to_linked_list([7]))))
# [7]
print(linked_list_to_list(reverse_linked_list(list_to_linked_list([1, 2]))))
# [2, 1]
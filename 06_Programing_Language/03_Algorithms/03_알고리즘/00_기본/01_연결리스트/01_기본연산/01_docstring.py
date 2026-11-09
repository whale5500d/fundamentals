# 연결 리스트 기본 연산(basic operations)
# 노드를 직접 구현하고, 리스트의 앞과 뒤에 노드를 삽입하며, 값으로 노드를 삭제하는 유형이다.
# 이후 모든 연결 리스트 문제의 기반이 된다.
# 앞에서 정리한 핵심 조건 중 포인터 재연결 순서, 경계 케이스, 더미 노드를 이 문제에서 처음 적용한다.

# 배열과 달라지는 지점
# 배열은 array.insert(index, value), array.remove(value)처럼 내장 메서드가 연산을 대신한다.
# 연결 리스트는 메서드가 없어서 next_node 참조를 직접 바꿔야 한다.
# 앞에서 배운 참조 할당(result = array)이 이 연산의 기반이다.
# node.next_node = other는 값을 복사하지 않고 같은 객체를 가리키게 만든다.

# 기초 문제
# 아래 세 가지를 구현하라.
#   변환 함수: 파이썬 list를 ListNode 연결 리스트로 바꾸는 함수와, 연결 리스트를 파이썬 list로 되돌리는 함수, 이후 모든 연결 리스트 문제의 입출력 검증에 재사용된다.
#   삽입: 연결 리스트의 맨 앞(head 앞)에 값을 삽입하는 함수와 맨 뒤에 삽입하는 함수
#   삭제: 연결 리스트에서 주어진 값을 가진 첫 번째 노드를 삭제하는 함수. 값이 없으면 리스트를 그대로 반환.

class ListNode:
    def __init__(self, value: int = 0, next_node: "ListNode | None" = None):
        self.value = value
        self.next_node = next_node

def list_to_linked_list(values: list[int]) -> ListNode | None:
    # 더미 노드 생성: 값이 없는 임시 시작 노드
    dummy_node = ListNode()
    
    # 꼬리 포인터 초기화: 지금까지 만든 리스트의 마지막 노드를 가리킴
    tail_node = dummy_node

    # 반복문: 파이썬 리스트의 값을 순서대로 순회
    for value in values:    
        # 새 노드 생성
        new_node = ListNode(value)
        # 꼬리 노드의 next_node에 새 노드를 연결
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

def insert_front(head: ListNode | None, value: int) -> ListNode:
    # 새 노드 생성
    new_node = ListNode(value)

    # 재연결 순서: 새 노드의 next_node를 기존 head로 먼저 설정
    new_node.next_node = head

    # 새 노드를 새로운 head로 반환
    return new_node


def insert_back(head: ListNode | None, value: int) -> ListNode:
    # 새 노드 생성
    new_node = ListNode(value)
    
    # 조건문: 빈 리스트(head가 None)인가
    if head is None:
        # 만족 시: 새 노드가 head이므로 반환
        return new_node
        
    # 현재 노드 초기화: head에서 시작
    current_node = head
    
    # 반복문: 현재 노드의 next_node가 None이 아닌 동안 이동 (마지막 노드까지)
    while current_node.next_node is not None:
        # 현재 노드를 다음 노드로 이동
        current_node = current_node.next_node
        
    # 마지막 노드의 next_node에 새 노드를 연결
    current_node.next_node = new_node
    
    # head 반환
    return head


def delete_value(head: ListNode | None, target: int) -> ListNode | None:
    # 더미 노드 생성: next_node가 head를 가리키도록 설정
    dummy_node = ListNode(next_node=head)
    
    # 현재 노드 초기화: 더미 노드에서 시작 (삭제 대상의 직전 노드를 추적)
    current_node = dummy_node
    
    # 반복문: 현재 노드의 다음 노드가 None이 아닌 동안 반복
    while current_node.next_node is not None:
        # 조건문: 다음 노드의 값이 target과 같은가
        if current_node.next_node.value == target:
            # 만족 시: 현재 노드의 next_node를 다음 노드의 next_node로 건너뛰어 연결
            current_node.next_node = current_node.next_node.next_node
            # 첫 번째 노드만 삭제하므로 반복 종료
            break
            
        # 아닐 경우: 현재 노드를 다음 노드로 이동
        current_node = current_node.next_node
        
    # 더미 노드의 다음 노드를 반환 (head가 삭제되었을 수 있음)
    return dummy_node.next_node

print(linked_list_to_list(list_to_linked_list([1, 2, 3])))
# [1, 2, 3]

print(linked_list_to_list(insert_front(list_to_linked_list([1, 2, 3]), 0)))
# [0, 1, 2, 3]

print(linked_list_to_list(insert_back(list_to_linked_list([1, 2, 3]), 4)))
# [1, 2, 3, 4]

print(linked_list_to_list(delete_value(list_to_linked_list([1, 2, 3]), 2)))
# [1, 3]

print(linked_list_to_list(delete_value(list_to_linked_list([1, 2, 3]), 1)))
# [2, 3] (head 삭제)

print(linked_list_to_list(delete_value(list_to_linked_list([1, 2, 3]), 3)))
# [1, 2] (마지막 노드 삭제)

print(linked_list_to_list(delete_value(list_to_linked_list([1, 2, 3]), 5)))
# [1, 2, 3] (없는 값)

print(linked_list_to_list(insert_back(None, 1)))
# [1] (빈 리스트에 삽입)

print(linked_list_to_list(delete_value(None, 1)))
# [] (빈 리스트에서 삭제)

print(linked_list_to_list(delete_value(list_to_linked_list([7]), 7)))
# [] (노드 하나 삭제)
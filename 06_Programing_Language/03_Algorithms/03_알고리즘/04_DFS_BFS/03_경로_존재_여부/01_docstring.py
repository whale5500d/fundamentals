
# 경로 존재 여부(path existence)
# 무방향 그래프에서 정점 A에서 정점 B로 간선을 따라 도달할 수 있는지 판별하는 유형.
# 앞서 배운 연결 요소 개념과 직접 연결됨.
# A와 B가 같은 연결 요소에 속하면 도달 가능하고, 다른 연결 요소에 속하면 도달 불가능하다.
# A에서 DFS 또는 BFS를 한 번 시작해 B가 방문되는지 확인하면 된다.

# 기초 문제
# 정점 개수 N과 간선 목록, 시작 정점 source, 목표 정점 destination이 주어질 때
# source에서 destination으로 도달 가능하면 True, 아니면 False를 반환하라.
# 정점 번호는 0부터 N-1이다.

from collections import deque

n = 6
input_list = [(0, 1), (1, 2), (3, 4)]
source = 0
destination_true = 2
destination_false = 4
output_result_true = True
output_result_false = False

def solution(n: int, edges: list[tuple[int, int]], source: int, destination: int) -> bool:
    # 인접 리스트 초기화 및 간선 목록 변환
    # (앞에서 만든 인접 리스트 변환 로직 적용)
    adjacency_list = [[] for _ in range(n)]
    for start_vertex, end_vertex in edges:
        adjacency_list[start_vertex].append(end_vertex)
        adjacency_list[end_vertex].append(start_vertex)

    # 방문 처리 배열 초기화: 정점 개수만큼 False로 생성
    visited = [False] * n

    # 탐색 자료구조 초기화: 시작 정점(source)을 넣고, 시작 정점을 방문 처리
    queue = deque([source])
    visited[source] = True

    # 반복문: 탐색 자료구조가 빌 때까지 반복
    while queue:
        # 현재 정점 꺼내기
        current_vertex = queue.popleft()

        # 조건문: 현재 정점이 목표 정점(destination)인가
        if current_vertex == destination:
            # 만족 시: 도달 가능하므로 True 반환
            return True

        # 반복문: 현재 정점의 인접 정점 순회
        for neighbor_vertex in adjacency_list[current_vertex]:
            # 조건문: 인접 정점을 아직 방문하지 않았는가
            if not visited[neighbor_vertex]:
                # 만족 시: 방문 처리 후 탐색 자료구조에 추가
                visited[neighbor_vertex] = True
                queue.append(neighbor_vertex)

    # 반복문 종료까지 목표 정점을 찾지 못한 경우: False 반환
    return False
    
print(solution(n, input_list, source, destination_true))
print(output_result_true)
print(solution(n, input_list, source, destination_false))
print(output_result_false)
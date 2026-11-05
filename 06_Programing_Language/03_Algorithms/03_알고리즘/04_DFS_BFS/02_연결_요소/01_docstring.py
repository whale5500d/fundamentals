# 연결 요소(conneted component)
# 무방향 그래프에서 간선을 따라 서로 도달할 수 있는 정점들의 최대 묶음
# 다른 묶음의 정점과는 어떤 경로로도 연결되지 않는다.
# DFS, BFS를 한 번 시작할 때 방문되는 정점 집합의 연결 요소 하나에 해당하므로, 탐색을 시작한 횟수가 연결 요소의 개수가 된다.

# 기초 문제
# 정점 개수 N과 간선 목록이 주어질 때, 연결 요소의 개수를 반환하라.
# 정점 번호는 0부터 N-1이며, 간선이 하나도 없는 정점도 하나의 연결 요소로 센다.

from collections import deque

input_list = [(0, 1), (1, 2), (3, 4)]
n = 6
output_result = 3 # ({0, 1, 2}, {3, 4}, {5})

def solution(n: int, edges: list[tuple[int, int]]) -> int:
    # 인접 리스트 초기화 및 간선 목록 변환
    # (앞에서 만든 인접 리스트 변환 로직 적용)
    adjacency_list = [[] for _ in range(n)]
    for start_vertex, end_vertex in edges:
        adjacency_list[start_vertex].append(end_vertex)
        adjacency_list[end_vertex].append(start_vertex)

    # 방문 처리 배열 초기화: 정점 개수만큼 False로 생성
    visited = [False] * n

    # 연결 요소 개수 초기화
    component_count = 0

    # 반복문: 정점 0부터 n-1까지 순회
    for source_vertex in range(n):
        # 조건문: 해당 정점을 아직 방문하지 않았는가
        if not visited[source_vertex]:
            # 만족 시: 탐색 시작 횟수(연결 요소 개수) 1 증가
            component_count += 1

            # 탐색 시작: 해당 정점에서 연결된 모든 정점을 방문 처리
            # (DFS 선택)
            # stack = [source_vertex]
            # visited[source_vertex] = True
            # while stack:
            #     current_vertex = stack.pop()
            #     for neighbor_vertex in adjacency_list[current_vertex]:
            #         if not visited[neighbor_vertex]:
            #             visited[neighbor_vertex] = True
            #             stack.append(neighbor_vertex)

            # (BFS 선택)
            queue = deque([source_vertex])
            visited[source_vertex] = True
            while queue:
                current_vertex = queue.popleft()
                for neighbor_vertex in adjacency_list[current_vertex]:
                    if not visited[neighbor_vertex]:
                        visited[neighbor_vertex] = True
                        queue.append(neighbor_vertex)

    # 연결 요소 개수 반환
    return component_count
    
print(solution(n, edges=input_list))
print(output_result)
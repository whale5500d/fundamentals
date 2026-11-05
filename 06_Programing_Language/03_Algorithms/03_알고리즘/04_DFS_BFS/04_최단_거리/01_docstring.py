# 최단 거리 (shortest distance, 가중치 없음)
# 가중치 (weight)가 없는 그래프에서 시작 정점에서 목표 정점까지 거치는 간선의 최소 개수를 구하는 유형이다.
# 앞에서 배운 경로 존재 여부가 "도달 가능한가"를 묻는다면, 이 유형은 "도달 가능하다면 가장 적은 이동 횟수는 얼마인가"를 묻는다.
# BFS는 시작 정점에서 가까운 층 (level) 순서로 정점을 방문하므로,
# 어떤 정점을 처음 방문한 시점의 층 번호가 그 정점까지의 최단 거리가 된다.
# DFS는 먼저 찾은 경로를 따라 깊게 들어가므로 그 경로가 최단이라는 보장이 없다.

# 기초 문제 제시:
# 정점 개수 N, 간선 목록, 시작 정점 source, 목표 정점 destination이 주어질 때, source에서 destination까지의 최소 간선 개수를 반환하라. 도달할 수 없으면 -1을 반환한다. 정점 번호는 0부터 N-1이며, 무방향 그래프이다.

# 예시 1:
# 입력: N=6, 간선 [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], source=0, destination=4
# 출력: 3 (0→1→3→4 또는 0→2→3→4)

# 예시 2:
# 입력: N=6, 간선 [(0, 1), (1, 2), (3, 4)], source=0, destination=4
# 출력: -1 (서로 다른 연결 요소)

from collections import deque

def solution(n: int, edges: list[tuple[int, int]], source: int, destination: int) -> int:
    # 인접 리스트 초기화 및 간선 목록 변환 (앞에서 만든 인접 리스트 변환 로직 적용)
    adjacency_list = [[] for _ in range(n)]
    for start_vertex, end_vertex in edges:
        adjacency_list[start_vertex].append(end_vertex)
        adjacency_list[end_vertex].append(start_vertex)

    # 거리 배열 초기화: -1은 미방문(도달 불가)을 의미, visited 배열 역할을 겸함
    distances = [-1] * n

    # 탐색 자료구조 초기화: 시작 정점을 넣고, 시작 정점의 거리를 0으로 기록
    queue = deque([source])
    distances[source] = 0

    # 반복문: 큐가 빌 때까지 반복
    while queue:
        # 현재 정점 꺼내기
        current_vertex = queue.popleft()

        # 조건문: 현재 정점이 목표 정점인가
        if current_vertex == destination:
            # 만족 시: 기록된 거리 반환
            return distances[current_vertex]

        # 반복문: 현재 정점의 인접 정점 순회
        for neighbor_vertex in adjacency_list[current_vertex]:
            # 조건문: 인접 정점을 아직 방문하지 않았는가 (거리가 -1인가)
            if distances[neighbor_vertex] == -1:
                # 만족 시: 현재 정점의 거리 + 1을 기록하고 큐에 추가
                distances[neighbor_vertex] = distances[current_vertex] + 1
                queue.append(neighbor_vertex)

    # 반복문 종료까지 목표 정점에 도달하지 못한 경우: -1 반환
    return -1
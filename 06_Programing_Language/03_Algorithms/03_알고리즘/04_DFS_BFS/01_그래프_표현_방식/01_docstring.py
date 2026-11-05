# 그래프 표현 방식(graph representation)
# 정점(vertex)과 간선(edge)으로 이루어진 그래프를 코드에서 저장하는 방식
# 탐색 알고리즘(DFS/BFS)을 적용하기 전에 입력을 탐색 가능한 형태로 변환하는 단계에 해당
# 인접 리스트(adjacency list): 각 정점마다 연결된 정점 목록을 저장한다. 공간 O(V+E)이며, 간선 수가 적은 희소 그래프(sparse graph)에 적합하다.
# 인접 행렬(adjacency matrix): V x V 크기의 2차원ㅇ 배열에 간선 존재 여부를 저장한다. 공간 O(V^2)이며, 두 정점 간 간선 존재 여부를 O(1)에 확인할 수 있다.

# 기초 문제
# 정점 개수 N과 간선 목록이 주어질 때, 무방향 그래프(undirected graph)를 인접 리스트로 변환해 반환하라.
# 정점 번호는 0부터 N-1이며, 각 정점의 인접 정점 목록은 오름차순으로 정렬한다.

n = 5
input_list = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
output_result = [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]

def solution(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    # 정점 개수만큼 빈 인접 리스트 초기화
    adjacency_list = [[] for _ in range(n)]

    # 반복문: 간선 목록 전체 순회
    for start_vertex, end_vertex in edges:
        # 무방향 그래프이므로 양방향으로 추가
        # start_vertex의 인접 목록에 end_vertex 추가
        adjacency_list[start_vertex].append(end_vertex)
        
        # end_vertex의 인접 목록에 start_vertex 추가
        adjacency_list[end_vertex].append(start_vertex)
        
    # 반복문: 각 정점의 인접 목록 순회
    for neighbors in adjacency_list:
        # 오름차순 정렬
        neighbors.sort()
    
    # 인접 리스트 반환
    return adjacency_list

print(solution(n, edges=input_list))
print(output_result)
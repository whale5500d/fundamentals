input_data="""
3 2 1
1 2 4
1 3 2
""".strip().splitlines()
input_index = 0
def input():
    global input_index
    result = input_data[input_index]
    input_index += 1
    return result

# 출발 노드 설정
INF = int(1e9) # 1_000_000_000
n, m, start = map(int, input().split())

# 최단 거리 테이블 초기화
graph = [[] for i in range(n+1)]
visited = [False] * (n+1)
distance = [INF] * (n+1)

for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))

print(graph)

def get_smallest_node():
    min_value = INF
    index = 0
    for i in range(1, n+1):
        if distance[i] < min_value and not visited[i]:
            min_value = distance[i]
            index = i

    return index

def dijkstra(start):
    distance[start] = 0
    visited[start] = True

    for j in graph[start]:
        v, w = j
        distance[v] = w

    for _ in range(n-1):
        now = get_smallest_node()
        visited[now] = True

        for j in graph[now]:
            v, w = j
            cost = distance[now] + w
            if cost < distance[v]:
                distance[v] = cost

dijkstra(start)

count = 0
max_distance = 0
for d in distance:
    if d != INF:
        count += 1
        max_distance = max(max_distance, d)

print(count-1, max_distance)
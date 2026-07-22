import { Queue } from "./01_queue.mjs";

function Graph() {
  this.edge = {};
  this.visited = {};
}

// addVertex(): 정점(Vertex) 추가
Graph.prototype.addVertex = function (v) {
  this.edge[v] = [];
  this.visited[v] = false;
};

// addEdge(): 간선(edge) 추가 (변경)
Graph.prototype.addEdge = function (v1, v2) {
  this.edge[v1].push(v2);
};

// print(): 현재 Graph 연결 상태 출력
Graph.prototype.print = function () {
  for (let vertex in this.edge) {
    let neighbors = this.edge[vertex];
    if (neighbors.length === 0) continue;

    process.stdout.write(`${vertex} -> `);
    for (let j = 0; j < neighbors.length; j++) {
      process.stdout.write(`${neighbors[j]} `);
    }

    console.log("");
  }
};

// bfs(): BFS 탐색
Graph.prototype.bfs = function (startVertex) {
  this._bfsLoopVisit(startVertex);
};

// _bfsLoopVisit(): 큐를 이용한 BFS 탐색
Graph.prototype._bfsLoopVisit = function (vertex) {
  let queue = new Queue();
  queue.enqueue(vertex);

  while (!queue.isEmpty()) {
    let vertex = queue.dequeue();
    if (this.visited[vertex]) continue;

    this.visited[vertex] = true;
    console.log(`visited: "${vertex}"`);

    let neighbors = this.edge[vertex];
    for (let i = 0; i < neighbors.length; i++) {
      queue.enqueue(neighbors[i]);
    }
  }
};

// _bfsShortestPath(): 다른 정점 간 최단 경로 비용 산출
Graph.prototype._bfsShortestPath = function (vertex) {
  let queue = new Queue();
  queue.enqueue(vertex);

  let distance = {}; // _bfsLoopVisit()에서 추가 코드
  let pre_visit = {}; // _bfsLoopVisit()에서 추가 코드
  for (let vertex in this.edge) {
    distance[vertex] = 0;
    pre_visit[vertex] = null;
  } // _bfsLoopVisit()에서 추가 코드

  while (!queue.isEmpty()) {
    let vertex = queue.dequeue();

    this.visited[vertex] = true;
    console.log(`visited: "${vertex}"`);

    let neighbors = this.edge[vertex];
    for (let i = 0; i < neighbors.length; i++) {
      if (!this.visited[neighbors[i]]) {
        distance[neighbors[i]] = distance[vertex] + 1; // _bfsLoopVisit()에서 추가 코드
        pre_visit[neighbors[i]] = vertex; // _bfsLoopVisit()에서 추가 코드
        queue.enqueue(neighbors[i]);
      }
    }
  }

  return { distance, pre_visit };
};

let graph = new Graph();
let vertices = ["A", "B", "C", "D", "E", "F", "G", "H", "I"];

for (let i = 0; i < vertices.length; i++) {
  graph.addVertex(vertices[i]);
}

graph.addEdge("A", "B");
graph.addEdge("A", "C");
graph.addEdge("A", "D");
graph.addEdge("C", "G");
graph.addEdge("D", "G");
graph.addEdge("D", "H");
graph.addEdge("B", "E");
graph.addEdge("B", "F");
graph.addEdge("E", "I");
graph.print();
console.log("");

console.log(graph._bfsShortestPath("A"));

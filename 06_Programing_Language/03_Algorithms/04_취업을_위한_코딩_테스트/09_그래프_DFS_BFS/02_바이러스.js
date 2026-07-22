/**
 * 최근 웜 바이러스가 네트워크를 통해 전파되고 있는데,
 * 한 컴퓨터라도 이 바이러스에 걸리면 컴퓨터와 연결되어 있는 모든 컴퓨터는 바이러스에 걸리게 된다.
 * 현재 PC에 설정된 네트워크 기준으로, 한 대의 PC에 바이러스가 걸렸을 때 총 몇 대의 PC가 바이러스에 걸릴지 계산하는 프로그램을 작성하라.
 * 예를 들어 7번까지의 PC가 있고,
 * 1, 2, 3, 5, 6번 PC는 1번 네트워크, 4, 7번 PC는 2번 네트워크로 구성되어 있을 때,
 * 1번 PC가 바이러스에 걸리면 총 5대의 PC가 바이러스에 걸리게 된다.
 * 입력은 PC의 총 대수와 PC와 PC가 연결된 네트워크 정보가 배열로 입력된다.
 * 웹 바이러스에 감염된 PC는 무조건 1번으로 고정될 때, 바이러스에 걸리는 총 PC의 대수를 계산하여 반환하라.
 */
function Graph() {
  this.edge = {};
  this.visited = {};
}

Graph.prototype.addVertex = function (v) {
  this.edge[v] = [];
  this.visited[v] = false;
};

Graph.prototype.addEdge = function (v1, v2) {
  // 무방향
  this.edge[v2].push(v1);
  this.edge[v1].push(v2);
};

Graph.prototype.dfs = function (vertex) {
  if (this.visited[vertex]) return;

  this.visited[vertex] = true;
  let neighbors = this.edge[vertex];
  for (let i = 0; i < neighbors.length; i++) {
    this.dfs(neighbors[i]);
  }
};

function solution(v, e_list) {
  let result = 0;

  let g = new Graph();
  // addVertex: PC 추가
  for (let i = 1; i <= v; i++) {
    g.addVertex(i);
  }

  // addEdge: 네트워크 연결 (무방향)
  for (let i = 0; i < e_list.length; i++) {
    let e = e_list[i]; // [v1, v2]
    g.addEdge(e[0], e[1]);
  }

  // dfs로 방문한 PC를 업데이트
  g.dfs(1);

  // visited[vertex] -> 방문했으면 true, 방문하지 않았으면 false
  // 몇 개가 true인지 카운팅
  for (let vertex in g.visited) {
    result += g.visited[vertex] ? 1 : 0;
  }

  return result;
}

const inputs = [
  [
    7,
    [
      [1, 2],
      [2, 3],
      [1, 5],
      [1, 5],
      [5, 2],
      [5, 6],
      [4, 7],
    ],
  ], // 5
  [
    10,
    [
      [8, 6],
      [5, 7],
      [9, 10],
      [7, 4],
      [1, 8],
      [5, 10],
      [7, 2],
    ],
  ], // 3
  [
    10,
    [
      [6, 9],
      [9, 4],
      [4, 8],
      [9, 7],
      [6, 8],
      [10, 1],
      [10, 9],
    ],
  ], // 7
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i][0], inputs[i][1]));
}

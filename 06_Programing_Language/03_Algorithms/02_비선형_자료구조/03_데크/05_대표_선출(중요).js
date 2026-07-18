/**
 * 마을에 대표를 선출해야 한다. 아래 규칙을 통해 대표를 선출하기로 했다.
 * 원탁에 둘러 앉아 시계 방향으로 1~n번까지 번호를 부여한다.
 * 주사위를 굴려 나온 숫자 m의 사람을 제외하고, 그 다음으로 나온 숫자 k만큼 이동해가며 대표 후보에서 제외시킨다.
 * 이렇게 순회하며 1명이 남을 때까지 반복해 대표를 선출하려고 한다.
 * n, m, k가 주어질 때 대표 후보에서 제외되는 번호를 출력하는 프로그램을 작성하라.
 * n, m, k는 자연수이며, 대표 후보에서 제외되는 번호를 순차적으로 배열로 반환한다.
 */
function CircularQueue(size) {
  this._array = new Array(size);
  this._size = this._array.length;
  this.length = 0;
  this.head = 0;
  this.tail = 0;
}

CircularQueue.prototype.enqueue = function (element) {
  this.length++;
  this._array[this.tail++ % this._size] = element;
};
CircularQueue.prototype.dequeue = function () {
  this.length--;
  return this._array[this.head++ % this._size];
};

function solution(n, m, k) {
  let result = [];

  // 1. 초기 원탁 배열 구현
  let cq = new CircularQueue(n);
  for (let i = 1; i <= n; i++) {
    cq.enqueue(i);
  }

  // 2. 첫 번째 제거 후보의 노드 위치로 설정
  cq.tail = cq.head = (n + m - 1) % n;

  // 3. k만큼 움직이면서 후보 제거(dequeue), 제거된 번호는 result에 추가
  let count;
  result.push(cq.dequeue());
  while (cq.length !== 0) {
    count = k - 1;
    while (count--) {
      cq.enqueue(cq.dequeue());
    }
    result.push(cq.dequeue());
  }

  return result;
}

const inputs = [
  5,
  2,
  3, // [2, 5, 4, 1, 3]
  8,
  2,
  3, // [2, 5, 8, 4, 1, 7, 3, 6]
  10,
  2,
  3, // [2, 5, 8, 1, 6, 10, 7, 4, 9, 3]
  20,
  5,
  7, // [5, 12, 19, 7, 15, 3, 13, 2, 14, 6, 18, 11, 9, 8, 10, 17, 4, 16, 20, 1]
];

for (let i = 0; i < inputs.length; i += 3) {
  console.log(`#${i + 1}`, solution(inputs[i], inputs[i + 1], inputs[i + 2]));
}

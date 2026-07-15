/**
 * 새로 구매한 프린터는 우선 순위를 고려해 프린트 결과물을 출력해주기 때문에 아래 규칙으로 동작한다.
 * 현재 등록된 프린트 문서들의 우선순위를 확인하고
 * 가장 높은 우선순위 문서가 먼저 출력되며
 * 현재 선택된 문서가 가장 높은 우선순위 문서가 아니라면, 취소되고 다시 뒤쪽 순서로 설정되어 추가된다.
 * 만약, 3개의 문서 A, B, C가 대기 상태이고, 중요도가 1, 2, 3이라면
 * "A B C -> B C A -> C A B -> C 출력 -> A B -> B A -> B 출력 -> A -> A 출력"으로 동작한다.
 * 현재 등록된 문서 우선순위를 보고, 내가 등록한 문서가 언제 출력될 지 계산하는 프로그램을 작성하라.
 * 입력은 우선순위와 0번부터 시작하는 문서 번호가 주어지고, 주어진 문서번호가 출력될 순서를 반환한다.
 */
function Queue() {
  this.array = [];
}
Queue.prototype.enqueue = function (element) {
  this.array.push(element);
};
Queue.prototype.dequeue = function () {
  return this.array.shift();
};
Queue.prototype.front = function () {
  return this.array[0];
};
Queue.prototype.max = function () {
  return Math.max(...this.array);
};

function solution(priorities, location) {
  let result = -1;
  // 1. 가장 높은 우선순위 찾기
  // 2. 가장 높은 우선순위 문서가 나오지 않으면 뒤로 보내기(dequeue, enqueue)
  // 3. 가장 높은 우선순위 문서가 나오면 출력
  // 4. 문서 번호 location을 찾을 때까지 계속 반복

  let vq = new Queue();
  let pq = new Queue();
  for (let i = 0; i < priorities.length; i++) {
    vq.enqueue(i);
    pq.enqueue(priorities[i]);
  }

  let count = 0;
  while (true) {
    // 1. 출력 부분
    if (pq.front() === pq.max()) {
      count++;
      if (vq.front() === location) {
        result = count;
        break;
      } else {
        vq.dequeue();
        pq.dequeue();
      }
    }
    // 2. 순서 변경 부분
    else {
      vq.enqueue(vq.dequeue());
      pq.enqueue(pq.dequeue());
    }
  }

  return result;
}

const inputs = [
  [3],
  0, // 1
  [3, 4, 5, 6],
  2, // 2
  [1, 1, 5, 1, 1, 1],
  0, // 5
];

for (let i = 0; i < inputs.length; i += 2) {
  console.log(`#${i / 2 + 1}`, solution(inputs[i], inputs[i + 1]));
}

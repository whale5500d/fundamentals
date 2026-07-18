/**
 * 자연수를 저장하는 데크를 만들고자 한다. 입력으로 주어진 명령어를 처리할 수 있는 프로그램을 작성하라.
 * 명령어의 종류는 총 8가지며 아래와 같으며, 명령에 따라 반환된 값을 result 배열에 넣도록 한다.
 * 1. push_front X: 자연수 X를 앞쪽에 넣는다.
 * 2. push_back X: 자연수 X를 뒤쪽에 넣는다.
 * 3. pop_front: 앞쪽 값을 제거하고 반환한다. 만약 값이 없다면 -1를 반환한다.
 * 4. pop_back: 뒤쪽 값을 제거하고 반환한다. 만약 값이 없다면 -1를 반환한다.
 * 5. empty: 큐가 비어 있다면 1, 아니면 0을 반환한다.
 * 6. size: 큐에 들어있는 자연수 개수를 반환한다.
 * 7. front: 앞쪽에 값이 있다면 해당 값을, 아니면 -1을 반환한다.
 * 8. back: 뒤쪽에 값이 있다면 해당 값을, 아니면 -1을 반환한다.
 */
function Deque() {
  this.array = [];
}
Deque.prototype.pushFront = function (element) {
  this.array.unshift(element);
};
Deque.prototype.pushBack = function (element) {
  this.array.push(element);
};
Deque.prototype.popFront = function () {
  let ret = this.array.shift();
  return ret === undefined ? -1 : ret;
};
Deque.prototype.popBack = function () {
  let ret = this.array.pop();
  return ret === undefined ? -1 : ret;
};
Deque.prototype.empty = function () {
  return this.array.length === 0 ? 1 : 0;
};
Deque.prototype.size = function () {
  return this.array.length;
};
Deque.prototype.front = function () {
  return this.array.length === 0 ? -1 : this.array[0];
};
Deque.prototype.back = function () {
  return this.array.length === 0 ? -1 : this.array[this.array.length - 1];
};

function solution(input) {
  let result = [];
  let deque = new Deque();

  for (let i = 0; i < input.length; i++) {
    let command = input[i].split(" ")[0];

    switch (command) {
      case "push_front":
        deque.pushFront(Number(input[i].split(" ")[1]));
        break;
      case "push_back":
        deque.pushBack(Number(input[i].split(" ")[1]));
        break;
      case "pop_front":
        result.push(deque.popFront());
        break;
      case "pop_back":
        result.push(deque.popBack());
        break;
      case "empty":
        result.push(deque.empty());
        break;
      case "size":
        result.push(deque.size());
        break;
      case "front":
        result.push(deque.front());
        break;
      case "back":
        result.push(deque.back());
        break;
    }
  }

  return result;
}

const inputs = [
  ["push_back 1", "push_front 2", "pop_front", "pop_back", "pop_front"], // [2, 1, -1]
  [
    "push_back 3",
    "push_front 4",
    "push_back 5",
    "push_front 6",
    "front",
    "back",
    "pop_front",
    "size",
    "empty",
  ], // [6, 5, 6, 3, 0]
  [
    "push_back 7",
    "push_front 8",
    "front",
    "back",
    "size",
    "empty",
    "pop_front",
    "pop_back",
    "pop_front",
    "size",
    "empty",
    "pop_back",
    "push_front 9",
    "empty",
    "front",
  ], // [8, 7, 2, 0, 8, 7, -1, 0, 1, -1, 0, 9]
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

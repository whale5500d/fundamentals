/**
 * 자연수를 저장하는 큐를 만들고자 한다. 입력으로 주어지는 큐 명령어를 처리하는 프로그램을 작성하라.
 * 명령어의 종류는 총 6가지며 아래와 같으며, 멸영에 따라 반환된 값을 result 배열에 넣는다.
 * 1. enqueue(x): 정수 x를 큐 뒤쪽에 추가한다.
 * 2. dequeue(): 큐 앞쪽에 있는 정수를 제거하고 그 수를 반환한다. 만약 큐에 들어있는 값이 없을 경우 -1을 반환한다.
 * 3. empty(): 큐에 들어있는 값이 없으면 1, 있으면 0을 반환한다.
 * 4. size(): 큐에 들어있는 자연수의 수를 반환한다.
 * 5. front(): 큐에 들어있는 자연수 중 가장 앞에 있는 수를 반환한다. 만약 큐에 들어있는 값이 없을 경우 -1을 반환한다.
 * 6. back(): 큐에 들어있는 자연수 중 가장 뒤에 있는 수를 반환한다. 만약 큐에 들어있는 값이 없을 경우 -1을 반환한다.
 */
function Queue() {
  this.array = [];
}

Queue.prototype.enqueue = function (element) {
  this.array.push(element);
};
Queue.prototype.dequeue = function () {
  return this.array.length === 0 ? -1 : this.array.shift();
};
Queue.prototype.empty = function () {
  return this.array.length === 0 ? 1 : 0;
};
Queue.prototype.size = function () {
  return this.array.length;
};
Queue.prototype.front = function () {
  return this.array.length === 0 ? -1 : this.array[0];
};
Queue.prototype.back = function () {
  return this.array.length === 0 ? -1 : this.array[this.array.length - 1];
};

function solution(input) {
  let result = [];
  let queue = new Queue();

  for (let i = 0; i < input.length; i++) {
    let command = input[i].split(" ")[0];

    switch (command) {
      case "enqueue":
        const element = Number(input[i].split(" ")[1]);
        queue.enqueue(element);
        break;
      case "dequeue":
        result.push(queue.dequeue());
        break;
      case "size":
        result.push(queue.size());
        break;
      case "empty":
        result.push(queue.empty());
        break;
      case "front":
        result.push(queue.front());
        break;
      case "back":
        result.push(queue.back());
        break;
    }
  }

  return result;
}

let inputs = [
  ["enqueue 1", "enqueue 2", "dequeue", "dequeue", "dequeue"], // [1, 2, -1]
  ["enqueue 3", "enqueue 4", "enqueue 5", "enqueue 6", "front", "back", "dequeue", "size", "empty"], // [3, 6, 3, 3, 0]
  [
    "enqueue 7",
    "enqueue 8",
    "front",
    "back",
    "size",
    "empty",
    "dequeue",
    "dequeue",
    "dequeue",
    "size",
    "empty",
    "dequeue",
    "enqueue 9",
    "empty",
    "front",
  ], // [7, 8, 2, 0, 7, 8, -1, 0, 1, -1, 0, 9]
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

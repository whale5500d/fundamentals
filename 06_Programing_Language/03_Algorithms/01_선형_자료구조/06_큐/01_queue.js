// Queue(): 생성자 함수로 초기 데이터 설정
export default function Queue_1(array) {
  this.array = array ? array : [];
}

// getBuffer(): 객체 내 데이터 셋 반환
Queue_1.prototype.getBuffer = function () {
  return this.array.slice();
};

// isEmpty(): 객체 내 데이터 존재 여부 확인
Queue_1.prototype.isEmpty = function () {
  return this.array.length === 0;
};

let queue = new Queue_1([1, 2, 3]);

console.log(queue); // Queue { array: [ 1, 2, 3 ] }

let data = queue.getBuffer();
console.log(data === queue.array); // false
console.log(data); // [ 1, 2, 3 ]
console.log(queue.isEmpty()); // false

console.log(Object.getOwnPropertyDescriptors(Queue_1.prototype));
/**
 * {
 *     constructor: {
 *         value: [Function: Queue],
 *         writable: true,
 *         enumerable: false,
 *         configurable: true
 *     },
 *     getBuffer: {
 *         value: [Function (anonymous)],
 *         writable: true,
 *         enumerable: true,
 *         configurable: true
 *     },
 *     isEmpty: {
 *         value: [Function (anonymous)],
 *         writable: true,
 *         enumerable: true,
 *         configurable: true
 *     }
 * }
 */

// enqueue(): 데이터 추가
Queue_1.prototype.enqueue = function (element) {
  return this.array.push(element);
};

// dequeue(): 데이터 삭제
Queue_1.prototype.dequeue = function () {
  return this.array.shift();
};

let queue2 = new Queue_1([1, 2]);
console.log(queue2); // Queue { array: [ 1, 2 ] }

queue2.enqueue(3);
queue2.enqueue(4);
console.log(queue2); // Queue { array: [ 1, 2, 3, 4 ] }

console.log(queue2.dequeue()); // 1
console.log(queue2.dequeue()); // 2
console.log(queue2); // Queue { array: [ 3, 4 ] }

// front(): 첫번째 데이터 조회
Queue_1.prototype.front = function () {
  return this.array.length > 0 ? this.array[0] : undefined;
};

// size(): 큐 내 데이터 개수 확인
Queue_1.prototype.size = function () {
  return this.array.length;
};

// clear(): 큐 비우기
Queue_1.prototype.clear = function () {
  this.array = [];
};

let queue3 = new Queue_1([1, 2, 3, 4]);

queue3.dequeue();
console.log(queue3.front()); // 2
console.log(queue3); // Queue { array: [ 2, 3, 4 ] }

console.log(queue3.size()); // 3
queue3.clear();
console.log(queue3); // Queue { array: [] }
console.log(queue3.size()); // 0

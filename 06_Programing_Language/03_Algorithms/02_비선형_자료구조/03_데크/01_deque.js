// Deque(): 초기 속성값 설정을 위한 생성자 함수
function Deque(array = []) {
  this.array = array;
}

// getBuffer(): 객체 내 데이터 출력
Deque.prototype.getBuffer = function () {
  return this.array.slice();
};

// isEmpty(): 비어 있는지 확인
Deque.prototype.isEmpty = function () {
  return this.array.length === 0;
};

let deque = new Deque([1, 2, 3]);
console.log(deque); // Deque { array: [ 1, 2, 3 ] }

let data = deque.getBuffer();
console.log(data === deque.array); // false
console.log(data); // [ 1, 2, 3 ]

console.log(deque.isEmpty()); // false

console.log(Object.getOwnPropertyDescriptors(Deque.prototype));
/**
 * {
 *  constructor: {
 *    value: [Function: Deque],
 *    writable: true,
 *    enumerable: false,
 *    configurable: true
 *  },
 *  getBuffer: {
 *    value: [Function (anonymous)],
 *    writable: true,
 *    enumerable: true,
 *    configurable: true
 *  },
 *  isEmpty: {
 *    value: [Function (anonymous)],
 *    writable: true,
 *    enumerable: true,
 *    configurable: true
 *  }
 * }
 */

/////////////////////////////
console.log("========================");
// pushFront(): 데이터 추가(앞쪽)
Deque.prototype.pushFront = function (element) {
  return this.array.unshift(element);
};

// popFront(): 데이터 삭제(앞쪽)
Deque.prototype.popFront = function () {
  return this.array.shift();
};

// pushBack(): 데이터 추가(뒤쪽)
Deque.prototype.pushBack = function (element) {
  return this.array.push(element);
};

// popBack(): 데이터 삭제(뒤쪽)
Deque.prototype.popBack = function () {
  return this.array.pop();
};

let deque2 = new Deque([1, 2, 3]);
console.log(deque2); // Deque { array: [ 1, 2, 3 ] }

deque2.pushFront(0);
deque2.pushBack(4);
console.log(deque2); // Deque { array: [ 0, 1, 2, 3, 4 ] }

console.log(deque2.popFront()); // 0
console.log(deque2.popBack()); // 4
console.log(deque2); // Deque { array: [ 1, 2, 3 ] }

/////////////////////////////
console.log("========================");
// front(): 첫번째 데이터 반환
Deque.prototype.front = function () {
  return this.array.length === 0 ? undefined : this.array[0];
};

// back(): 마지막 데이터 반환
Deque.prototype.back = function () {
  return this.array.length === 0 ? undefined : this.array[this.array.length - 1];
};

// size(): 큐의 크기 반환
Deque.prototype.size = function () {
  return this.array.length;
};

// clear(): 큐 초기화
Deque.prototype.clear = function () {
  this.array = [];
};

let deque3 = new Deque([1, 2, 3]);
console.log(deque3); // Deque { array: [ 1, 2, 3 ] }

console.log(deque3.front()); // 1
console.log(deque3.back()); // 3
console.log(deque3.size()); // 3

deque3.clear();
console.log(deque3); // Deque { array: [] }

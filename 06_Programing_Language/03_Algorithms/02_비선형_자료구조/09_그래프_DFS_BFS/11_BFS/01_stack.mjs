// Stack(): 생성자 함수로 초기 데이터 설정
function Stack(array) {
  this.array = array ? array : [];
}

// getBuffer(): 객체 내 데이터 셋 반환
Stack.prototype.getBuffer = function () {
  return this.array;
};

// isEmpty(): 객체 내 데이터 존재 여부 파악
Stack.prototype.isEmpty = function () {
  return this.array.length === 0;
};

// let stack = new Stack([1, 2, 3]);
// console.log(stack); // Stack { array: [ 1, 2, 3 ] }

// let data = stack.getBuffer();
// console.log(data === stack.array); // false, 배열 주소가 다르기 때문, slice로 값이 복사되었음을 확인할 수 있음.
// console.log(data); // [1, 2, 3]
// console.log(stack.isEmpty()); // false

// console.log(Object.getOwnPropertyDescriptors(Stack.prototype));
/**
 * {
 *     constructor: {
 *         value: [Function: Stack],
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
 *  }
 */

// push(): 데이터 추가
Stack.prototype.push = function (element) {
  return this.array.push(element);
};

// pop(): 데이터 삭제
Stack.prototype.pop = function () {
  return this.array.pop();
};

// peak(): 마지막 데이터 조회
Stack.prototype.peak = function () {
  return this.array[this.array.length - 1];
};

// size(): 스택 내 데이터 개수 확인
Stack.prototype.size = function () {
  return this.array.length;
};

let stack2 = new Stack([1, 2]);

// console.log(stack2); // Stack { array: [ 1, 2 ] }

// stack2.push(3);
// console.log(stack2); // Stack { array: [ 1, 2, 3 ] }

// stack2.pop();
// console.log(stack2.pop()); // 3
// console.log(stack2.pop()); // 2
// console.log(stack2); // Stack { array: [ 1 ] }

// console.log(stack2.peak()); // 1
// console.log(stack2.size()); // 1

// indexOf(): 데이터 위치 확인
Stack.prototype.indexOf = function (element, position = 0) {
  // case 1
  // return this.array.indexOf(element, position);
  // case 2
  for (let i = position; i < this.array.length; i++) {
    if (element === this.array[i]) return i;
  }
  return -1;
};

// includes(): 데이터 존재 여부 확인
Stack.prototype.includes = function (element, position = 0) {
  // case 1
  // return this.array.includes(element, position);
  // case 2
  for (let i = position; i < this.array.length; i++) {
    if (element === this.array[i]) return true;
  }
  return false;
};

// let stack3 = new Stack([1, 2, 3]);
// console.log(stack3.indexOf(1)); // 1
// console.log(stack3.indexOf(1, 2)); // -1
// console.log(stack3.includes(1)); // true
// console.log(stack3.includes(1, 2)); // false

export { Stack };

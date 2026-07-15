/**
 * 접시가 a, b, c, d 순으로 한쪽이 막혀 있는 세척기에 들어간다고 할 때,
 * b, a, c, d 순으로 꺼내기 위해서는 push, push, pop, pop, push, pop, push, pop 순으로 꺼내면 된다.
 * 세척기에 꺼내야 하는 접시의 순서가 주어질 때, push/pop 연산의 순서를 반환하는 프로그램을 제작하라.
 * 입력은 접시의 수가 10개를 넘기지 않는 소문자 알파벳으로 주어지며,
 * 접시 꺼내는 push/pop 연산 동작을 push -> 0, pop -> 1로 변환하여 배열로 반환한다.
 * (단, 주어진 순서로 못 꺼낼 경우, 빈 배열로 반환)
 */
if (!Array.prototype.peek) {
  Array.prototype.peek = function () {
    return this[this.length - 1];
  };
}

if (!Array.prototype.isEmpty) {
  Array.prototype.isEmpty = function () {
    return this.length === 0;
  };
}

function solution(input) {
  // 1. 접시의 순서 abcd 문자열
  // 2. 꺼내야 하는 접시, 세척기 안에 있는 알파벳 작을 때 push
  // 3. 최상단 접시와의 비교

  let stack = [];
  let result = [];
  let dish = input.split("").sort().join("");
  let dishIndex = 0;

  for (let i = 0; i < input.length; i++) {
    // 1) 세척기 안에 있는 접시와 비교
    // 세척기 안에 있는 접시가 없거나, 세척기 내 최상단 접시가 꺼내야 하는 목표 접시보다 작을 때 push
    while (stack.length === 0 || stack[stack.length - 1] < input[i]) {
      stack.push(dish[dishIndex++]);
      result.push(0); // push를 0으로 표시
    }
    // 2) 최상단 접시와의 비교
    // 세척기 내 접시가 없거나, 최상단 접시가 꺼내야 하는 목표 접시보다 클 때, 목표와 틀리므로 빈 배열 반환
    // (영문자 순서 비교)
    if (stack.isEmpty() || stack.peek() > input[i]) {
      return [];
    } else {
      // 세척기 내 최상단 접시가 꺼내야 하는 목표 접시와 같을 때, pop
      stack.pop();
      result.push(1); // pop을 1로 표시
    }
  }

  return result;
}

const inputs = [
  "bacd", // [0, 0, 1, 1, 0, 1, 0, 1]
  "dabc", // []
  "edcfgbijha", // [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1]
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

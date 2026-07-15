/**
 * 계산 수식이 주어졌을 때, 같은 짝의 괄호 위치를 찾는 프로그램을 제작하라.
 * 입력은 계산 수식으로 주어지며, 괄호의 짝 별 위치를 [시작, 끝]으로 찾아 2차원 배열 형태로 반환한다.
 * 위치 시작 값은 0으로 시작하며, 하나라도 짝이 맞지 않을 경우 빈 배열을 반환한다.
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
  let result = [];

  // 1. 괄호의 짝을 찾기 위해 스택을 사용
  let stack = [];
  for (let i = 0; i < input.length; i++) {
    // 1) 열린 괄호는 스택에 추가 (index만 추가하면 됨)
    if (input[i] === "(") {
      stack.push(i);
    }
    // 2) 닫힌 괄호는 스택에서 제거
    else if (input[i] === ")") {
      // 2-1) 스택이 비어있으면 불가능
      if (stack.isEmpty()) {
        return [];
      }
      // 2-2) 스택에서 제거하고 결과에 추가
      result.push([stack.pop(), i]);
    }
  }

  // 3) 스택이 비어있지 않으면 불가능
  if (!stack.isEmpty()) return [];

  return result;
}

const inputs = [
  "(a+b)", // [[0, 4]]
  "(a*(b+c)+d)", // [[3, 7], [0, 10]]
  "(a*(b+c)+d+(e)", // []
  "(a*(b+c)+d)+e)", // []
  "(a*(b+c)+d)+(e*(f+g))", // [[3, 7], [0, 10], [15, 19], [12, 20]]
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

/**
 * 열차가 들어갔다 나올 수 있는 플랫폼이 있다. 열차가 1번부터 3번까지 순서대로 들어온다고 했을 때,
 * 입력 순서대로 나갈 수 있는지 없는지 판단하는 프로그램을 작성하라.
 * 입력은 차량 순서 번호가 적혀 있는 배열이며, 가능 여부에 따라 true/false를 반환한다.
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
  let stack = [];

  // 2. 출발은 input의 index를 보고 바로 출발할지, 이따가 출발할 지 결정
  // 1) 진입 -> 출발 -> 진입 -> 출발 -> 진입 -> 출발
  // 2) 진입 -> 진입 -> 출발 -> 출발 -> 진입 -> 출발
  // 3) 진입 -> 진입 -> 진입 -> 출발 -> 출발 -> 출발
  let num = 0;
  for (let i = 0; i < input.length; i++) {
    // stack이 비어있거나, top이 input[i]보다 작으면 진입
    while (stack.isEmpty() || stack.peek() < input[i]) {
      stack.push(num++);
    }
    // stack의 top이 input[i]와 같으면 출발
    if (stack.peek() === input[i]) {
      stack.pop();
    }
    // 그 외의 경우는 불가능
    else return false;
  }
  return true;
}

const inputs = [
  [1, 2, 3],
  [3, 2, 1],
  [3, 1, 2],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

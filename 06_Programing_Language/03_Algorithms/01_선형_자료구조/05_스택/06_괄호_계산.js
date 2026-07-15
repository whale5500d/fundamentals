/**
 * 4개의 기호 (,), [, ]를 이용해서 만들어지는 괄호 열로, 아래 규칙으로 계산하는 프로그램을 작성하라.
 * 1. ()인 괄호 열 값은 2
 * 2. []인 괄호 열 값은 3
 * 3. (X)인 괄호 값은 2 * 값(X)로 계산
 * 4. [X]인 괄호 값은 3 * 값[X]로 계산
 * 5. XY인 괄호 값은 값(X) + 값(Y)로 계산
 *
 * 예를 들어, ()[[]]는 2 + 3 * 3 = 11이 나오며, ([])의 값은 2 * 3 = 6이다.
 * 만약 쌍이 맞지 않거나 기호 순서가 비정상적이라 올바른 괄호 셋이 만들어지지 않을 경우 0을 반환한다.
 * 입력은 4개의 기호로만 이뤄진 괄호가 문자열 형태로 주어지며, 계산을 통해 나온 정수를 반환한다.
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
  let result = 0;

  // "(" -> *2, "[" -> *3, ")" -> /2, "]" -> /3
  // () or [] 일 때, 현재 temp값을 result에 추가
  let stack = [];
  let temp = 1;
  for (let i = 0; i < input.length; i++) {
    let mark = input[i];

    switch (mark) {
      case "(":
        temp *= 2;
        stack.push(mark);
        break;
      case "[":
        temp *= 3;
        stack.push(mark);
        break;
      case ")":
        if (stack.isEmpty() || stack.peek() !== "(") {
          return 0;
        }

        if (input[i - 1] === "(") {
          result += temp;
        }

        stack.pop();
        temp /= 2;
        break;
      case "]":
        if (stack.isEmpty() || stack.peek() !== "[") {
          return 0;
        }

        if (input[i - 1] === "[") {
          result += temp;
        }

        stack.pop();
        temp /= 3;
        break;
    }
  }

  if (!stack.isEmpty()) {
    return 0;
  }
  return result;
}

// function solution(input) {
//   let result = 0;

//   // "(" -> *2, "[" -> *3, ")" -> /2, "]" -> /3
//   let stack = [];
//   let temp = 1;
//   for (let i = 0; i < input.length; i++) {
//     let mark = input[i];
//     // 1. '(' 또는 '[' 일 때, 스택에 추가
//     if (mark === "(" || mark === "[") {
//       temp *= mark === "(" ? 2 : 3;
//       stack.push(mark);
//     }
//     // 2. ')' 또는 ']' 일 때, 스택에서 제거
//     else if (mark === ")" || mark === "]") {
//       // 2-1. 괄호 쌍이 맞지 않으면 불가능
//       if ((temp % 2 === 0 && mark === ")") || (temp % 3 === 0 && mark === "]")) {
//         return 0;
//       }
//       // 2-2. 스택에서 제거하고 결과 추가
//       result += temp;
//       temp /= mark === ")" ? 2 : 3;
//       stack.pop();
//     }
//   }

//   if (temp !== 1) {
//     return 0;
//   }
//   return result;
// }

const inputs = [
  "(()[[]])", // 22
  "[][]((])", // 0
  "(()[[]])([])", // 28
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

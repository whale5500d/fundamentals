/**
 * 기린이 앞쪽만 볼 수 있는 경우, 다른 기린을 몇 마리 볼 수 있는지 총합을 구하는 프로그램을 작성하라.
 * 기린은 자신보다 작거나 같은 기린만 볼 수 있으며, 자신보다 큰 기린이 나올 경우 앞 기린들이 가려서 볼 수 없다.
 * 입력은 기린 별 키 값이 들어오며, 다른 기린을 볼 수 있는 총합을 구해 반환한다.
 * 예를 들어, 5 2 4 2 6 1 순의 기린 키가 입력으로 들어오면,
 * 1. 1번 기린은 2, 3, 4번 기린을 볼 수 있어 3마리,
 * 2. 2번 기린은 볼 수 있는 기린이 없어 0마리,
 * 3. 3번 기린은 1마리,
 * 4. 4번 기린은 0마리,
 * 5. 5번 기린은 1마리,
 * 6. 6번 기린은 0마리이므로, 총 5마리 기린이다.
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
  // result: 볼 수 있는 총합
  let result = 0;

  // 2중 반복문: 반복문을 돌면서 현재 기린보다 작거나 같은 기린을 볼 수 있는 기린의 수를 카운트
  // for (let i = 0; i < input.length; i++) {
  //   for (let j = i + 1; j < input.length; j++) {
  //     if (input[i] < input[j]) {
  //       break;
  //     } else {
  //       result++;
  //     }
  //   }
  // }

  /** 스택 사용: 반복문을 1회 돌면서
   * 1. 스택이 비어있을 때, 현재 기린을 스택에 추가
   * 2. 스택이 비어있지 않을 때
   *   2-1. 스택의 최상단 기린이 현재 기린보다 작거나 같을 때, 스택에서 기린을 제거하고 볼 수 있는 기린의 수를 카운트
   *   2-2. 스택의 최상단 기린이 현재 기린보다 클 때, 현재 기린을 스택에 추가
   */
  let stack = [];
  input.push(Number.MAX_SAFE_INTEGER);
  for (let i = 0; i < input.length; i++) {
    while (!stack.isEmpty() && stack.peek()["h"] < input[i]) {
      // 높이 계산
      result += i - stack.pop()["i"] - 1;
    }
    stack.push({ i: i, h: input[i] });
  }

  return result;
}

const inputs = [
  [10, 3, 7, 4, 12, 2], // 5
  [7, 4, 12, 1, 13, 11, 12, 6], // 6
  [20, 1, 19, 18, 15, 4, 6, 8, 3, 3], // 30
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

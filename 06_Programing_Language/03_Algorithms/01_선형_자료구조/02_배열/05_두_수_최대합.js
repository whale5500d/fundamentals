/**
 * 수열이 주어질 때, 이 중 두 개의 수를 선택하여 최대 합이 나올 수 있도록 프로그램을 제작하라.
 * 입력은 정수로 된 배열을 받고, 최대 합이 나올 수 있는 두 수를 배열 형태로 반환한다.
 * 배열로 입력되는 정수는 10 ~ 20개 사이이며, 정수의 범위는 -20 ~ +20 사이의 값이 입력된다.
 */
function solution(input) {
  let result = [];

  // 1. 배열을 돌면서 두 수를 비교해 가장 큰 값과 두 번째로 큰 값을 찾는다.
  result = input[0] > input[1] ? [input[0], input[1]] : [input[1], input[0]];
  for (let i = 2; i < input.length; i++) {
    if (input[i] > result[0]) {
      result[1] = result[0]; // value shift
      result[0] = input[i];
    } else if (input[i] > result[1]) {
      result[1] = input[i];
    }
  }

  return result;
}

const inputs = [
  [-11, 5, 18, -2, -3, 6, 4, 17, 10, 9],
  [3, 7, -14, 2, -6, 13, -20, -2, -7, 6, -17, -5, 14, -9, 19],
  [-15, -4, -8, 12, 12, -8, -8, 9, 10, 15, -2, 10, -14, 2, 13, 19, -9, 3, -18, 14],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution(inputs[i]));
}

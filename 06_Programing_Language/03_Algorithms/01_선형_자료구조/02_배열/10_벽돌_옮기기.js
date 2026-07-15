/**
 * 새로 온 알바생이 벽돌의 높이를 맞추지 않고 벽을 쌓아 놓았다.
 * 관리자를 위해 몇 개의 벽돌을 옮겨야 벽돌의 높이가 같아질 수 있을지 구해주는 프로그램을 제작하라.
 * 입력은 배열 형태의 정수이며, 같은 높이를 맞추기 위해 옮겨야 하는 벽돌의 개수를 반환한다.
 * 단, 입력으로 들어오는 배열은 남은 벽돌 없이 높이가 딱 나눠 떨어지도록 들어온다.
 */
function solution(input) {
  let result = 0;

  // 1. 평균 높이 구하기
  let sum = 0;
  for (let i = 0; i < input.length; i++) {
    sum += input[i];
  }
  let average = sum / input.length;

  // 2. 평균 높이보다 높은 벽돌의 개수 구하기
  for (let i = 0; i < input.length; i++) {
    if (input[i] > average) {
      result += input[i] - average;
    }
  }

  return result;
}

const inputs = [
  [5, 2, 4, 1, 7, 5],
  [12, 8, 10, 11, 9, 5, 8],
  [27, 14, 19, 11, 26, 25, 23, 15],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution(inputs[i]));
}

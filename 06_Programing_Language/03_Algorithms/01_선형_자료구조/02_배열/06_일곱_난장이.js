/**
 * 일터에 나갔던 난장이 9명이 와서는 모두 자기가 일곱 난장이 중 하나라고 우기고 있다.
 * 모든 난장이의 가슴에는 숫자가 표시된 배지가 있는데,
 * 다행히도 일곱 난장이의 배지에 표시된 숫자의 합이 100이라는 단서로 일곱 난장이를 분별할 수 있다.
 * 일곱 난장이를 분별하는 프로그램을 작성하라.
 * 배지 값은 100이하의 자연수로 들어오며, 일곱 난장이의 배지 값을 기존 순서대로 배열에 넣어 반환한다.
 */
function solution(input) {
  let result = [];

  // 1. input의 합산 결과 - 100 = 두 난장이의 합
  let sum = 0;
  for (let i = 0; i < input.length; i++) {
    sum += input[i];
  }
  sum -= 100;

  // 2. 두 난장이의 합이 sum과 동일한 faker를 찾는다.
  let faker = [];
  for (let i = 0; i < input.length; i++) {
    for (let j = i + 1; j < input.length; j++) {
      if (input[i] + input[j] === sum) {
        faker = [i, j];
        break;
      }
    }

    if (faker.length === 2) break;
  }

  // 3. faker를 제외한 나머지 난장이를 result에 추가한다.
  let count = 0;
  for (let i = 0; i < input.length; i++) {
    if (i !== faker[0] && i !== faker[1]) {
      result[count++] = input[i];
    }
  }

  return result;
}

const inputs = [
  [1, 5, 6, 7, 10, 12, 19, 29, 33],
  [25, 23, 11, 2, 18, 3, 28, 6, 37],
  [3, 37, 5, 36, 6, 22, 19, 2, 28],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution(inputs[i]));
}

/**
 * 네카라쿠배 대학교에서 OX 퀴즈 쇼를 진행한다.
 * 정답을 맞췄을 경우 문제당 1점을 부여하며, 연속적으로 맞출 경우 연속한 정답 개수 만큼의 가산점을 부여한다.
 * 진행자를 위해 채점표를 보고 점수를 산출해주는 프로그램을 제작하자.
 * 배열 형태의 채점 값이 1(정답), 0(오답)으로 입력되며, 점수의 합계를 반환한다.
 */
function solution(input) {
  let result = 0;

  // 1. 배열을 돌면서
  // 2. 1일 경우, 점수를 증가시켜서 점수에 합산
  // 3. 0일 경우, 점수 초기화
  let score = 0;
  let index = 0;
  while (index < input.length) {
    if (input[index] === 1) {
      score++;
      result += score;
    } else {
      score = 0;
    }
    index++;
  }

  return result;
}

const inputs = [
  [1, 0, 1, 1, 1, 0, 1, 1, 0, 0],
  [1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution(inputs[i]));
}

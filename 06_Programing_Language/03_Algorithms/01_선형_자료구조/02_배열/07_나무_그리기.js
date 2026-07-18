/**
 * 조카가 나무 그리기를 어려워 하고 있다. 어린 조카를 위해 나무를 그려주는 프로그램을 만들어주자.
 * 자연수를 높이로 입력 받고 대칭형 형태로 나무 문자열을 만들어 반환한다.
 * 각 행 별로 개행 문자(\n)를 넣어주면서 *를 찍으며 출력 값 형태로 나무를 그려준다.
 */
function solution(input) {
  let result = "\n";

  // 입력받은 높이만큼 반복문을 돌면서, 각 행에 공백을 찍고 *을 찍는다.
  for (let i = 0; i < input; i++) {
    // const total = 2 * input - 1;
    const space = input - i - 1;
    const star = 2 * i + 1;
    // result += " ".repeat(space) + "*".repeat(star) + "\n";

    // 1. 공백 처리
    for (let j = 0; j < space; j++) {
      result += " ";
    }
    // 2. 별 처리 (2n+1)
    for (let j = 0; j < star; j++) {
      result += "*";
    }
    // 3. 개행 처리
    result += "\n";
  }

  return result;
}

const inputs = [3, 5, 7];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

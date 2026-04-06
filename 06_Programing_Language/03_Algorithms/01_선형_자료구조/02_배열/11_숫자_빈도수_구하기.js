/**
 * 두 자연수 M, N을 입력 받아, M부터 N까지 각 자리수의 빈도수를 합하는 프로그램을 제작하라.
 * 예를 들어
 * M = 129, N = 137인 경우
 * 129, 130, 131, 132, 133, 134, 135, 136, 137
 * 0: 1개
 * 1: 10개
 * 2: 2개
 * 3: 9개
 * 4: 1개
 * 5: 1개
 * 6: 1개
 * 7: 1개
 * 8: 0개
 * 9: 1개
 * 결과값: [1, 10, 2, 9, 1, 1, 1, 1, 0, 1]
 */
function solution(m, n) {
  let result = Array(10).fill(0);

  // 1. m부터 n까지 반복
  for (let i = m; i <= n; i++) {
    // 2. 각 자리수를 10으로 나눈 나머지로 빈도수 계산
    let num = i;
    while (num > 0) {
      result[num % 10]++;
      num = parseInt(num / 10);
    }
  }

  return result;
}

const inputs = [129, 137, 1412, 1918, 4159, 9182];

for (let i = 0; i < inputs.length; i += 2) {
  console.log(`#${i + 1} `, solution(inputs[i], inputs[i + 1]));
}

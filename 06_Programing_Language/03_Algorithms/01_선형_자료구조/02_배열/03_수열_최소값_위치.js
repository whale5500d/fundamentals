/**
 * 수열이 주어질 때, 이 수열의 있는 수 중 최소값의 위치를 모두 출력하는 프로그램을 작성하라.
 * 입력은 자연수로 된 배열을 받고, 시작 위치는 0으로 계산하여 최소값의 위치를 배열로 반환한다.
 * 모든 수는 100이하의 자연수로 입력 받는다.
 */
// 최대한 메서드를 사용하지 않기
function solution(arr) {
  let result = [];

  // 1. 최소값이 무엇인지 찾기
  let min = Number.MAX_SAFE_INTEGER;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] < min) {
      min = arr[i];
    }
  }

  // 2. 최소값에 해당하는 index를 배열로 반환하기
  let count = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === min) {
      result[count++] = i; // count -> 0
      // count -> 1
    }
  }

  return result;
}

console.log(solution([5, 2, 10, 2])); // [1, 3]
console.log(solution([4, 5, 7, 4, 8])); // [0, 3]
console.log(solution([12, 11, 11, 16, 11, 12])); // [1, 2, 4]

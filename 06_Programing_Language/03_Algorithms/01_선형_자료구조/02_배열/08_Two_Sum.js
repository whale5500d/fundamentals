/**
 * 배열과 정수 값이 주어질 때, 배열 내 두 값을 합하여 정수 값을 만들 수 있도록 두 개의 index를 반환하는 함수를 작성하라.
 * 각 입력에 정확히 하나의 솔루션이 있다고 가정하고, 동일한 요소를 두 번 사용하지 않는다.
 * 배열의 index는 오름차순으로 정렬하여 반환한다.
 */
function solution(nums, target) {
  // (O(n^2)) 2중 For문을 돌면서 두 값을 합하여 target과 동일한 값일 때, break 실행하고 result에 index를 추가
  // for (let i = 0; i < nums.length; i++) {
  //   for (let j = i + 1; j < nums.length; j++) {
  //     if (nums[i] + nums[j] === target) {
  //       // result = [i, j];
  //       // break;
  //       return [i, j];
  //     }
  //   }
  //   // if (result.length > 0) break;
  // }

  // (O(n)) 1중 For문을 돌면서 두 값을 합하여 target과 동일한 값일 때, break 실행하고 result에 index를 추가
  let map = {};
  for (let i = 0; i < nums.length; i++) {
    const nums_j = target - nums[i];
    if (map[nums_j] !== undefined) {
      return [map[nums_j], i];
    }
    map[nums[i]] = i;
  }

  return [];
}

const inputs = [[2, 7, 11, 15], 9, [3, 2, 4], 6, [3, 3], 6];

for (let i = 0; i < inputs.length; i += 2) {
  console.log(`#${i + 1} `, solution(inputs[i], inputs[i + 1]));
}

/**
 * 오래된 창고에서 채스판과 체스 기물을 발견했다.
 * 불행히도 기물별 개수가 부족하거나 많아, 완전한 한 세트를 이루지 못한다.
 * 게임을 하기 위해 부족하거나 많은 기물의 개수를 계산하여 변환하는 프로그램을 제작하라.
 * 기물의 개수는 배열 형태로 아래와 같이 king부터 pawns 순으로 들어오며
 * 한 게임을 하기 위해 필요한 기물의 개수는 아래와 같다.
 * (순서 및 기물 필요 개수: king(1), queen(1), rook(2), bishop(2), knight(2), pawn(8))
 */
function solution(input) {
  let result = [];

  // 1. 필요한 기물의 수
  const required = [1, 1, 2, 2, 2, 8];

  // 2. 필요한 기물의 수와 비교하여 부족하거나 많은 기물의 개수 계산
  for (let i = 0; i < input.length; i++) {
    result[i] = required[i] - input[i];
  }

  return result;
}

const inputs = [
  [0, 1, 2, 2, 2, 7],
  [2, 1, 2, 1, 2, 1],
  [0, 1, 1, 5, 3, 6],
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution(inputs[i]));
}

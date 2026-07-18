/**
 * 조카를 잠재우기 위해 달팽이 모양으로 숫자를 하나씩 적어주는 프로그램이 필요하게 되었다.
 * 이를 위해 정사각형 모양의 달팽이 2차원 배열을 그려주는 함수를 작성하라.
 * 입력한 크기의 정사각형으로, 아래 그림처럼 시계방향으로 돌면서 숫자를 채워 2차원 배열을 반환한다.
 */
function solution1(input) {
  let result = [];

  // 1. 배열 초기화
  let x = 0; // 현재 x 좌표
  let y = 0; // 현재 y 좌표
  let dx = [0, 1, 0, -1]; // x 좌표 이동 방향
  let dy = [1, 0, -1, 0]; // y 좌표 이동 방향
  let dir = 0; // 현재 방향
  let count = 0; // 현재 숫자
  for (let i = 0; i < input; i++) {
    result.push(Array(input).fill(0));
  }

  // 1. 첫 번째 반복에서 오른쪽으로 이동
  // 2. 두 번째 반복에서 아래쪽으로 이동
  // 3. 세 번째 반복에서 왼쪽으로 이동
  // 4. 네 번째 반복에서 위쪽으로 이동
  // 5. 반복 횟수 증가
  for (let i = 0; i < input * input; i++) {
    result[x][y] = ++count; // 현재 숫자 채우기

    let nextX = x + dx[dir]; // 다음 x 좌표
    let nextY = y + dy[dir]; // 다음 y 좌표

    // 다음 좌표가 배열 범위를 벗어나거나 이미 숫자가 채워져 있으면, 방향 전환 후 다음 좌표 계산
    const isOutOfRange = nextX < 0 || nextX >= input || nextY < 0 || nextY >= input;
    const isAlreadyFilled = result[nextX][nextY] !== 0;
    if (isOutOfRange || isAlreadyFilled) {
      dir = (dir + 1) % 4; // 방향 전환
      nextX = x + dx[dir]; // 다음 x 좌표 계산
      nextY = y + dy[dir]; // 다음 y 좌표 계산
    }

    x = nextX; // 현재 x 좌표 업데이트
    y = nextY; // 현재 y 좌표 업데이트
  }

  return result;
}

function solution2(input) {
  let result = [];

  // 1. 2차원 배열 생성

  /** 2. 반복문 패턴 구현
   * 1) length 길이만큼 시작해서 숫자를 채워준다.
   * 2) length - 1, 방향, 2회
   * 3) length == 0일 때 반복문을 멈춘다.
   */
  let direction = 1;
  let x, y, count;
  x = y = count = 0;

  x--; // 첫 번째 숫자를 채우기 전에 좌표를 한 칸 뒤로 빼야, 첫 번째 칸을 1부터 숫자를 채울 수 있음.
  while (true) {
    for (let i = 0; i < length; i++) {
      x += direction;
      result[y][x] = ++count;
    }

    length--;

    if (length <= 0) break;

    for (let i = 0; i < length; i++) {
      y += direction;
      result[y][x] = ++count;
    }

    direction *= -1;
  }
}

const inputs = [3, 4, 5, 6];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1} `, solution1(inputs[i]));
}

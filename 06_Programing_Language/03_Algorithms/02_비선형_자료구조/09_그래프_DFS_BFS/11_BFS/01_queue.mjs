// Queue(): 생성자 함수로 초기 데이터 설정
export default function Queue(array) {
  this.array = array ? array : [];
}

// getBuffer(): 객체 내 데이터 셋 반환
Queue.prototype.getBuffer = function () {
  return this.array.slice();
};

// isEmpty(): 객체 내 데이터 존재 여부 확인
Queue.prototype.isEmpty = function () {
  return this.array.length === 0;
};

// enqueue(): 데이터 추가
Queue.prototype.enqueue = function (element) {
  return this.array.push(element);
};

// dequeue(): 데이터 삭제
Queue.prototype.dequeue = function () {
  return this.array.shift();
};

// front(): 첫번째 데이터 조회
Queue.prototype.front = function () {
  return this.array.length > 0 ? this.array[0] : undefined;
};

// size(): 큐 내 데이터 개수 확인
Queue.prototype.size = function () {
  return this.array.length;
};

// clear(): 큐 비우기
Queue.prototype.clear = function () {
  this.array = [];
};

export { Queue };

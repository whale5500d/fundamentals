export default function Queue_2(array) {
  this.array = array ? array : [];
  this.tail = array ? array.length : 0;
  this.head = 0;
}

Queue_2.prototype.enqueue = function (element) {
  // return this.array.push(element);
  return (this.array[this.tail++] = element);
};

Queue_2.prototype.dequeue = function () {
  // return this.array.shift();
  if (this.tail === this.head) return undefined;

  let element = this.array[this.head];
  delete this.array[this.head++];
  return element;
};

let queue = new Queue_2([1, 2]);
console.log(queue); // Queue { array: [ 1, 2 ], tail: 2, head: 0 }

queue.enqueue(3);
queue.enqueue(4);
console.log(queue); // Queue { array: [ 1, 2, 3, 4 ], tail: 4, head: 0 }

console.log(queue.dequeue()); // 1
console.log(queue.dequeue()); // 2
console.log(queue); // Queue { array: [ <2 empty items>, 3, 4 ], tail: 4, head: 2 }

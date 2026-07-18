import Queue_1 from "./01_queue.js";
import Queue_2 from "./02_queue_optimization.js";

let queue_1 = new Queue_1();
let queue_2 = new Queue_2();
const COUNT = 100000;

function benchmark(queue, enqueue) {
  let start = Date.now();
  for (let i = 0; i < COUNT; i++) {
    enqueue ? queue.enqueue(i) : queue.dequeue();
  }
  return Date.now() - start;
}

console.log("enqueue queue_1: " + benchmark(queue_1, true) + "ms"); // 8ms
console.log("enqueue queue_2: " + benchmark(queue_2, true) + "ms"); // 3ms

console.log("dequeue queue_1: " + benchmark(queue_1, false) + "ms"); // 876ms
console.log("dequeue queue_2: " + benchmark(queue_2, false) + "ms"); // 3ms

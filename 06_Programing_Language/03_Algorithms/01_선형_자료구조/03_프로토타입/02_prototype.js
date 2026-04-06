// 생성자 속성 정의
function Person(name, age) {
  this.name = name;
  this.age = age;
}

// prototype을 이용한 Person 메서드 정의
Person.prototype.isAdult = function () {
  return this.age > 18;
};

// 객체 생성
const person1 = new Person("John", 20);
const person2 = new Person("Jane", 15);

// 메서드 호출
console.log(person1.isAdult()); // true
console.log(person2.isAdult()); // false

// 속성 접근
console.log(person1.name); // John
console.log(person2.name); // Jane
console.log(person1.age); // 20
console.log(person2.age); // 15

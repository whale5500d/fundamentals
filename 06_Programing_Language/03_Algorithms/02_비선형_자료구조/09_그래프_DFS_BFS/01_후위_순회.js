/**
 * 컴퓨터공학과에 들어간 사촌 동생이 후위 순회를 궁금해한다.
 * 트리가 주어졌을 때, 후위 순회하며 방문했던 노드를 산출해주는 프로그램을 작성하라.
 * 입력은 노드가 추가되는 순번대로 명시된 문자열이 주어지며,
 * 트리를 만들어 갈 때 작은 값은 왼쪽으로, 큰 값은 오른쪽으로 붙여가며 만든다.
 * 왼쪽 - 오른쪽 - 루트 순으로 후위 순회하며 방문한 노드를 배열에 저장하고 그 결과를 반환한다.
 */
function Node(value) {
  this.value = value;
  this.left = null;
  this.right = null;
}

function BinaryTree() {
  this.root = null;
}

BinaryTree.prototype._insertNode = function (node, value) {
  if (node === null) {
    node = new Node(value);
  } else if (value < node.value) {
    node.left = this._insertNode(node.left, value);
  } else if (value > node.value) {
    node.right = this._insertNode(node.right, value);
  }

  return node;
};

BinaryTree.prototype.insert = function (value) {
  this.root = this._insertNode(this.root, value);
};

BinaryTree.prototype.postOrderTraverse = function (node, array) {
  if (node === null) return;

  this.postOrderTraverse(node.left, array);
  this.postOrderTraverse(node.right, array);
  array.push(node.value);
};

function solution(input) {
  let result = [];

  let tree = new BinaryTree();
  for (let i = 0; i < input.length; i++) {
    tree.insert(input[i]);
  }

  tree.postOrderTraverse(tree.root, result);

  return result;
}

const inputs = [
  "ABC", // ['C', 'B', 'A' ]
  "FBADCEGIH", // ['A', 'C', 'E', 'D', 'B', 'H', 'I', 'G', 'F']
  "CBAEDFG", // [A', 'B', 'D', 'G', 'F', 'E', 'C']
];

for (let i = 0; i < inputs.length; i++) {
  console.log(`#${i + 1}`, solution(inputs[i]));
}

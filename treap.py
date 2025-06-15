import random

class Node:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.randint(1, 10**6)
        self.left = None
        self.right = None

class Treap:
    def __init__(self, root=None):
        self.root = root
    
    def insert(self, key, priority=None):
        new_node = Node(key, priority)
        if self.root is None:
            self.root = new_node
        else:
            self.root = self._insert(self.root, new_node)
    
    def remove(self, key):
        if self.root is None:
            return
        self.root = self._remove(self.root, key)
    
    def find(self, key):
        return self._find(self.root, key)
    
    def split(self, key):
        if self.root is None:
            return Treap(), Treap()
        left, right = self._split(self.root, key)
        return Treap(left), Treap(right)
    
    def merge(self, other):
        if not isinstance(other, Treap):
            raise TypeError("Expected Treap instance")
        self.root = self._merge(self.root, other.root)
    
    def build(self, items):
        if not items:
            return
        
        nodes = [Node(key, priority) for key, priority in items]
        stack = []
        root = nodes[0]
        stack.append(root)
        
        for i in range(1, len(nodes)):
            last_popped = None
            while stack and stack[-1].priority < nodes[i].priority:
                last_popped = stack.pop()
            
            if stack:
                stack[-1].right = nodes[i]
            else:
                root = nodes[i]
            
            if last_popped:
                nodes[i].left = last_popped
            
            stack.append(nodes[i])
        
        self.root = root
    
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _insert(self, node, new_node):
        if node is None:
            return new_node
        if new_node.priority > node.priority:
            left, right = self._split(node, new_node.key)
            new_node.left = left
            new_node.right = right
            return new_node
        elif new_node.key < node.key:
            node.left = self._insert(node.left, new_node)
        else:
            node.right = self._insert(node.right, new_node)
        return node
    
    def _remove(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            return self._merge(node.left, node.right)
        return node
    
    def _find(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)
    
    def _split(self, node, key):
        if node is None:
            return (None, None)
        if node.key <= key:
            left, right = self._split(node.right, key)
            node.right = left
            return (node, right)
        else:
            left, right = self._split(node.left, key)
            node.left = right
            return (left, node)
    
    def _merge(self, left, right):
        if left is None:
            return right
        if right is None:
            return left
        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)
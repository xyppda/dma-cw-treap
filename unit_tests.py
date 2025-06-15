import unittest
from treap import Treap

class TestTreap(unittest.TestCase):
    def setUp(self):
        self.treap = Treap()
        self.test_keys = [5, 3, 7, 2, 4, 6, 8]
        for key in self.test_keys:
            self.treap.insert(key)
    
    def test_bst_property(self):
        self.assertEqual(self.treap.inorder(), sorted(self.test_keys))
    
    def test_heap_property(self):
        def check_heap(node):
            if node:
                if node.left:
                    self.assertTrue(node.priority >= node.left.priority)
                    check_heap(node.left)
                if node.right:
                    self.assertTrue(node.priority >= node.right.priority)
                    check_heap(node.right)
        
        check_heap(self.treap.root)
    
    def test_insert_remove(self):
        self.assertEqual(len(self.treap.inorder()), len(self.test_keys))
        self.treap.remove(5)
        self.assertEqual(self.treap.inorder(), [2, 3, 4, 6, 7, 8])
        self.treap.insert(1)
        self.assertEqual(self.treap.inorder(), [1, 2, 3, 4, 6, 7, 8])
        self.assertIsNotNone(self.treap.find(7))
        self.assertIsNone(self.treap.find(5))
    
    def test_split(self):
        left, right = self.treap.split(5)
        self.assertEqual(left.inorder(), [2, 3, 4, 5])
        self.assertEqual(right.inorder(), [6, 7, 8])
        self._check_heap(left.root)
        self._check_heap(right.root)
    
    def test_merge(self):
        left = Treap()
        for key in [1, 3, 5]:
            left.insert(key)
        
        right = Treap()
        for key in [7, 9, 11]:
            right.insert(key)
        
        left.merge(right)
        self.assertEqual(left.inorder(), [1, 3, 5, 7, 9, 11])
        self._check_heap(left.root)
    
    def test_build(self):
        items = [
            (1, 50),
            (2, 30),
            (3, 80),
            (4, 20),
            (5, 40)
        ]
        
        treap = Treap()
        treap.build(items)
        self.assertEqual(treap.inorder(), [1, 2, 3, 4, 5])
        self._check_heap(treap.root)
        
        root = treap.root
        self.assertEqual(root.key, 3)
        self.assertEqual(root.left.key, 1)
        self.assertEqual(root.left.right.key, 2)
        self.assertEqual(root.right.key, 5)
        self.assertEqual(root.right.left.key, 4)
    
    def test_edge_cases(self):
        empty = Treap()
        self.assertEqual(empty.inorder(), [])
        empty.remove(1)
        self.assertIsNone(empty.find(5))
        left, right = empty.split(5)
        self.assertEqual(left.inorder(), [])
        self.assertEqual(right.inorder(), [])
    
    def _check_heap(self, node):
        if node:
            if node.left:
                self.assertTrue(node.priority >= node.left.priority)
                self._check_heap(node.left)
            if node.right:
                self.assertTrue(node.priority >= node.right.priority)
                self._check_heap(node.right)

if __name__ == '__main__':
    unittest.main()

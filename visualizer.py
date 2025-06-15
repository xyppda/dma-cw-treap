import matplotlib.pyplot as plt
import networkx as nx
from treap import Treap
import random
import time

class TreapVisualizer:
    def __init__(self):
        self.treap = Treap()
        self.graph = nx.DiGraph()

    def visualize(self, title='Treap'):
        self.graph.clear()
        self._add_edges(self.treap.root)
        
        pos = self._hierarchy_pos(self.treap.root)
        labels = {node: f'{node.key}\n({node.priority})' for node in self.graph.nodes}
        
        plt.figure(figsize=(10, 6))
        nx.draw(self.graph, pos, with_labels=True, labels=labels, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
        plt.title(title)
        plt.show()
        time.sleep(1)

    def _add_edges(self, node):
        if node:
            self.graph.add_node(node)
            if node.left:
                self.graph.add_edge(node, node.left)
                self._add_edges(node.left)
            if node.right:
                self.graph.add_edge(node, node.right)
                self._add_edges(node.right)

    def _hierarchy_pos(self, node, x=0, y=0, dx=1.0):
        pos = {}
        def recurse(node, x, y, dx):
            if node is None:
                return
            pos[node] = (x, y)
            if node.left:
                recurse(node.left, x - dx, y - 1, dx / 2)
            if node.right:
                recurse(node.right, x + dx, y - 1, dx / 2)
        recurse(node, x, y, dx)
        return pos

    def demo(self):
        keys = [5, 3, 7, 2, 4, 6, 8]
        random.seed(42)
        for key in keys:
            self.treap.insert(key)
            self.visualize(f'After insert {key}')

        self.treap.remove(5)
        self.visualize('After remove 5')

        self.treap.insert(1)
        self.visualize('After insert 1')

        left, right = self.treap.split(4)
        self._draw_split(left.root, right.root)

    def _draw_split(self, left_root, right_root):
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        for ax, root, title in zip(axes, [left_root, right_root], ['Left Split', 'Right Split']):
            g = nx.DiGraph()
            def add_edges(node):
                if node:
                    g.add_node(node)
                    if node.left:
                        g.add_edge(node, node.left)
                        add_edges(node.left)
                    if node.right:
                        g.add_edge(node, node.right)
                        add_edges(node.right)
            add_edges(root)

            pos = self._hierarchy_pos(root)
            labels = {node: f'{node.key}\n({node.priority})' for node in g.nodes}
            nx.draw(g, pos, with_labels=True, labels=labels, node_size=2000, node_color='lightgreen', font_size=10, font_weight='bold', ax=ax)
            ax.set_title(title)
        plt.show()


if __name__ == '__main__':
    viz = TreapVisualizer()
    viz.demo()

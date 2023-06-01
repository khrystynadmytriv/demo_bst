"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    # def add(self, item):
    #     """Adds item to the tree."""

    #     # Helper function to search for item's position
    #     def recurse(node):
    #         # New item is less, go left until spot is found
    #         if item < node.data:
    #             if node.left is None:
    #                 node.left = BSTNode(item)
    #             else:
    #                 recurse(node.left)
    #         # New item is greater or equal,
    #         # go right until spot is found
    #         elif node.right is None:
    #             node.right = BSTNode(item)
    #         else:
    #             recurse(node.right)
    #             # End of recurse

    #     # Tree is empty, so new item goes at the root
    #     if self.isEmpty():
    #         self._root = BSTNode(item)
    #     # Otherwise, search for the item's spot
    #     else:
    #         recurse(self._root)
    #     self._size += 1
    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
        else:
            current = self._root
            added = False
            
            while not added:
                if item < current.data:
                    if current.left is None:
                        current.left = BSTNode(item)
                        added = True
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = BSTNode(item)
                        added = True
                    else:
                        current = current.right

        self._size += 1




    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left is None \
                and not currentnode.right is None:
            liftmaxinleftsubtreetotop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 +max(height1(top.left),height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() < (2*log(self._size + 1, 2)) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        return lst[lst.index(low):lst.index(high)+1]

    # def rebalance(self):
    #     '''
    #     Rebalances the tree.
    #     :return:
    #     '''
    #     def recurse(lst):
    #         node = lst[len(lst)//2]
    #         self.add(node)
    #         lst.remove(node)
    #         if len(lst) != 0:
    #             recurse(lst)
    #     lst = list(self.inorder())
    #     self.clear()
    #     recurse(lst)
    def rebalance(self):
        """
        Rebalances the tree.
        """
        nodes = list(self.inorder())
        self.clear()
        self._build_balanced_tree(nodes)

    def _build_balanced_tree(self, nodes):
        """
        Helper method to build a balanced tree from a sorted list of nodes.
        """
        if not nodes:
            return

        mid = len(nodes) // 2
        self.add(nodes[mid])

        self._build_balanced_tree(nodes[:mid])
        self._build_balanced_tree(nodes[mid+1:])
# res = []
#         def make_rebalance_list(lst):
#             res.append(lst[len(lst) // 2])
#             if len(lst[:len(lst) // 2]) // 2 != 0:
#                 return make_rebalance_list(lst[:len(lst) // 2]), make_rebalance_list(lst[len(lst) // 2 + 1:])
#         lst = [item for item in self]
#         lst.sort()
#         make_rebalance_list(lst)

        # for i in lst:
        #     if i not in res:
        #         res.append(i)
        # self.clear()
        # for item in res:
        #     self.add(item)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = []
        for i in self.inorder():
            if i>item:
                res.append(i)
        if not res:
            return None
        return min(res)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = []
        for i in self.inorder():
            if i<item:
                res.append(i)
        if not res:
            return None
        return max(res)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path,'r',encoding='utf-8') as file:
            words = [word.strip() for word in file]

        sorted_words = sorted(words)
        random_words = sorted(words, key=lambda x: hash(x))

        print("Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику (пошук у списку слів з використанням методів вбудованого типу list).")
        start_time = time.time()
        for i in range(10000):
            _ = sorted_words.index(random_words[i])
        end_time = time.time()
        print(f"Час пошуку: {end_time - start_time:.6f} сек")

        bst = LinkedBST()
        for word in sorted_words:
            bst.add(word)

        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку. Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника, який впорядкований за абеткою.")
        start_time = time.time()
        for i in range(1000):
            _ = bst.find(random_words[i])
        end_time = time.time()
        print(f"Час пошуку: {end_time - start_time:.6f} сек")

        random_bst = LinkedBST()
        for word in random_words:
            random_bst.add(word)
        
        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку. Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника, який не впорядкований за абеткою (слова у дерево додаються випадковим чином).")
        start_time = time.time()
        for i in range(10000):
            _ = random_bst.find(random_words[i])
        end_time = time.time()
        print(f"Час пошуку: {end_time - start_time:.6f} сек")
    
        random_bst.rebalance()
        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку після його балансування.")
        start_time = time.time()
        for i in range(10000):
            _ = random_bst.find(random_words[i])
        end_time = time.time()
        print(f"Час пошуку: {end_time - start_time:.6f} сек")

bst = LinkedBST()
bst.demo_bst('words.txt')
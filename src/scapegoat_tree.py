""" Author: Indiana
    Date: 7 Dec 2022

    Implements class for scapegoat trees.
"""

from math import floor, log

class Node():
    def __init__(self, key):
        """ Make new leaf node,
            given key.
        """
        self.key = key
        self.left = None
        self.right = None


class ScapegoatTree():
    def __init__(self, alpha):
        """ Make new scapegoat tree,
            given alpha value.
        """
        self.alpha = alpha
        self.root = None
        self.size = 0
        self.max_size = 0


    def __subtree_size(self, subroot):
        """ Return size of subtree,
            given subroot node.
        """
        # base:
        if subroot is None:
            return 0
        # recurse:
        # count root + left subtree + right subtree
        return (1 +
                self.__subtree_size(subroot.left) +
                self.__subtree_size(subroot.right))


    def __alpha_weight_balanced(self, child_size_1, child_size_2):
        """ Return whether a node is alpha-weight-balanced,
            given the sizes of the subtrees rooted at its children.
        """
        node_size = 1 + child_size_1 + child_size_2
        return (child_size_1 <= self.alpha*node_size and
                child_size_2 <= self.alpha*node_size)


    def __scapegoat(self, leaf, ancestor_trail):
        """ Return scapegoat node, its parent, and 
            the direction of the scapegoat relative to its parent,
            given the leaf node from which a scapegoat should be found
            and a list of tuples containing ancestors from the root to the leaf
            and the direction of the ancestor relative to its parent.
        """
        # the child is initally the leaf
        child = leaf
        child_size = 1
        # ancestor closest to leaf ... root
        for i in range(len(ancestor_trail)-1, -1, -1):
            # ancestor of child
            ancestor = ancestor_trail[i][0]
            # direction of ancestor relative to its parent
            direction = ancestor_trail[i][1]
            # size of sibling of child
            sibling_size = (self.__subtree_size(ancestor.left) if child is ancestor.right
                            else self.__subtree_size(ancestor.right))
            
            # check if ancestor is alpha-weight-balanced
            if not self.__alpha_weight_balanced(child_size, sibling_size):
                if ancestor is self.root:
                    return ancestor, None, ''
                else:
                    ancestor_parent = ancestor_trail[i-1][0]
                    return ancestor, ancestor_parent, direction

            # update child and child size for next ancestor
            child = ancestor
            child_size += sibling_size + 1
        
        # not finding a scapegoat contradicts the paper's proofs!
        # this should never happen!
        raise Exception(f'No ancestral scapegoat was found from the new leaf {leaf.key}!')


    def __inorder_helper(self, subroot, aux_array):
        """ Helper for __inorder
        """
        # base:
        if subroot is None:
            return None
        # recurse:
        # traverse in order and append nodes to aux array
        self.__inorder_helper(subroot.left, aux_array)
        aux_array.append(subroot)
        self.__inorder_helper(subroot.right, aux_array)

        return aux_array


    def __inorder(self, subroot):
        """ Return a list of nodes ordered by inorder traversal,
            given subroot node.
        """
        # call helper
        return self.__inorder_helper(subroot, [])


    def __balanced_subtree_helper(self, nodes, start, end):
        """ Helper for __balanced_subtree
        """
        # base:
        if start > end:
            return None
        # recurse:
        # set subroot
        mid = (start + end) // 2
        subroot = nodes[mid]
        # point subroot to children
        subroot.left = self.__balanced_subtree_helper(nodes, start, mid-1)
        subroot.right = self.__balanced_subtree_helper(nodes, mid+1, end)

        return subroot


    def __balanced_subtree(self, nodes):
        """ Return root of balanced tree,
            given list of nodes.
        """
        # call helper
        return self.__balanced_subtree_helper(nodes, 0, len(nodes)-1)


    def search(self, key, return_parent=False):
        """ Return highest node with given key---
            optionally return parent of node
            and direction of node relative to parent, too.
        """
        # start at root
        node = self.root
        parent = None
        direction = ''
        # traverse
        while node is not None:
            # found
            if key == node.key:
                return (node if not return_parent
                        else node, parent, direction)
            # go left
            elif key < node.key:
                parent = node
                node = node.left
                direction = 'l'
            # go right
            elif key > node.key:
                parent = node
                node = node.right
                direction = 'r'

        # not found
        return (None if not return_parent
                else None, None, '')

    
    def insert(self, key):
        """ Insert new node with given key.
        """
        # update tree counters
        self.size += 1
        self.max_size = max(self.size, self.max_size)

        # insert as root if tree is empty
        if self.root is None:
            self.root = Node(key)
            return None

        # else go down and insert
        node = self.root
        node_depth = 0
        # keep track of path
        ancestor_trail = [(self.root, '')]
        while True:
            # go left
            if key < node.key and node.left is not None:
                node = node.left
                node_depth += 1
                ancestor_trail.append((node, 'l'))
            # go right
            elif key >= node.key and node.right is not None:
                node = node.right
                node_depth += 1
                ancestor_trail.append((node, 'r'))
            # insert left
            elif key < node.key:
                node.left = Node(key)
                node = node.left
                node_depth += 1
                break
            # insert right
            elif key >= node.key:
                node.right = Node(key)
                node = node.right
                node_depth += 1
                break

        # rebalance if new node is deep
        if node_depth > floor(log(self.size, 1/self.alpha)):
            # find scapegoat
            scapegoat, parent, direction = self.__scapegoat(node, ancestor_trail)
            # nodes of subtree rooted at scapegoat inorder
            subtree_nodes = self.__inorder(scapegoat)
            # root of balanced subtree
            balanced_subroot = self.__balanced_subtree(subtree_nodes)

            # point parent of scapegoat to root of balanced subtree
            if scapegoat is self.root:
                self.root = balanced_subroot
            # to left child
            elif direction == 'l':
                parent.left = balanced_subroot
            # to right child
            elif direction == 'r':
                parent.right = balanced_subroot


    def delete(self, key):
        """ Delete highest node with given key.
        """
        # search for node
        node, parent, direction = self.search(key, return_parent=True)

        # do nothing if not found
        if node is None:
            return None
        
        # else delete it
        # leaf:
        if node.left is None and node.right is None:
            if node is self.root:
                self.root = None
            elif direction == 'l':
                parent.left = None
            elif direction == 'r':
                parent.right = None

        # only left child:
        if node.right is None:
            if node is self.root:
                self.root = node.left
            elif direction == 'l':
                parent.left = node.left
            elif direction == 'r':
                parent.right = node.left

        # only right child:
        if node.left is None:
            if node is self.root:
                self.root = node.right
            elif direction == 'l':
                parent.left = node.right
            elif direction == 'r':
                parent.right = node.right

        # two children:
        else:
            # find node with largest key in left subtree
            swap = node.left
            swap_parent = node
            # direction of swap relative to its parent
            direction = 'l'
            # go far right in left subtree
            while swap.right is not None:
                swap_parent = swap
                swap = swap.right
                direction = 'r'
            
            # swap keys and splice out swap
            node.key = swap.key
            if direction == 'l':
                swap_parent.left = swap.left
            elif direction == 'r':
                swap_parent.right = swap.left

        # update tree counter
        self.size -= 1

        # rebalance entire tree if needed
        if self.size < self.alpha*self.max_size:
            # all nodes inorder
            tree_nodes = self.__inorder(self.root)
            # root of balanced tree
            balanced_root = self.__balanced_subtree(tree_nodes)
            # set root to balanced root
            self.root = balanced_root

            # update tree max size
            self.max_size = self.size

    
    def valid(self):
        """ Raise exception if the tree isn't
            a valid binary search tree.
        """
        keys = [node.key for node in self.__inorder(self.root)]
        if keys != sorted(keys):
            raise Exception('Invalid binary search tree!')
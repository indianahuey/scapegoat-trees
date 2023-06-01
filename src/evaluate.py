""" Author: Indiana
    Date:   8 Dec 2022

    Evaluate insertion times of scapegoat trees and red-black trees.
"""

import timeit
from random import randint
from scapegoat_tree import *
from red_black_tree import *


def evaluate(tree_type, keys, alpha=None):
    """ Print milliseconds taken to insert 250k, 500k, and 1M keys.
    """
    # init tree
    if tree_type == 'redblack':
        tree = RedBlackTree()
    elif tree_type == 'scapegoat':
        tree = ScapegoatTree(alpha)
    else:
        raise Exception('Invalid tree type.')

    # start timer
    start = timeit.default_timer()

    # insert keys
    for k in keys[:250000]:
        tree.insert(k)
    print((timeit.default_timer() - start)*1000, end='\t')

    for k in keys[250000:500000]:
        tree.insert(k)
    print((timeit.default_timer() - start)*1000, end='\t')

    for k in keys[500000:1000000]:
        tree.insert(k)
    print((timeit.default_timer() - start)*1000, end='\n')


def generate_keys():
    """ Return list of 1M random integers,
        ranging from 0 to 1M. 
    """
    return [randint(0, 1000000) for _ in range(1000000)]


def main():
    """ Run evaluations.
    """
    num_runs = 30

    # evaluate red-black trees
    print('Red-black tree:')
    for run in range(num_runs):
        evaluate('redblack', generate_keys())

    # evaluate scapegoat trees
    for alpha in [0.5, 0.6, 0.7, 0.8, 0.9]:
        print(f'Scapegoat tree, alpha={alpha}:')
        for run in range(num_runs):
            evaluate('scapegoat', generate_keys(), alpha)


if __name__ == '__main__':
    main()

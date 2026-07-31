"""Homework 4: Data Abstraction and Trees"""

from copy import deepcopy
from ADT import tree, label, branches, is_leaf, print_tree, copy_tree

#####################
# Required Problems #
#####################


# Problem 1.1
def fn_empty():
    """Return an empty function.

    >>> fn_empty()
    []
    """
    return []


def fn_remap(fn, x, y):
    """Return a new function that is the same as fn except that it maps x to y.

    >>> f = fn_remap(fn_empty(), 1, 2)
    >>> f
    [[1, 2]]
    >>> fn_remap(f, 1, 3)
    [[1, 3]]
    >>> fn_remap(f, 2, 3)
    [[1, 2], [2, 3]]
    """
    check = 0
    f0 = deepcopy(fn)
    if f0 == fn_empty():
        return [[x,y]]
    else:
        for i in f0:
            if i[0] == x:
                i[1] = y
                check = 1
        if check == 0:
            f0.append([x,y])
    return f0
        


def fn_domain(fn):
    """Return a sorted list of all the inputs (domain) of fn.
    Note that if fn maps x to None, then x is not in the domain of fn.

    >>> fn_domain(fn_remap(fn_remap(fn_empty(), 1, 2), 2, 3))
    [1, 2]
    >>> fn_domain(fn_remap(fn_remap(fn_empty(), 2, 3), 1, 2))
    [1, 2]
    >>> fn_domain(fn_empty())
    []
    >>> fn_domain(fn_remap(fn_empty(), 1, None))
    []
    """
    l1 = []
    for i in fn:
        if i[1] != None:
            if i[0] not in l1:
                l1.append(i[0])
    return sorted(l1)
        
    


def fn_call(fn, x):
    """Return the result of applying fn to x.
    If fn does not map x to a value, return None.

    >>> fn_call(fn_remap(fn_empty(), 1, 2), 1)
    2
    >>> fn_call(fn_remap(fn_remap(fn_empty(), 1, 2), 2, 3), 2)
    3
    >>> fn_call(fn_remap(fn_remap(fn_empty(), 1, 2), 2, 3), 1)
    2
    >>> fn_call(fn_empty(), 1) is None
    True
    """
    for i in fn:
        if i[0] == x:
            return i[1]
    return None


# Problem 1.2
def fn_ext(fn1, fn2):
    """Return whether fn1 and fn2 represent the same function.
    Two functions are the same if and only if they have the same domain
    and output the same value for each input in the domain.

    >>> f = fn_remap(fn_empty(), 1, 2)
    >>> g = fn_remap(fn_empty(), 2, 3)
    >>> fn_ext(f, g)
    False
    >>> fn_ext(fn_remap(f, 2, 3), g)
    False
    >>> fn_ext(fn_remap(f, 2, 3), fn_remap(g, 1, 2))
    True
    """
    if fn_domain(fn1) != fn_domain(fn2):
        return False
    for i in fn_domain(fn1):
        if fn_call(fn1,i) != fn_call(fn2,i):
            return False
    return True


def fn_compose(fn1, fn2):
    """Return a new function that is the composition of fn1 and fn2.
    The composition of two functions fn1 and fn2 is a function fn such that
    fn(x) = fn1(fn2(x)) for every x in the domain of fn2.

    >>> f = fn_remap(fn_empty(), 2, 3)
    >>> g = fn_remap(fn_empty(), 1, 2)
    >>> h = fn_compose(f, g)
    >>> fn_call(h, 1)
    3
    >>> fn_call(h, 2) is None
    True
    """
    l = fn_empty()
    for i in fn_domain(fn2):
            l = fn_remap(l,i,fn_call(fn1,fn_call(fn2,i)))
    return l


def fn_inverse(fn):
    """Return a new function that is the inverse of fn.
    The inverse of a function fn is a function fn_inv such that
    fn_inv(y) = x if and only if fn(x) = y.
    If fn is not invertible, return None.

    >>> f = fn_remap(fn_remap(fn_empty(), 1, 2), 2, 3)
    >>> fn_call(fn_inverse(f), 3)
    2
    >>> g = fn_remap(fn_remap(fn_empty(), 1, 2), 2, 2)
    >>> fn_inverse(g) is None
    True
    """
    l1 = []
    result = fn_empty()
    for i in fn_domain(fn):
        if fn_call(fn,i) in l1:
            return None
        l1.append(fn_call(fn,i))
        result = fn_remap(result,fn_call(fn,i),i)
    return result
    


# Problem 2.1
def add_trees(t1, t2):
    """
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    
    """
    c1 = deepcopy(t1)
    c2 = deepcopy(t2)
    if is_leaf(c1) and is_leaf(c2):
        return tree(label(c1)+label(c2))
    if is_leaf(c1):
        return tree(label(c1)+label(c2),branches(c2))
    if is_leaf(c2):
        return tree(label(c1)+label(c2),branches(c1))
    new_branches = []
    if len(branches(c1)) < len(branches(c2)):
        c1,c2=c2,c1
    for index,branch in enumerate(branches(c1)):
        if index < len(branches(c2)):
            new_branches += [add_trees(branch,branches(c2)[index])]
        else:
            new_branches += [branch]

    return tree(label(c1)+label(c2),new_branches)

        


# Problem 2.2
def bigpath(t, n):
    """Return the number of rooted paths in t that have a sum larger or equal to n.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> bigpath(t, 3)
    4
    >>> bigpath(t, 6)
    2
    >>> bigpath(t, 9)
    1
    """
    if is_leaf(t):
        if label(t) >= n:
            return 1
        else:
            return 0
    else:
        result = 1 if label(t) >= n else 0
        for i in branches(t):
            result += bigpath(i,n-label(t))
        return result 



# Problem 2.3
def bigger_path(t, n):
    """Return the number of general rooted paths in t that have a sum larger or equal to n.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> bigger_path(t, 3)
    9
    >>> bigger_path(t, 6)
    4
    >>> bigger_path(t, 9)
    1
    """
    if is_leaf(t):
        if label(t) >= n:
            return 1
        else:
            return 0
    else:
        result = bigpath(t,n)
        for i in branches(t):
            result += bigger_path(i,n)
        return result


# Problem 2.4
def has_path(t, word):
    """Return whether there is a rooted path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path(greetings, 'h')
    True
    >>> has_path(greetings, 'i')
    False
    >>> has_path(greetings, 'hi')
    True
    >>> has_path(greetings, 'hello')
    True
    >>> has_path(greetings, 'hey')
    True
    >>> has_path(greetings, 'bye')
    False
    """
    assert len(word) > 0, "no path for empty word."
    def func(t):
        rootlist = [label(t)]
        if not is_leaf(t):
            for i in branches(t):
                for j in func(i):
                    rootlist.append(label(t)+j)   
        return rootlist
    return word in func(t)


##########################
# Just for fun Questions #
##########################


# Problem 3
def fold_tree(t, base_func, merge_func):
    """Fold tree into a value according to base_func and merge_func"""
    "*** YOUR CODE HERE ***"


def count_leaves(t):
    """Count the leaves of a tree.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> count_leaves(t)
    3
    """
    return fold_tree(t, "YOUR EXPRESSION HERE", "YOUR EXPRESSION HERE")


def label_sum(t):
    """Sum up the labels of all nodes in a tree.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> label_sum(t)
    15
    """
    return fold_tree(t, "YOUR EXPRESSION HERE", "YOUR EXPRESSION HERE")


def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> preorder(t)
    [1, 2, 3, 4, 5]
    """
    return fold_tree(t, "YOUR EXPRESSION HERE", "YOUR EXPRESSION HERE")


def has_path_fold(t, word):
    """Return whether there is a path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path_fold(greetings, 'h')
    True
    >>> has_path_fold(greetings, 'i')
    False
    >>> has_path_fold(greetings, 'hi')
    True
    >>> has_path_fold(greetings, 'hello')
    True
    >>> has_path_fold(greetings, 'hey')
    True
    >>> has_path_fold(greetings, 'bye')
    False
    """
    assert len(word) > 0, "no path for empty word."

    def base_func(l):
        return "YOUR EXPRESSION HERE"
    def merge_func(l, bs):
        return "YOUR EXPRESSION HERE"

    return fold_tree(t, base_func, merge_func)(word)

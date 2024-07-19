from z3 import *
import math
from fractions import Fraction
from collections import defaultdict
import itertools
import sys


def det_sign(n):
    return -1 if n % 2 else 1


def minor(Mat, rows, cols):
    assert len(rows) == len(cols)
    return [[Mat[r][c] for c in cols] for r in rows]


def det(Mat):
    if 1 == len(Mat):
        return Mat[0][0]
    res = 0
    rows = [i + 1 for i in range(len(Mat) - 1)]
    cols = rows.copy()
    for i in range(len(Mat)):
        res += det_sign(i) * Mat[i][0] * det(minor(Mat, rows, cols))
        if i < len(rows):
            rows[i] -= 1
    return res

def D(l, mat):
    rows = [i for i in range(len(l))]
    return det(minor(mat, rows, l))


def solve(rows, cols, bases, edges, evaluate=True):
    """Returns a tableau of the specified size, of the base {x_0, ..., x_rows-1},
    s.t. the pivot graph contains a specified subgraph.
    Each edge is represented as a base B, given as a list of indices, and an index i, which specifies that in 
    Tab(B), -c_i < 0. This means a pivot can be performed from B to any feasible basis, by swapping a variable in B for x_i.
    Bases is a list of bases that must be feasible. 
    This function either halts, returns an LP that has the specified subgraph, or
    states that the requested LP doesn't exist
    """
    s = Solver()
    A = [[Real(f"A_{i}_{j}") for j in range(cols)] for i in range(rows-1)]
    A.append([Real(f"c_{i}") for i in range(cols)])
    for i, j in itertools.product(range(rows), range(rows - 1)):
        if i == j:
            A[i][j] = 1
            A[-1][j] = 0
        else:
            A[i][j] = 0

    for x in bases:
        s.add(D(x, A) > 0)

    for x in edges:
        s.add(D(x, A) < 0)

    if s.check() == unsat:
        return None
        return s
    else:
        s = s.model()
        if not evaluate:
            return s
        return [
            [s.evaluate(x).as_fraction() if type(x) != int else x for x in r] 
                for r in A
        ]


def get_adj(LP):
    """builds an adjacency list from a given tableau"""
    cols = len(LP[0])
    rows = len(LP)
    gr = defaultdict(lambda: ([]))
    for b in itertools.product(range(cols), repeat=rows):
        if D(b, LP) < 0 and D(b[:-1], LP):
            for i in range(rows - 1):
                base = b[:i] + (b[-1],) + b[i + 1 : -1]
                if D(base, LP) > 0:
                    gr[tuple(b[:-1])] = gr[tuple(b[:-1])] + [base]
    return gr

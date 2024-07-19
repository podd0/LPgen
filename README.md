# LPgen
Generate a linear program with given pivots.
Based on [Systematic construction of examples for cycling in the simplex method](https://www.sciencedirect.com/science/article/abs/pii/S0305054805000493), by Peter Zörnig.

## Usage example

To build an LP with a cycle of length 6:
```python
solve(rows=3, cols=6, bases=[[0, 1], [2, 1], [2, 3], [4, 3], [4, 5], [0, 5]], edges=[[0, 1, 2], [2, 1, 3], [2, 3, 4], [4, 3, 5], [4, 5, 0], [0, 5, 1]])
```
bases is a list of the feasible bases (order of variables matters).
each edge can be seen as (B | j) and means that in B, the jth coefficient of the objective function is negative (for example an edge `[0, 1, 2]` means that in the base `[0, 1]` you can pivot on column 2).

This returns a z3 model of a tableau of the LP or returns `None` if it doesn't exist.

The first row-1 rows of the tableau are the list of coefficients of $A$, the last row contains the coefficients of the objective row. $b = 0$ and so it is not returned

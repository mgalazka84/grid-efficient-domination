# Supplement S1. Constructing and verifying a dominating set

This software accompanies *A random-access construction of 1,2-efficient dominating sets in grids with an even side*, by Marek Gałązka and Hanna Wdowicka. The implementation and the finite tests use the Python standard library and were tested with Python 3.12.14. A separate solver input checks the two symbolic claims.

## Reproduce the example

Run the commands in the directory containing both Python files.

~~~sh
python3 grid_domination.py 6 10
python3 grid_domination.py 6 10 --cell 1 1
python3 grid_domination.py 6 10 --cell 1 2
~~~

In the bitmap, 1 denotes a marked vertex. Coordinates are one-based and follow the order row, column. The two single-cell commands return 1 and 0. If the number of rows is odd and the number of columns is even, the implementation transposes the construction internally. The input must have at least one even side.

## Verification

~~~sh
python3 verify.py
~~~

The default run checks both seeds against a column recurrence generated from the requirement of exactly one marked open neighbour on the strip. It checks the number of marks in each row of one period, and both boundary inclusions for every length residue at each even width from 2 through 200. It then directly counts neighbours at every vertex of each of the 768 ordered rectangles with both dimensions at most 32 and an even side. A final reproducible test queries cells and their neighbours in 1,024 large grids.

The limits can be adjusted with the --width and --side options. The mathematical proof is in the manuscript.

## Symbolic checks for arbitrary width

The file symbolic.smt2 uses the standard SMT-LIB language and quantifier-free linear integer arithmetic. Run it with Z3, for example with version 4.13.3.

~~~sh
z3 symbolic.smt2
~~~

The expected output is two lines containing “unsat”. The first query asks for an even width and a cell in a representative strip block at which the four open-neighbour indicators fail to sum to one. It includes both boundary rows and the horizontal join by reflecting coordinates as required. The second asks for a row and a length residue that violate either of the two cut inclusions in the manuscript. The width has no upper bound in either query.

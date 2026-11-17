"""Check the strip formula against the forced recurrence and the finite graph definition."""

import argparse
from random import Random

from grid_domination import Grid, choose_cut, strip_member


def require(condition, details):
    if not condition:
        raise AssertionError(details)


def recurrence_columns(width, seed):
    """Generate columns by imposing exactly one marked open neighbour at every cell."""
    word = "1100" if seed == "A" else "1001"
    first = sum(1 << i for i in range(width) if word[i % 4] == "1")
    full = (1 << width) - 1
    previous, current = 0, first
    columns = []
    for index in range(2 * (width + 1)):
        columns.append(previous)
        above, below = (current << 1) & full, current >> 1
        require(not ((previous & above) | (previous & below) | (above & below)),
                ("two existing neighbours", width, seed, index))
        following = full ^ (previous | above | below)
        previous, current = current, following
    require((previous, current) == (0, first), ("period", width, seed))
    return columns


def check_strip(width):
    period = 2 * (width + 1)
    patterns = {}
    for seed in ("A", "B"):
        columns = recurrence_columns(width, seed)
        patterns[seed] = columns
        row_counts = [sum((column >> i) & 1 for column in columns) for i in range(width)]
        require(row_counts == [row if row % 2 == 0 else width + 1 - row
                               for row in range(1, width + 1)],
                ("row counts over one period", width, seed))
        for column, reference in enumerate(columns):
            formula = sum(1 << (i-1) for i in range(1, width + 1)
                          if strip_member(width, seed, i, column))
            require(formula == reference, ("strip entry", width, seed, column))
    for length in range(1, period + 1):
        seed, left = choose_cut(width, length)
        cols = patterns[seed]
        right = left + length
        require(not cols[left % period] & ~cols[(left + 1) % period],
                ("left cut", width, length, seed, left))
        require(not cols[(right + 1) % period] & ~cols[right % period],
                ("right cut", width, length, seed, right))


def check_rectangle(rows, columns):
    grid = Grid(rows, columns)
    chosen = {(i, j) for i in range(1, rows + 1) for j in range(1, columns + 1)
              if grid.contains(i, j)}
    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            count = sum(v in chosen for v in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)))
            require(count == 1 or (count == 0 and (i, j) in chosen),
                    ("finite grid", rows, columns, i, j, count))


def check_large_queries():
    # Mix corners, boundaries and interior cells on grids too large to materialise.
    rng = Random(20261117)
    for k in range(1024):
        rows = 2 * rng.randrange(1, 10**17)
        columns = rng.randrange(1, 10**18)
        if k % 2:
            rows, columns = columns, rows
        grid = Grid(rows, columns)
        i = rng.choice((1, rows, rng.randrange(1, rows + 1)))
        j = rng.choice((1, columns, rng.randrange(1, columns + 1)))
        neighbours = ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
        count = sum(grid.contains(a, b) for a, b in neighbours
                    if 1 <= a <= rows and 1 <= b <= columns)
        require(count == 1 or (count == 0 and grid.contains(i, j)),
                ("large grid", rows, columns, i, j, count))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=200,
                        help="largest even width for the recurrence comparison")
    parser.add_argument("--side", type=int, default=32,
                        help="maximum side length for the direct finite-graph check")
    args = parser.parse_args()
    if args.width < 2 or args.side < 2:
        parser.error("both limits must be at least two")
    for width in range(2, args.width + 1, 2):
        check_strip(width)
    print(f"Strip formula and every cut residue verified for {args.width // 2} even widths.")
    rectangles = 0
    for rows in range(1, args.side + 1):
        for columns in range(1, args.side + 1):
            if rows % 2 == 0 or columns % 2 == 0:
                check_rectangle(rows, columns)
                rectangles += 1
    print(f"Finite neighbourhoods verified on {rectangles} rectangles.")
    check_large_queries()
    print("Large-coordinate neighbourhoods verified on 1024 reproducibly sampled grids.")


if __name__ == "__main__":
    main()

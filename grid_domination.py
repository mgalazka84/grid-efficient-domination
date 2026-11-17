"""Random-access 1,2-efficient domination on rectangular grids with an even side."""

import argparse
from dataclasses import dataclass


def choose_cut(width, length):
    """Return the seed (A or B) and the column just before the rectangle."""
    if width < 2 or width % 2 or length < 1:
        raise ValueError("width must be positive and even, and length must be positive")
    half = width // 2
    block_length = width + 1
    residue = length % block_length
    if residue % 2 == 0:
        central_even = half + half % 2
        return "A", max(0, central_even - residue)
    if residue == 1:
        return "B", 0
    gap = block_length - residue
    central_odd = half + (1 - half % 2)
    return "B", max(1 + gap, central_odd)


def strip_member(width, seed, row, column):
    """Return one bit of the infinite strip, with rows 1 through width."""
    block_length = width + 1
    block, position = divmod(column, block_length)
    if block % 2:
        row = block_length - row
    diagonal = row if row % 2 == 0 else block_length - row
    if position % 2:
        if position >= diagonal:
            return False
        index = row + position - 1
    else:
        if diagonal <= block_length - position:
            return False
        index = position - row - 1 if row % 2 else row + position - 1
    residues = (1, 2) if seed == "A" else (0, 1)
    return index % 4 in residues


@dataclass(frozen=True)
class Grid:
    """A grid and its implicit dominating set. Public coordinates are one-based."""

    rows: int
    columns: int

    def __post_init__(self):
        if self.rows < 1 or self.columns < 1:
            raise ValueError("both dimensions must be positive")
        if self.rows % 2 and self.columns % 2:
            raise ValueError("this construction requires an even side")

    def contains(self, row, column):
        if not (1 <= row <= self.rows and 1 <= column <= self.columns):
            raise ValueError("cell lies outside the grid")
        width, length = self.rows, self.columns
        if width % 2:
            width, length = length, width
            row, column = column, row
        seed, cut = choose_cut(width, length)
        return strip_member(width, seed, row, cut + column)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rows", type=int)
    parser.add_argument("columns", type=int)
    parser.add_argument("--cell", nargs=2, type=int, metavar=("ROW", "COLUMN"),
                        help="print a single membership bit instead of the full bitmap")
    args = parser.parse_args()
    try:
        grid = Grid(args.rows, args.columns)
        if args.cell is not None:
            print(int(grid.contains(*args.cell)))
        else:
            for row in range(1, grid.rows + 1):
                for column in range(1, grid.columns + 1):
                    print(int(grid.contains(row, column)), end="")
                print()
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

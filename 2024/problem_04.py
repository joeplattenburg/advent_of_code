import sys
import numpy as np


def get_count_at_index(i: int, j: int, mat: np.ndarray, word: str = "XMAS") -> int:
    l = len(word)
    counter = 0
    counter += int(safe_access((i, i + 1), (j, j + l), mat) == word)
    counter += int(safe_access((i, i + 1), (j, j - l), mat) == word)
    counter += int(safe_access((i, i + l), (j, j + 1), mat) == word)
    counter += int(safe_access((i, i - l), (j, j + 1), mat) == word)
    counter += int(safe_access((i, i + l), (j, j + l), mat, diag=True) == word)
    counter += int(safe_access((i, i - l), (j, j + l), mat, diag=True) == word)
    counter += int(safe_access((i, i + l), (j, j - l), mat, diag=True) == word)
    counter += int(safe_access((i, i - l), (j, j - l), mat, diag=True) == word)
    return counter


def safe_access(
        row_range: tuple[int, int], col_range: tuple[int, int], mat: np.ndarray, diag: bool = False
) -> str:
    row_slice = slice(
        None if row_range[0] < 0 else row_range[0],
        None if row_range[1] < 0 else row_range[1],
        -1 if row_range[1] < row_range[0] else 1
    )
    col_slice = slice(
        None if col_range[0] < 0 else col_range[0],
        None if col_range[1] < 0 else col_range[1],
        -1 if col_range[1] < col_range[0] else 1
    )
    subset = mat[row_slice, col_slice]
    if diag:
        subset = np.diag(subset)
    return ''.join(subset.reshape(-1))


if __name__ == "__main__":
    input_path = sys.argv[1]
    input_ = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            input_.append([c for c in line.strip()])
    mat = np.array(input_)
    rows, cols = mat.shape
    counter = 0
    for i in range(rows):
        for j in range(cols):
            if mat[i, j] == 'X':
                counter += get_count_at_index(i, j, mat)
    print(f'Part 1: {counter}')
    part2 = 0
    print(f'Part 2: {part2}')

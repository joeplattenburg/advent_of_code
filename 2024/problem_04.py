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


def is_xmas(i: int, j: int, mat: np.ndarray) -> bool:
    check = mat[(i - 1):(i + 2), (j - 1):(j + 2)]
    if check.shape != (3, 3):
        return False
    return {check[0, 0], check[2, 2]} == {check[2, 0], check[0, 2]} == {'M', 'S'}


if __name__ == "__main__":
    input_path = sys.argv[1]
    input_ = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            input_.append([c for c in line.strip()])
    mat = np.array(input_)
    rows, cols = mat.shape
    counter1, counter2 = 0, 0
    for i in range(rows):
        for j in range(cols):
            if mat[i, j] == 'X':
                counter1 += get_count_at_index(i, j, mat)
            if mat[i, j] == 'A':
                counter2 += int(is_xmas(i, j, mat))
    print(f'Part 1: {counter1}')
    print(f'Part 2: {counter2}')

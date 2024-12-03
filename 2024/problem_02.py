import sys


if __name__ == "__main__":
    input_path = sys.argv[1]
    safe_count = 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            levels = [int(l) for l in line.strip().split()]
            sign = 0
            safe = True
            for level, next_level in zip(levels[:-1], levels[1:]):
                diff = next_level - level
                new_sign = 1 if diff > 0 else -1
                sign_change = new_sign * sign == -1
                sign = new_sign
                if abs(diff) < 1 or abs(diff) > 3 or sign_change:
                    safe = False
                    break
            if safe:
                safe_count += 1
    assert safe_count == 341
    print(f'Part 1: {safe_count}')




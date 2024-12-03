import sys


def report_safe(levels: list[int]) -> bool:
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
    return safe


if __name__ == "__main__":
    input_path = sys.argv[1]
    safe_count = 0
    safe_count_damper = 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            levels = [int(l) for l in line.strip().split()]
            if report_safe(levels):
                safe_count += 1
                safe_count_damper += 1
            else:
                for i in range(len(levels)):
                    temp_levels = levels.copy()
                    temp_levels.pop(i)
                    if report_safe(temp_levels):
                        safe_count_damper += 1
                        break
    print(f'Part 1: {safe_count}')
    print(f'Part 2: {safe_count_damper}')

import sys
from collections import Counter


def parse_input(input_path: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    section = 1
    rules = []
    updates = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            l = line.strip()
            if section == 1:
                if l == '':
                    section = 2
                else:
                    first, second = l.split('|')
                    rules.append((int(first), int(second)))
            else:
                updates.append([int(i) for i in l.split(',')])
    return rules, updates


def get_relevant_rules(rules: list[tuple[int, int]], update: list[int]) -> list[tuple[int, int]]:
    return [rule for rule in rules if rule[0] in update and rule[1] in update]


def is_valid(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for rule in rules:
        if rule[1] not in update[update.index(rule[0]):]:
            return False
    return True


def make_valid(rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    counted = Counter([rule[0] for rule in rules])
    out = [k for k, v in sorted(counted.items(), key=lambda item: item[1], reverse=True)]
    last_page = list(set(update) - set(out))
    return out + last_page


def middle_page(update: list[int]) -> int:
    return update[len(update) // 2]


if __name__ == "__main__":
    input_path = sys.argv[1]
    rules, updates = parse_input(input_path)
    part1 = 0
    part2 = 0
    for update in updates:
        relevant_rules = get_relevant_rules(rules, update)
        if is_valid(relevant_rules, update):
            part1 += middle_page(update)
        else:
            part2 += middle_page(make_valid(relevant_rules, update))
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

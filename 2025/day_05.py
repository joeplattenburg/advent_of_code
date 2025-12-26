import sys
from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass
class Range:
    lower: int
    upper: int

    @classmethod
    def from_str(cls, s: str) -> 'Range':
        lower, upper = s.split('-')
        return cls(lower=int(lower), upper=int(upper))

    @property
    def size(self):
        return self.upper - self.lower + 1

    def union(self, other: 'Range') -> list['Range']:
        if self.lower > other.upper or self.upper < other.lower:
            return sorted([self, other])
        else:
            return [Range(lower=min(self.lower, other.lower), upper=max(self.upper, other.upper))]

    def __eq__(self, other: 'Range') -> bool:
        return self.lower == other.lower and self.upper == other.upper

    def __lt__(self, other: 'Range') -> bool:
        return (self.lower < other.lower) or (self.lower == other.lower and self.upper < other.upper)


@dataclass
class Database:
    ranges: list[Range]

    def in_range(self, i: int) -> bool:
        for r in self.ranges:
            if r.lower <= i <= r.upper:
                return True
        return False

    @classmethod
    def from_string(cls, s: str) -> 'Database':
        return cls(ranges=sorted([Range.from_str(line) for line in s.split('\n')]))

    def make_unique(self) -> 'Database':
        unique_ranges = self.ranges[:1]
        for next_ in self.ranges[1:]:
            last_ = unique_ranges.pop(-1)
            unique_ranges += last_.union(next_)
        self.ranges = sorted(unique_ranges)
        return self

    def count_valid(self) -> int:
        return sum(r.size for r in self.ranges)


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        top, bottom = f.read().split('\n\n')
    database = Database.from_string(top).make_unique()
    part1 = sum(1 for i in bottom.split('\n') if database.in_range(int(i)))
    part2 = database.count_valid()
    print('Part 1:', part1)
    print('Part 2:', part2)

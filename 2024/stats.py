import subprocess
import time
import csv


if __name__ == "__main__":
    recs = []
    for day in range(1, 26):
        tic = time.time()
        output = subprocess.run(['uv', 'run', f'problem_{day:02}.py', f'inputs/input_{day:02}_1.txt'], capture_output=True)
        toc = time.time()
        part1, part2 = output.stdout.decode("utf-8").strip().split('\n')
        recs.append({
            'day': day,
            'time': toc - tic,
            'part1': part1.split(': ')[1],
            'part2': part2.split(': ')[1],
        })
    with open('stats.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=recs[0].keys())
        w.writeheader()
        w.writerows(recs)

import csv
import re
import sys
from collections import Counter
from pathlib import Path

DATE_RE = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')


def count_jobs_by_date(path: str) -> dict[str, int]:
    counts: Counter = Counter()
    with open(path) as f:
        for line in f:
            # Skip header, separator, and summary lines
            stripped = line.strip()
            if not stripped or stripped.startswith('-') or stripped[0].isdigit() and 'workloads' in stripped:
                continue
            # Header row has no UUID pattern
            if re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-', stripped):
                m = DATE_RE.search(stripped)
                if m:
                    counts[m.group(1)] += 1
    return dict(sorted(counts.items()))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <workloads_file>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    counts = count_jobs_by_date(path)

    out_path = Path(path).with_name(Path(path).stem + '_time_series.csv')
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['date', 'count'])
        w.writerows(counts.items())
    print(f"Saved {len(counts)} rows to {out_path}")

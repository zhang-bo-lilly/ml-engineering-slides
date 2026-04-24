"""
Extract slide metrics from LillyPod data files.

Writes metrics.json and timeseries_data.csv to this directory.
gen_slides.py reads both files, so run this first whenever new data arrives.

Usage (auto-discovers latest files by glob):
    python extract_metrics.py

Usage (explicit paths):
    python extract_metrics.py --users users.txt --projects projects.txt \
        --workloads workloads_20260501_090000.txt
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Accounts to exclude from user count
TEST_ACCOUNTS = {'runai-test@run.ai', 'test@run.ai'}

# Projects excluded from the active-project count (per the projects.txt summary line)
EXCLUDED_PROJECTS = {'default', 'common'}


def find_latest(pattern):
    matches = glob.glob(os.path.join(BASE_DIR, pattern))
    if not matches:
        return None
    return max(matches, key=os.path.getmtime)


def parse_users(path):
    count = 0
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('-'):
                continue
            parts = stripped.split()
            if not parts or parts[0].lower() == 'username':
                continue
            if parts[0] not in TEST_ACCOUNTS:
                count += 1
    return count


def parse_projects(path):
    count = 0
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('-') or '|' in stripped:
                continue
            parts = stripped.split()
            if not parts or parts[0].lower() == 'project':
                continue
            if parts[0] not in EXCLUDED_PROJECTS:
                count += 1
    return count


def parse_workloads(path):
    UUID_RE = re.compile(
        r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    )
    total_workloads = 0
    total_gpu_hours = 0.0
    cloud_cost = None
    since_date = None
    gpu_hours_by_project = {}
    jobs_by_date = {}

    with open(path) as f:
        for line in f:
            stripped = line.strip()

            # Summary line: "9055 workloads since 2026-02-23  |  568493.704 GPU-hours  |  est. cloud cost $7,893,853.44"
            if 'workloads since' in stripped:
                m = re.match(r'(\d+)\s+workloads since\s+(\S+)', stripped)
                if m:
                    total_workloads = int(m.group(1))
                    since_date = m.group(2)
                m2 = re.search(r'([\d.]+)\s+GPU-hours', stripped)
                if m2:
                    total_gpu_hours = float(m2.group(1))
                m3 = re.search(r'est\. cloud cost \$([0-9,]+(?:\.\d+)?)', stripped)
                if m3:
                    cloud_cost = float(m3.group(1).replace(',', ''))
                continue

            m = UUID_RE.search(line)
            if not m:
                continue
            parts = line[m.end():].split()
            if len(parts) < 7:
                continue
            # fields after UUID: Type Phase Project GPU_Req Created Pending Running
            project, gpu_s, date_s, run_s = parts[2], parts[3], parts[4], parts[6]
            if '—' in (gpu_s, run_s):
                continue
            try:
                gpu_h = float(gpu_s) * float(run_s) / 3600
                gpu_hours_by_project[project] = gpu_hours_by_project.get(project, 0.0) + gpu_h
                jobs_by_date[date_s] = jobs_by_date.get(date_s, 0) + 1
            except ValueError:
                pass

    return {
        'total_workloads': total_workloads,
        'total_gpu_hours': total_gpu_hours,
        'since_date': since_date,
        'cloud_cost_usd': cloud_cost,
        'gpu_hours_by_project': gpu_hours_by_project,
        'jobs_by_date': dict(sorted(jobs_by_date.items())),
    }


def fmt_cost(usd):
    if usd >= 1_000_000:
        return f'${usd / 1_000_000:.1f}M'
    if usd >= 1_000:
        return f'${usd / 1_000:.0f}K'
    return f'${usd:.0f}'


def fmt_workloads(n):
    return f'{n:,}'


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--users',     help='Path to users.txt')
    parser.add_argument('--projects',  help='Path to projects.txt')
    parser.add_argument('--workloads', help='Path to workloads*.txt')
    args = parser.parse_args()

    users_path     = args.users     or find_latest('users*.txt')
    projects_path  = args.projects  or find_latest('projects*.txt')
    workloads_path = args.workloads or find_latest('workloads*.txt')

    missing = [n for n, p in [('users', users_path), ('projects', projects_path),
                               ('workloads', workloads_path)] if not p]
    if missing:
        print(f'ERROR: Could not find files for: {", ".join(missing)}', file=sys.stderr)
        sys.exit(1)

    print(f'users     : {users_path}')
    print(f'projects  : {projects_path}')
    print(f'workloads : {workloads_path}')
    print()

    n_users    = parse_users(users_path)
    n_projects = parse_projects(projects_path)
    wl         = parse_workloads(workloads_path)

    metrics = {
        'generated_at': datetime.now().isoformat(),
        'sources': {
            'users':     os.path.basename(users_path),
            'projects':  os.path.basename(projects_path),
            'workloads': os.path.basename(workloads_path),
        },
        # Slide 1 stats
        'users':            n_users,
        'projects':         n_projects,
        'total_workloads':  wl['total_workloads'],
        'total_gpu_hours':  wl['total_gpu_hours'],
        'since_date':       wl['since_date'],
        'cloud_cost_usd':   wl['cloud_cost_usd'],
        'cloud_cost_label': fmt_cost(wl['cloud_cost_usd']) if wl['cloud_cost_usd'] else None,
        'workloads_label':  fmt_workloads(wl['total_workloads']),
        # Slide 2 data
        'gpu_hours_by_project': {
            k: round(v, 1)
            for k, v in sorted(wl['gpu_hours_by_project'].items(), key=lambda x: -x[1])
        },
        # Chart data (also written to timeseries_data.csv)
        'jobs_by_date': wl['jobs_by_date'],
    }

    # Write metrics.json
    metrics_path = os.path.join(BASE_DIR, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    # Write stable timeseries CSV for diagram_timeseries.py
    csv_path = os.path.join(BASE_DIR, 'timeseries_data.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['date', 'count'])
        w.writerows(metrics['jobs_by_date'].items())

    # Human-readable summary
    print(f"Active projects : {metrics['projects']}")
    print(f"Registered users: {metrics['users']}")
    print(f"Total workloads : {metrics['workloads_label']}  (since {metrics['since_date']})")
    print(f"Total GPU-hours : {metrics['total_gpu_hours']:,.1f}")
    print(f"Cloud cost equiv: {metrics['cloud_cost_label']}")
    print()
    print('GPU-hours by project (top 10):')
    for proj, hrs in list(metrics['gpu_hours_by_project'].items())[:10]:
        print(f'  {proj:<28} {hrs:>10,.0f} hrs')
    print()
    print(f'Saved -> {metrics_path}')
    print(f'Saved -> {csv_path}')


if __name__ == '__main__':
    main()

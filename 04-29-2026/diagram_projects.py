import json
import math
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HIGHLIGHT_RED  = {'alchemy', 'large-mol', 'small-mol'}
HIGHLIGHT_BLUE = {'tunelab-ai'}

RED   = '#e4002b'
BLUE  = '#3b82f6'
GRAY  = '#cccccc'
BG    = '#f7f7f7'
DARK  = '#333333'
WHITE = '#ffffff'

LOG_FLOOR = 1


def fmt_hours(h):
    if h >= 1000:
        return f'{h / 1000:.0f}K'
    if h >= 1:
        return str(int(h))
    return ''


def parse_projects(path):
    EXCLUDE = {'default', 'common'}
    names = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('-') or '|' in s:
                continue
            parts = s.split()
            if not parts or parts[0].lower() == 'project':
                continue
            if parts[0] not in EXCLUDE:
                names.append(parts[0])
    return names


def main():
    with open(os.path.join(BASE_DIR, 'metrics.json')) as f:
        metrics = json.load(f)

    gpu = metrics['gpu_hours_by_project']
    projects = parse_projects(os.path.join(BASE_DIR, 'projects.txt'))

    # Sort descending by GPU-hours, drop projects with no activity
    projects = sorted(
        [p for p in projects if gpu.get(p, 0) > 0],
        key=lambda p: gpu[p],
        reverse=True,
    )
    raw    = [gpu[p] for p in projects]
    values = [max(v, LOG_FLOOR) for v in raw]

    colors = []
    for p in projects:
        if p in HIGHLIGHT_RED:
            colors.append(RED)
        elif p in HIGHLIGHT_BLUE:
            colors.append(BLUE)
        else:
            colors.append(GRAY)

    fig, ax = plt.subplots(figsize=(26.4, 7), facecolor=BG)
    ax.set_facecolor(BG)

    bars = ax.bar(range(len(projects)), values, color=colors, width=0.6, zorder=2)

    ax.set_yscale('log')
    y_top = max(values) * 5
    ax.set_ylim(LOG_FLOOR * 0.8, y_top)

    # X-axis: slanted project names
    ax.set_xticks(range(len(projects)))
    ax.set_xticklabels(projects, rotation=35, ha='right', fontsize=18, color=DARK)
    ax.tick_params(axis='x', length=0)

    # Y-axis: label only, no tick numbers
    ax.set_ylabel('GPU-hrs', fontsize=20, color='#555555', labelpad=10)
    ax.yaxis.set_major_formatter(ticker.NullFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    ax.tick_params(axis='y', length=0)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', color='#dddddd', linewidth=0.8, zorder=1)

    # Value labels — inside tall bars (white), above short bars (dark)
    log_ymin  = math.log10(LOG_FLOOR * 0.8)
    log_ytop  = math.log10(y_top)
    log_range = log_ytop - log_ymin

    for bar, r, v in zip(bars, raw, values):
        if r < 10:
            continue
        label = fmt_hours(r)
        bx = bar.get_x() + bar.get_width() / 2
        log_bar_top = math.log10(v)
        bar_frac = (log_bar_top - log_ymin) / log_range

        if bar_frac > 0.30:
            # Tall enough — center label inside on log scale
            log_mid = (log_bar_top + log_ymin) / 2
            ax.text(bx, 10 ** log_mid, label,
                    ha='center', va='center',
                    fontsize=16, fontweight='bold', color=WHITE, zorder=3)
        else:
            ax.text(bx, v * 1.8, label,
                    ha='center', va='bottom',
                    fontsize=15, fontweight='bold', color=DARK, zorder=3)

    fig.tight_layout(pad=0.5)
    out = os.path.join(BASE_DIR, 'projects_gpuhours.png')
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    main()

import csv
import os
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RED = '#e4002b'
BG  = '#f7f7f7'


def main():
    csv_path = os.path.join(BASE_DIR, 'timeseries_data.csv')
    dates, counts = [], []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            dates.append(datetime.strptime(row['date'], '%Y-%m-%d'))
            counts.append(int(row['count']))

    fig, ax = plt.subplots(figsize=(24, 6), facecolor=BG)
    ax.set_facecolor(BG)

    ax.bar(dates, counts, color=RED, width=0.8, zorder=2)

    # Month labels only
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', labelsize=22, colors='#555555', length=0)
    ax.tick_params(axis='y', labelsize=20, colors='#555555', length=0)

    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f'{int(x):,}' if x >= 1 else ''
    ))

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', color='#dddddd', linewidth=0.8, zorder=1)

    from datetime import timedelta
    ax.set_xlim(dates[0] - timedelta(days=1), dates[-1] + timedelta(days=2))
    ax.set_ylim(0.8, max(counts) * 1.5)

    fig.tight_layout(pad=0.4)
    out = os.path.join(BASE_DIR, 'timeseries.png')
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    main()

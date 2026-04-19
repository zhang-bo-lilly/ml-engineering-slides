"""
diagram_cost.py — Cost comparison bar chart for slide 4.
Output: diagram_cost.png (2800 × 1400 px @ 200 dpi)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import blended_transform_factory
import numpy as np

EMERALD  = '#10b981'
AWS3     = '#60a5fa'   # light blue — 3-year
AWS5     = '#2563eb'   # dark blue  — 5-year
LIGHT_BG = '#f7f7f7'

fig, ax = plt.subplots(figsize=(14, 7), facecolor=LIGHT_BG)
ax.set_facecolor(LIGHT_BG)

# Bar positions
BAR_W = 0.30
GAP   = 0.08

# MagTrain group center = 0.6, LillyPod group center = 2.6
G0 = 0.6   # MagTrain
G1 = 2.6   # LillyPod

# MagTrain AWS SP 5-yr: extrapolated from 3-yr rate, with 22% Lilly enterprise discount applied
DISC    = 0.78
MT_AWS3 = round(19 * DISC, 1)           # 14.8
MT_AWS5 = round(19 * DISC * 5 / 3, 1)  # 24.7

pos = {
    'mt_prem': G0 - BAR_W - GAP,
    'mt_aws3': G0,
    'mt_aws5': G0 + BAR_W + GAP,
    'lp_prem': G1 - BAR_W - GAP,
    'lp_aws3': G1,
    'lp_aws5': G1 + BAR_W + GAP,
}

# multipliers: AWS SP vs on-prem
MT_MULT3 = f'{round(MT_AWS3 / 6.8, 1)}×'   # 3-yr vs capex
MT_MULT5 = f'{round(MT_AWS5 / 6.8, 1)}×'   # 5-yr vs capex
LP_MULT3 = f'{round(247 / 150, 1)}×'
LP_MULT5 = f'{round(412 / 150, 1)}×'

bars = [
    (pos['mt_prem'], 6.8,    EMERALD, None),
    (pos['mt_aws3'], MT_AWS3, AWS3,   MT_MULT3),
    (pos['mt_aws5'], MT_AWS5, AWS5,   MT_MULT5),
    (pos['lp_prem'], 150,    EMERALD, None),
    (pos['lp_aws3'], 247,    AWS3,    LP_MULT3),
    (pos['lp_aws5'], 412,    AWS5,    LP_MULT5),
]

for xp, val, color, mult in bars:
    ax.bar(xp, val, width=BAR_W, color=color, zorder=3, linewidth=0, alpha=0.90)
    ax.text(xp, val * 1.08, f'${val}M', ha='center', va='bottom',
            fontsize=12, fontweight='bold', color='#222222')
    # Draw multiplier inside the bar (vertically centered)
    if mult:
        ax.text(xp, val / 2, mult, ha='center', va='center',
                fontsize=13, fontweight='bold', color='white', zorder=4)

# Footnote
plt.figtext(0.02, 0.01, '* AWS Savings Plans max at 3 years; 5-yr figures extrapolated at same rate. All AWS figures reflect 22% Lilly enterprise discount.',
            fontsize=9, color='#888888')

# Callout box: AWS SP 3yr > LillyPod 5yr TCO
ax.annotate(
    'AWS SP 3-yr alone ($247M)\nexceeds LillyPod\'s full\n5-yr TCO ($150M)',
    xy=(pos['lp_aws3'], 247),
    xytext=(pos['lp_aws3'] + 0.55, 350),
    fontsize=11.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.5', fc='#fef3c7', ec='#f59e0b', lw=1.8),
    arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=1.8),
)

# Group labels — blended transform: data x, axes fraction y
trans = blended_transform_factory(ax.transData, ax.transAxes)
ax.text(G0, -0.06, 'MagTrain', ha='center', fontsize=15,
        fontweight='bold', color='#333333', transform=trans)
ax.text(G1, -0.06, 'LillyPod', ha='center', fontsize=15,
        fontweight='bold', color='#333333', transform=trans)

# Legend
ax.legend(
    handles=[mpatches.Patch(color=EMERALD, label='On-Premise'),
             mpatches.Patch(color=AWS3,    label='AWS Savings Plans 3-yr'),
             mpatches.Patch(color=AWS5,    label='AWS Savings Plans 5-yr*')],
    loc='lower center', bbox_to_anchor=(0.5, 1.01),
    ncol=3, fontsize=12, frameon=False,
)

# Axes styling
ax.set_yscale('log')
ax.set_xlim(-0.1, 3.8)
ax.set_ylim(4, 700)
ax.set_yticks([10, 50, 100, 200, 500])
ax.set_yticklabels(['$10M', '$50M', '$100M', '$200M', '$500M'],
                   fontsize=11, color='#555555')
ax.set_ylabel('log scale', fontsize=10, color='#aaaaaa', labelpad=6)
ax.tick_params(bottom=False, labelbottom=False)
for spine in ['top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.yaxis.grid(True, color='#e5e5e5', zorder=0, linestyle='--', alpha=0.8)
ax.set_axisbelow(True)

plt.tight_layout(pad=1.5, rect=[0, 0.06, 1, 0.94])
plt.savefig('diagram_cost.png', dpi=200, facecolor=LIGHT_BG, bbox_inches='tight')
print('saved diagram_cost.png')

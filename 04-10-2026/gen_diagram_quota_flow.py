"""
gen_diagram_quota_flow.py — Draw the biweekly quota adjustment decision flowchart.

Output: diagram-quota-flow.png  (2000 × 1440 px, light bg, 160 DPI)

Run: source .venv/bin/activate && python3 gen_diagram_quota_flow.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Palette (matches gen_slides.py) ─────────────────────────────────────────
BG        = '#f7f7f7'
LILLY_RED = '#e4002b'
EMERALD   = '#10b981'
BLUE      = '#3b82f6'
AMBER     = '#f59e0b'
GREY_CARD = '#9ca3af'
WHITE     = '#ffffff'
BLACK     = '#1a1a1a'
GREY_DIM  = '#d0d5e0'
GREY_TEXT = '#555555'

DPI   = 160
FIG_W = 12.5   # inches  → 2000 px
FIG_H = 9.0    # inches  → 1440 px

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12.5)
ax.set_ylim(0, 9.0)
ax.axis('off')

plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'

# ── Drawing helpers ───────────────────────────────────────────────────────────

def proc_box(cx, cy, w, h, text, fill=WHITE, edge=GREY_DIM,
             tc=BLACK, fs=10, bold=False):
    """Rounded rectangle process box centered at (cx, cy)."""
    rect = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.10',
        facecolor=fill, edgecolor=edge, linewidth=1.8, zorder=3,
    )
    ax.add_patch(rect)
    fw = 'bold' if bold else 'normal'
    ax.text(cx, cy, text,
            ha='center', va='center', fontsize=fs, color=tc,
            fontweight=fw, multialignment='center', zorder=4)


def decision_diamond(cx, cy, dw, dh, text, fill=WHITE, edge=EMERALD,
                     tc=BLACK, fs=10):
    """Diamond decision shape centered at (cx, cy)."""
    pts = np.array([
        [cx,          cy + dh / 2],
        [cx + dw / 2, cy         ],
        [cx,          cy - dh / 2],
        [cx - dw / 2, cy         ],
    ])
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge,
                   linewidth=2.5, zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, text,
            ha='center', va='center', fontsize=fs, color=tc,
            fontweight='bold', multialignment='center', zorder=4)


def tier_box(cx, cy, w, h, tier_label, formula, fill):
    """Colored tier result box with tier name above formula."""
    proc_box(cx, cy, w, h, '', fill=fill, edge=WHITE)
    ax.text(cx, cy + h * 0.17, tier_label,
            ha='center', va='center', fontsize=11, color=WHITE,
            fontweight='bold', zorder=4)
    ax.text(cx, cy - h * 0.22, formula,
            ha='center', va='center', fontsize=9, color=WHITE,
            multialignment='center', zorder=4)


def arrow(x1, y1, x2, y2, label='', lx=None, ly=None):
    """Draw arrow from (x1, y1) to (x2, y2) with optional Yes/No label."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=GREY_TEXT,
                    lw=1.8, mutation_scale=20,
                ),
                zorder=2)
    if label:
        mx = (x1 + x2) / 2 if lx is None else lx
        my = (y1 + y2) / 2 if ly is None else ly
        ax.text(mx, my, label,
                ha='center', va='center', fontsize=9, color=GREY_TEXT,
                style='italic', zorder=5,
                bbox=dict(boxstyle='round,pad=0.08', facecolor=BG,
                          edgecolor='none', alpha=0.9))


# ── Layout coordinates ────────────────────────────────────────────────────────
# START
S_CX,  S_CY  = 3.0, 8.45
S_W,   S_H   = 5.5, 0.65

# Decisions (diamond half-dims: dw, dh)
D_DW, D_DH = 2.5, 1.0
D1_X, D1_Y = 3.0, 7.2   # EQ > Q?
D2_DW      = 3.2
D2_X, D2_Y = 7.5, 7.2   # avg util > 80%?
D3_X, D3_Y = 3.0, 4.5   # EQ ≥ 0.8Q?

# Tier result boxes
T1_X, T1_Y = 11.2, 7.2
T2_X, T2_Y = 7.5,  5.75
T3_X, T3_Y = 7.0,  4.5
T4_X, T4_Y = 3.0,  2.7
T_W, T_H   = 2.8, 0.95   # Tier 2 / 3 / 4 box dims
T1_W       = 2.0           # Tier 1 box width

# New squad note
NS_CX, NS_CY = 6.5, 1.35
NS_W,  NS_H  = 10.5, 0.80

# ── Draw shapes ───────────────────────────────────────────────────────────────

# Section header
ax.text(0.25, 8.85,
        'BIWEEKLY QUOTA ADJUSTMENT — DECISION FLOW',
        fontsize=11, color=LILLY_RED, fontweight='bold',
        ha='left', va='center', zorder=5)

# START box
proc_box(S_CX, S_CY, S_W, S_H,
         'For each squad:\nCompute EQ = allocated GPU-hrs ÷ evaluation period hours',
         fill=WHITE, edge=GREY_DIM, tc=BLACK, fs=10)

# Decision diamonds
decision_diamond(D1_X, D1_Y, D_DW, D_DH, 'EQ > Q?')
decision_diamond(D2_X, D2_Y, D2_DW, D_DH, 'avg util\n> 80%?')
decision_diamond(D3_X, D3_Y, D_DW, D_DH, 'EQ ≥ 0.8Q?')

# Tier boxes
tier_box(T1_X, T1_Y, T1_W, T_H,  'TIER 1', 'EQ + ND',            EMERALD)
tier_box(T2_X, T2_Y, T_W,  T_H,  'TIER 2', '(EQ−Q)·DF + Q + ND', BLUE)
tier_box(T3_X, T3_Y, T_W,  T_H,  'TIER 3', 'Q + ND·(EQ/Q)',       AMBER)
tier_box(T4_X, T4_Y, 2.2,  T_H,  'TIER 4', 'EQ',                  GREY_CARD)

# New squad note
proc_box(NS_CX, NS_CY, NS_W, NS_H,
         'New squad (no history): weight = min(ND, max weight cap)  →  treated as Tier 3',
         fill='#ebebeb', edge='#aaaaaa', tc=GREY_TEXT, fs=9)

# ── Draw arrows ───────────────────────────────────────────────────────────────

# START → D1 (straight down)
arrow(S_CX, S_CY - S_H / 2,
      D1_X, D1_Y + D_DH / 2)

# D1 → D2 (Yes, horizontal right)
arrow(D1_X + D_DW / 2, D1_Y,
      D2_X - D2_DW / 2, D2_Y,
      label='Yes', ly=D1_Y + 0.28)

# D2 → T1 (Yes, horizontal right)
arrow(D2_X + D2_DW / 2, D2_Y,
      T1_X - T1_W / 2, T1_Y,
      label='Yes', ly=D2_Y + 0.28)

# D2 → T2 (No, straight down)
arrow(D2_X, D2_Y - D_DH / 2,
      T2_X, T2_Y + T_H / 2,
      label='No', lx=D2_X + 0.38)

# D1 → D3 (No, straight down)
arrow(D1_X, D1_Y - D_DH / 2,
      D3_X, D3_Y + D_DH / 2,
      label='No', lx=D1_X + 0.38)

# D3 → T3 (Yes, horizontal right)
arrow(D3_X + D_DW / 2, D3_Y,
      T3_X - T_W / 2, T3_Y,
      label='Yes', ly=D3_Y + 0.28)

# D3 → T4 (No, straight down)
arrow(D3_X, D3_Y - D_DH / 2,
      T4_X, T4_Y + T_H / 2,
      label='No', lx=D3_X + 0.38)

# ── Save ──────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.3)
out = os.path.join(BASE_DIR, 'diagram-quota-flow.png')
fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
print(f'  Saved {out}')

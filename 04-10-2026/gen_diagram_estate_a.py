import os
import matplotlib
matplotlib.use('Agg')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Light-mode palette ────────────────────────────────────────────────────────
BG           = '#f7f7f7'
CARD_BG      = '#ffffff'
GOV_BORDER   = '#10b981'   # Compute Layer emerald
GOV_FILL     = '#f0faf6'   # very light green tint
UNGOV_BORDER = '#b0bac5'   # grey
UNGOV_FILL   = '#f0f2f5'
TEXT_DARK    = '#1a1a1a'
TEXT_MID     = '#444444'
TEXT_DIM     = '#888888'
TEXT_GREEN   = '#0a7c57'   # darker emerald — legible on white
RED          = '#e4002b'   # Lilly Red

FIG_W, FIG_H = 16, 8.1
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')

def box(x, y, w, h, fill, edge, lw=1.5, ls='-', alpha=1.0, radius=0.18, zorder=2):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
        linestyle=ls, zorder=zorder, alpha=alpha
    )
    ax.add_patch(rect)

def label(x, y, text, color=TEXT_DARK, size=9, weight='normal', ha='center', va='center', zorder=6, style='normal'):
    ax.text(x, y, text, color=color, fontsize=size, fontweight=weight,
            ha=ha, va=va, zorder=zorder, style=style)

# ── GOVERNED ROW ──────────────────────────────────────────────────────────────
GOV_X, GOV_Y = 0.3, 3.9
GOV_W, GOV_H = 15.4, 3.8

box(GOV_X, GOV_Y, GOV_W, GOV_H, GOV_FILL, GOV_BORDER, lw=2.5, radius=0.3, zorder=1)
label(GOV_X + GOV_W/2, GOV_Y + GOV_H - 0.32,
      "THIS TEAM'S GOVERNANCE",
      color=TEXT_GREEN, size=11, weight='bold')

gov_cards = [
    ('B300',  '1,016', 'LillyPod',        TEXT_GREEN),
    ('H100',  '72',    'MagTrain',         TEXT_MID),
    ('H200',  '64',    'MagTrain',         TEXT_MID),
    ('L40s',  '32',    'MagTrain',         TEXT_MID),
    ('A800',  '8',     'Standalone server', TEXT_DIM),
]

card_w, card_h = 2.4, 2.5
card_y = GOV_Y + 0.48
total_cards_w = len(gov_cards) * card_w + (len(gov_cards) - 1) * 0.38
start_x = GOV_X + (GOV_W - total_cards_w) / 2

for i, (gpu, count, loc, count_color) in enumerate(gov_cards):
    cx = start_x + i * (card_w + 0.38)
    border = GOV_BORDER if i == 0 else '#6abfa0'
    box(cx, card_y, card_w, card_h, CARD_BG, border, lw=1.8, radius=0.2, zorder=3)
    label(cx + card_w/2, card_y + card_h*0.74, gpu,
          color=TEXT_DARK, size=13, weight='bold')
    label(cx + card_w/2, card_y + card_h*0.50, count,
          color=count_color, size=16, weight='bold')
    label(cx + card_w/2, card_y + card_h*0.20, loc,
          color=TEXT_DIM, size=8)

# ── NON-GOVERNED ROW ──────────────────────────────────────────────────────────
UNGOV_Y = 0.3
UNGOV_H = 3.2
UNGOV_X, UNGOV_W = 0.3, 15.4

box(UNGOV_X, UNGOV_Y, UNGOV_W, UNGOV_H, UNGOV_FILL, UNGOV_BORDER, lw=1.5,
    ls='--', radius=0.3, zorder=1)
label(UNGOV_X + UNGOV_W/2, UNGOV_Y + UNGOV_H - 0.28,
      'REST OF ESTATE',
      color=TEXT_DIM, size=10, weight='bold')

ungov_cards = [
    ('Brainiac',         '~2,100', 'L4 · RTX6000 · A16\n+AWS burst (L40s)'),
    ('AWS\nNon-HPC',     '251',    'T4 · A4 · A10G\nmixed'),
    ('Azure',            '11',     'A10 · A100 · V100 · T4\nmixed'),
    ('Loxo\nColorado',   '140',    'misc GPU types'),
    ('San Diego\n+ Workstns', '~88', 'CryoEM · 4090\nRTX4000ADA etc.'),
    ('Alcobendas',       '5',      'V100'),
]

ucard_w = 2.2
ucard_h = 2.1
ucard_y = UNGOV_Y + 0.38
total_uw = len(ungov_cards) * ucard_w + (len(ungov_cards) - 1) * 0.30
ux_start = UNGOV_X + (UNGOV_W - total_uw) / 2

for i, (name, count, detail) in enumerate(ungov_cards):
    cx = ux_start + i * (ucard_w + 0.30)
    box(cx, ucard_y, ucard_w, ucard_h, CARD_BG, UNGOV_BORDER,
        lw=1.0, radius=0.18, zorder=3)
    label(cx + ucard_w/2, ucard_y + ucard_h*0.82, name,
          color=TEXT_DIM, size=9, weight='bold')
    label(cx + ucard_w/2, ucard_y + ucard_h*0.57, count,
          color='#a0aabb', size=13, weight='bold')
    label(cx + ucard_w/2, ucard_y + ucard_h*0.24, detail,
          color=TEXT_DIM, size=7.5, style='italic')

plt.tight_layout(pad=0.1)
plt.savefig(os.path.join(BASE_DIR, 'diagram-estate-full.png'),
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("Saved diagram-estate-full.png")

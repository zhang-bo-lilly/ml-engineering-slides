import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Light-mode palette ────────────────────────────────────────────────────────
BG           = '#f7f7f7'
CARD_BG      = '#ffffff'
GOV_BORDER   = '#10b981'   # Compute Layer emerald
GOV_FILL     = '#f0faf6'
UNGOV_BORDER = '#b0bac5'
UNGOV_FILL   = '#f0f2f5'
TEXT_DARK    = '#1a1a1a'
TEXT_MID     = '#444444'
TEXT_DIM     = '#888888'
TEXT_GREEN   = '#0a7c57'
RED          = '#e4002b'   # Lilly Red — used for stamps

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

def label(x, y, text, color=TEXT_DARK, size=9, weight='normal', ha='center', va='center',
          zorder=6, style='normal', rotation=0):
    ax.text(x, y, text, color=color, fontsize=size, fontweight=weight,
            ha=ha, va=va, zorder=zorder, style=style,
            rotation=rotation, rotation_mode='anchor')

# ── GOVERNED OUTER BOX ────────────────────────────────────────────────────────
GOV_X, GOV_Y = 0.3, 3.9
GOV_W, GOV_H = 15.4, 3.8

box(GOV_X, GOV_Y, GOV_W, GOV_H, GOV_FILL, GOV_BORDER, lw=2.5, radius=0.3, zorder=1)
label(GOV_X + GOV_W/2, GOV_Y + GOV_H - 0.32,
      "THIS TEAM'S GOVERNANCE",
      color=TEXT_GREEN, size=11, weight='bold')

# ── RUN:AI SUB-BOX (B300, H100, H200, L40s) ──────────────────────────────────
runai_cards = [
    ('B300', '1,016', 'LillyPod', TEXT_GREEN),
    ('H100', '72',    'MagTrain', '#0a7c57'),
    ('H200', '64',    'MagTrain', '#0a7c57'),
    ('L40s', '32',    'MagTrain', '#0a7c57'),
]

card_w, card_h = 2.4, 2.5
card_y = GOV_Y + 0.52

sub_pad_x   = 0.22
sub_pad_y_b = 0.30
total_runai_w = len(runai_cards) * card_w + (len(runai_cards) - 1) * 0.38
sub_x = GOV_X + 0.35
sub_w = total_runai_w + 2 * sub_pad_x

runai_start_x = sub_x + sub_pad_x
for i, (gpu, count, loc, count_color) in enumerate(runai_cards):
    cx = runai_start_x + i * (card_w + 0.38)
    border = GOV_BORDER if i == 0 else '#6abfa0'
    box(cx, card_y, card_w, card_h, CARD_BG, border, lw=1.8, radius=0.2, zorder=3)
    label(cx + card_w/2, card_y + card_h*0.74, gpu,
          color=TEXT_DARK, size=13, weight='bold')
    label(cx + card_w/2, card_y + card_h*0.50, count,
          color=count_color, size=16, weight='bold')
    label(cx + card_w/2, card_y + card_h*0.20, loc,
          color=TEXT_DIM, size=8)

# ── $$$ JUSTIFIED stamp over the Run:ai cards ─────────────────────────────────
stamp_rx = sub_x + sub_pad_x + (total_runai_w / 2)
stamp_ry = card_y + card_h * 0.50
label(stamp_rx, stamp_ry, '$$$  JUSTIFIED',
      color=RED, size=34, weight='bold', zorder=8, rotation=20)

# ── A800 — governed but outside Run:ai sub-box ────────────────────────────────
a800_x = sub_x + sub_w + 0.55
box(a800_x, card_y, card_w, card_h, CARD_BG, UNGOV_BORDER, lw=1.2, radius=0.2, zorder=3)
label(a800_x + card_w/2, card_y + card_h*0.74, 'A800',
      color=TEXT_DARK, size=13, weight='bold')
label(a800_x + card_w/2, card_y + card_h*0.50, '8',
      color=TEXT_DIM, size=16, weight='bold')
label(a800_x + card_w/2, card_y + card_h*0.20, 'Standalone server',
      color=TEXT_DIM, size=8)
# NOT JUSTIFIED stamp in Lilly Red
label(a800_x + card_w/2, card_y + card_h*0.50, '$$$\nNOT JUSTIFIED',
      color=RED, size=11, weight='bold', zorder=8, rotation=20)

# ── REST OF ESTATE BOX ────────────────────────────────────────────────────────
UNGOV_Y = 0.3
UNGOV_H = 3.2
UNGOV_X, UNGOV_W = 0.3, 15.4

box(UNGOV_X, UNGOV_Y, UNGOV_W, UNGOV_H, UNGOV_FILL, UNGOV_BORDER, lw=1.5,
    ls='--', radius=0.3, zorder=1)
label(UNGOV_X + UNGOV_W/2, UNGOV_Y + UNGOV_H - 0.28,
      'REST OF ESTATE',
      color=TEXT_DIM, size=10, weight='bold')

ungov_cards = [
    ('Brainiac',              '~2,100', 'L4 · RTX6000 · A16\n+AWS burst'),
    ('AWS\nNon-HPC',          '251',    'T4 · A4 · A10G'),
    ('Azure',                 '11',     'A10 · A100\nV100 · T4'),
    ('Loxo\nColorado',        '140',    'misc GPUs'),
    ('San Diego\n+ Workstns', '~88',    '4090 · RTX4000ADA\netc.'),
    ('Alcobendas',            '5',      'V100'),
]

ucard_w = 2.2
ucard_h = 2.1
ucard_y = UNGOV_Y + 0.38
total_uw = len(ungov_cards) * ucard_w + (len(ungov_cards) - 1) * 0.30
ux_start = UNGOV_X + (UNGOV_W - total_uw) / 2

for i, (name, count, detail) in enumerate(ungov_cards):
    cx = ux_start + i * (ucard_w + 0.30)
    box(cx, ucard_y, ucard_w, ucard_h, CARD_BG, UNGOV_BORDER,
        lw=1.0, radius=0.18, alpha=0.6, zorder=3)
    label(cx + ucard_w/2, ucard_y + ucard_h*0.82, name,
          color='#b0bac5', size=9, weight='bold')
    label(cx + ucard_w/2, ucard_y + ucard_h*0.57, count,
          color='#c0cad5', size=13, weight='bold')
    label(cx + ucard_w/2, ucard_y + ucard_h*0.28, detail,
          color='#c8d0da', size=7.5)

# ── LARGE STAMP over REST OF ESTATE in Lilly Red ─────────────────────────────
stamp_cx = UNGOV_X + UNGOV_W / 2
stamp_cy = UNGOV_Y + UNGOV_H / 2 - 0.1
label(stamp_cx, stamp_cy, '$$$  NOT JUSTIFIED',
      color=RED, size=34, weight='bold', zorder=8, rotation=20)

plt.tight_layout(pad=0.1)
plt.savefig('/Users/C271831/Project/compute-layer/diagram-estate-runai.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("Saved diagram-estate-runai.png")

import os
import matplotlib
matplotlib.use('Agg')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Colours (light mode) ─────────────────────────────────────────────────────
BG           = '#f7f7f7'
CLUSTER_FILL = '#ffffff'
LILY_BORDER  = '#10b981'
B300_EDGE    = '#10b981'
B300_FILL    = '#e6f7f1'
BLUE_EDGE    = '#3b5fa8'
BLUE_FILL    = '#eef2fb'
CPU_EDGE     = '#6366f1'
CPU_FILL     = '#f0f0fe'
WEKA_EDGE    = '#10b981'
WEKA_FILL    = '#e6f7f1'
TEAL         = '#0a7c57'
BLUE         = '#3b5fa8'
PURPLE       = '#6366f1'
TEXT_WHITE   = '#1a1a1a'
TEXT_DIM     = '#666666'
TEXT_GREEN   = '#0a7c57'
TEXT_BLUE    = '#1e3a7a'
TEXT_PURPLE  = '#3730a3'

# ── Canvas ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# ── Layout ───────────────────────────────────────────────────────────────────
CLUS_X, CLUS_Y = 0.35, 0.25
CLUS_W, CLUS_H = 13.3, 7.5
CLUS_TOP = CLUS_Y + CLUS_H     # 7.75

INNER_X = CLUS_X + 0.45
INNER_W = CLUS_W - 0.90        # 12.4
INNER_CX = INNER_X + INNER_W / 2

WEKA_H = 1.00;  WEKA_Y = CLUS_Y + 0.45    # Weka bar near bottom
WEKA_TOP = WEKA_Y + WEKA_H                 # 1.45

# Boxes: tighten up under subtitle
BOX_H  = 2.90
BOX_Y  = 3.50                              # moved up vs previous
BOX_TOP = BOX_Y + BOX_H                   # 6.40

N_BOXES = 5
BOX_GAP = 0.32
BOX_W   = (INNER_W - (N_BOXES - 1) * BOX_GAP) / N_BOXES   # ≈ 2.344

ARROW_MID_Y = (WEKA_TOP + BOX_Y) / 2      # midpoint of arrow gap for speed label

# ── Helpers ──────────────────────────────────────────────────────────────────
def box(x, y, w, h, fill, edge, lw=1.5, ls='-', zorder=2, radius=0.18):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
        linestyle=ls, zorder=zorder)
    ax.add_patch(rect)

def seg(x0, y0, x1, y1, color, lw=1.5, ls='-', zorder=4):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, linestyle=ls,
            solid_capstyle='round', zorder=zorder)

def bidir_vert(x, y0, y1, color, lw=2.2, head=0.16):
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(
                    arrowstyle=f'<->,head_width={head},head_length={head*0.8}',
                    color=color, lw=lw), zorder=5)

# ── Cluster box ───────────────────────────────────────────────────────────────
box(CLUS_X, CLUS_Y, CLUS_W, CLUS_H, CLUSTER_FILL, LILY_BORDER, lw=2, zorder=1)

# Title: LillyPod
ax.text(INNER_CX, CLUS_TOP - 0.28, 'LillyPod',
        color=TEXT_WHITE, fontsize=16, fontweight='bold',
        ha='center', va='top', zorder=6)

# Subtitle line 1: "Heterogeneous compute" — prominent
ax.text(INNER_CX, CLUS_TOP - 0.68, 'Heterogeneous compute',
        color=TEXT_GREEN, fontsize=11, fontweight='bold',
        ha='center', va='top', zorder=6)

# Subtitle line 2: secondary info — dim
ax.text(INNER_CX, CLUS_TOP - 1.05, 'Run:ai  ·  Air-gapped',
        color=TEXT_DIM, fontsize=8.5,
        ha='center', va='top', zorder=6)

# ── Weka FS bar ──────────────────────────────────────────────────────────────
box(INNER_X, WEKA_Y, INNER_W, WEKA_H, WEKA_FILL, WEKA_EDGE, lw=1.8, zorder=3)
ax.text(INNER_CX, WEKA_Y + WEKA_H * 0.62, 'Weka Filesystem',
        color=TEXT_WHITE, fontsize=11, fontweight='bold',
        ha='center', va='center', zorder=6)
ax.text(INNER_CX, WEKA_Y + WEKA_H * 0.25, 'Unified storage  ·  GPU Direct',
        color=TEXT_DIM, fontsize=8.5,
        ha='center', va='center', zorder=6)

# ── 800G row speed label (no decorations, shifted left of H200 path) ──────────
ax.text(5.73, ARROW_MID_Y, '800G',
        color=TEAL, fontsize=9, fontweight='bold',
        ha='center', va='center', zorder=6)

# ── Compute boxes (all in one row) ───────────────────────────────────────────
BOXES = [
    dict(label='B300',     sub='1016 ×',    edge=B300_EDGE, fill=B300_FILL,
         label_c=TEXT_GREEN,  sub_c=TEXT_GREEN,  arrow_c=TEAL),
    dict(label='H100',     sub='72 ×',      edge=BLUE_EDGE, fill=BLUE_FILL,
         label_c=TEXT_WHITE,  sub_c=TEXT_BLUE,   arrow_c=BLUE),
    dict(label='H200',     sub='64 ×',      edge=BLUE_EDGE, fill=BLUE_FILL,
         label_c=TEXT_WHITE,  sub_c=TEXT_BLUE,   arrow_c=BLUE),
    dict(label='L40s',     sub='32 ×',      edge=BLUE_EDGE, fill=BLUE_FILL,
         label_c=TEXT_WHITE,  sub_c=TEXT_BLUE,   arrow_c=BLUE),
    dict(label='CPU-only', sub='1024 cores', edge=CPU_EDGE,  fill=CPU_FILL,
         label_c=TEXT_PURPLE, sub_c=TEXT_DIM,    arrow_c=PURPLE),
]

for i, spec in enumerate(BOXES):
    bx  = INNER_X + i * (BOX_W + BOX_GAP)
    bcx = bx + BOX_W / 2

    box(bx, BOX_Y, BOX_W, BOX_H, spec['fill'], spec['edge'], lw=1.8, zorder=3)

    ax.text(bcx, BOX_Y + BOX_H * 0.68,
            spec['label'],
            color=spec['label_c'], fontsize=12, fontweight='bold',
            ha='center', va='center', zorder=6)
    ax.text(bcx, BOX_Y + BOX_H * 0.36,
            spec['sub'],
            color=spec['sub_c'], fontsize=9,
            ha='center', va='center', zorder=6)

    bidir_vert(bcx, BOX_Y, WEKA_TOP, spec['arrow_c'])

plt.tight_layout(pad=0)
plt.savefig(os.path.join(BASE_DIR, 'diagram-target-architecture.png'),
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Saved diagram-target-architecture.png")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── Colours (light mode) ─────────────────────────────────────────────────────
BG            = '#f7f7f7'
CLUSTER_FILL  = '#ffffff'
MAG_BORDER    = '#3b5fa8'
LILY_BORDER   = '#10b981'
YELLOW        = '#b07d10'
TEAL          = '#0a7c57'
BLUE          = '#3b5fa8'
TEXT_WHITE    = '#1a1a1a'
TEXT_DIM      = '#666666'
TEXT_GREEN    = '#0a7c57'
DASHED_FILL   = '#fffbe6'

# ── Canvas ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# ── Layout constants ─────────────────────────────────────────────────────────
# Cluster outer boxes
MAG_X, MAG_W = 0.4,  5.8   # MagTrain  left=0.4  right=6.2
LILY_X, LILY_W = 7.6, 5.8  # LillyPod  left=7.6  right=13.4
CLUSTER_Y, CLUSTER_H = 0.3, 7.2

# Inner box horizontal insets
INNER_PAD = 0.35
MAG_IX  = MAG_X  + INNER_PAD
MAG_IW  = MAG_W  - 2*INNER_PAD   # 5.10
LILY_IX = LILY_X + INNER_PAD
LILY_IW = LILY_W - 2*INNER_PAD

# Row heights  (bottom → top inside cluster)
GAP   = 0.30
GPU_H = 1.55
FS_H  = 1.72

# Vertical positions (y = bottom of box)
GPU_Y  = CLUSTER_Y + 0.55
ISIL_Y = GPU_Y  + GPU_H + GAP
WEKA_Y = ISIL_Y + FS_H  + GAP      # MagTrain dashed Weka top row

# Computed centres
mag_cx   = MAG_IX  + MAG_IW  / 2
lily_cx  = LILY_IX + LILY_IW / 2
weka_mid = WEKA_Y  + FS_H / 2      # y-centre of Weka row

# ── Helper: rounded rect ──────────────────────────────────────────────────────
def box(x, y, w, h, fill, edge, lw=1.5, ls='-', zorder=2, alpha=1.0, radius=0.18):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
        linestyle=ls, zorder=zorder, alpha=alpha
    )
    ax.add_patch(rect)
    return rect

# ── Helper: line segment ──────────────────────────────────────────────────────
def seg(x0, y0, x1, y1, color, lw=2.0, ls='-', zorder=4):
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, linestyle=ls,
            solid_capstyle='round', zorder=zorder)

# ── Helper: bidirectional vertical arrow ────────────────────────────────────
def bidir_vert(x, y0, y1, color, lw=2.5, head=0.18):
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle=f'<->,head_width={head},head_length={head*0.8}',
                                color=color, lw=lw), zorder=5)

# ── Helper: filled triangle arrowhead ────────────────────────────────────────
import numpy as np
def tri_arrow(tip_x, tip_y, direction, color, size=0.16, zorder=6):
    """Draw a filled triangle arrowhead. direction: 'left','right','up','down'."""
    s, h = size * 0.55, size  # half-base, length
    if direction == 'left':
        pts = [(tip_x, tip_y), (tip_x+h, tip_y+s), (tip_x+h, tip_y-s)]
    elif direction == 'right':
        pts = [(tip_x, tip_y), (tip_x-h, tip_y+s), (tip_x-h, tip_y-s)]
    elif direction == 'down':
        pts = [(tip_x, tip_y), (tip_x-s, tip_y+h), (tip_x+s, tip_y+h)]
    elif direction == 'up':
        pts = [(tip_x, tip_y), (tip_x-s, tip_y-h), (tip_x+s, tip_y-h)]
    poly = mpatches.Polygon(pts, closed=True, facecolor=color, edgecolor=color, zorder=zorder)
    ax.add_patch(poly)

# ── CLUSTER BOXES ─────────────────────────────────────────────────────────────
box(MAG_X,  CLUSTER_Y, MAG_W,  CLUSTER_H, CLUSTER_FILL, MAG_BORDER,  lw=2, zorder=1)
box(LILY_X, CLUSTER_Y, LILY_W, CLUSTER_H, CLUSTER_FILL, LILY_BORDER, lw=2, zorder=1)

# Cluster labels
ax.text(MAG_X  + MAG_W/2,  CLUSTER_Y + CLUSTER_H - 0.28, 'MagTrain',
        color=TEXT_WHITE, fontsize=15, fontweight='bold', ha='center', va='top', zorder=6)
ax.text(MAG_X  + MAG_W/2,  CLUSTER_Y + CLUSTER_H - 0.62, 'Slurm · Internet access',
        color=TEXT_DIM, fontsize=9, ha='center', va='top', zorder=6)

ax.text(LILY_X + LILY_W/2, CLUSTER_Y + CLUSTER_H - 0.28, 'LillyPod',
        color=TEXT_WHITE, fontsize=15, fontweight='bold', ha='center', va='top', zorder=6)
ax.text(LILY_X + LILY_W/2, CLUSTER_Y + CLUSTER_H - 0.62, 'Run:ai · Air-gapped',
        color=TEXT_GREEN, fontsize=9, ha='center', va='top', zorder=6,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#e6f7f1', edgecolor='#10b981', linewidth=0.8))

# ── MAGTRAIN INNER BOXES ──────────────────────────────────────────────────────
# Row 1 (top): Weka NFS mount — dashed
box(MAG_IX, WEKA_Y, MAG_IW, FS_H, DASHED_FILL, YELLOW, lw=1.5, ls='--', zorder=3)
ax.text(mag_cx, WEKA_Y + FS_H*0.62, 'Weka FS  (NFS mount)',
        color=YELLOW, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(mag_cx, WEKA_Y + FS_H*0.35, 'appears local — but is not',
        color=TEXT_DIM, fontsize=8.5, ha='center', va='center', style='italic', zorder=6)
ax.text(mag_cx, WEKA_Y + FS_H*0.12,
        'GPU idle waiting on IO if not careful',
        color='#c0392b', fontsize=8, ha='center', va='center', zorder=6)

# Row 2: Isilon filesystem — solid
box(MAG_IX, ISIL_Y, MAG_IW, FS_H, CLUSTER_FILL, MAG_BORDER, lw=1.5, zorder=3)
ax.text(mag_cx, ISIL_Y + FS_H*0.50, 'Isilon Filesystem',
        color=TEXT_WHITE, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)

# Row 3 (bottom): GPU box
box(MAG_IX, GPU_Y, MAG_IW, GPU_H, CLUSTER_FILL, MAG_BORDER, lw=1.5, zorder=3)
ax.text(mag_cx, GPU_Y + GPU_H*0.70, 'GPUs',
        color=TEXT_WHITE, fontsize=12, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(mag_cx, GPU_Y + GPU_H*0.38, '72 × H100   64 × H200   32 × L40s',
        color=TEXT_DIM, fontsize=8.5, ha='center', va='center', zorder=6)

# ── LILLYPOD INNER BOXES ──────────────────────────────────────────────────────
# Row 1 (top): Weka FS — solid  (aligned with MagTrain Weka row)
box(LILY_IX, WEKA_Y, LILY_IW, FS_H, CLUSTER_FILL, LILY_BORDER, lw=1.5, zorder=3)
ax.text(lily_cx, WEKA_Y + FS_H*0.55, 'Weka Filesystem',
        color=TEXT_WHITE, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(lily_cx, WEKA_Y + FS_H*0.30, 'GPU Direct',
        color=TEXT_DIM, fontsize=8.5, ha='center', va='center', zorder=6)

# Row 2 (bottom): GPU box  — same GPU_Y as MagTrain
box(LILY_IX, GPU_Y, LILY_IW, GPU_H, CLUSTER_FILL, LILY_BORDER, lw=1.5, zorder=3)
ax.text(lily_cx, GPU_Y + GPU_H*0.70, 'GPUs',
        color=TEXT_WHITE, fontsize=12, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(lily_cx, GPU_Y + GPU_H*0.38, '1016 × B300',
        color=TEXT_GREEN, fontsize=10, ha='center', va='center', zorder=6)

# ── ARROWS ────────────────────────────────────────────────────────────────────

# 1. Isilon ↔ GPU (blue, bidirectional, MagTrain centre)
isil_bot = ISIL_Y
gpu_top  = GPU_Y + GPU_H
bidir_vert(mag_cx, isil_bot, gpu_top, BLUE)
ax.text(mag_cx + 0.18, (isil_bot + gpu_top)/2, '400G',
        color=BLUE, fontsize=8.5, ha='left', va='center', fontweight='bold', zorder=6)

# 2. Yellow 10G path: starts at LillyPod Weka left edge, horizontal to nfs_drop_x,
#    then straight down to MagTrain GPU top. Bidirectional, dashed (slow link).
nfs_drop_x    = MAG_IX + MAG_IW * 0.75   # 25% from right of dashed box
lily_weka_left = LILY_IX
weka_bot       = WEKA_Y
isil_top       = ISIL_Y + FS_H
isil_bot2      = ISIL_Y
gpu_top2       = GPU_Y + GPU_H

# All segments dashed to convey slow/NFS path
seg(lily_weka_left, weka_mid, nfs_drop_x, weka_mid, YELLOW, lw=2.5, ls='--')   # horizontal
seg(nfs_drop_x, weka_mid,  nfs_drop_x, weka_bot,   YELLOW, lw=2.5, ls='--')   # inside dashed box
seg(nfs_drop_x, weka_bot,  nfs_drop_x, isil_top,   YELLOW, lw=2.5, ls='--')   # gap
seg(nfs_drop_x, isil_top,  nfs_drop_x, isil_bot2,  YELLOW, lw=2.5, ls='--')   # through Isilon
seg(nfs_drop_x, isil_bot2, nfs_drop_x, gpu_top2,   YELLOW, lw=2.5, ls='--')   # gap → GPU top

# Arrowheads at both terminals (bidirectional)
tri_arrow(lily_weka_left, weka_mid, 'right', YELLOW, size=0.09)   # → into LillyPod Weka
tri_arrow(nfs_drop_x, gpu_top2, 'down', YELLOW, size=0.09)        # → into MagTrain GPU

# Label at the 90-degree elbow
ax.text(nfs_drop_x + 0.14, weka_mid + 0.18, '10G',
        color=YELLOW, fontsize=8.5, ha='left', va='bottom', fontweight='bold', zorder=6)

# 3. LillyPod Weka ↔ GPU (teal, bidirectional)
lily_weka_bot = WEKA_Y
lily_gpu_top  = GPU_Y + GPU_H
bidir_vert(lily_cx, lily_weka_bot, lily_gpu_top, TEAL)
ax.text(lily_cx + 0.18, (lily_weka_bot + lily_gpu_top)/2, '800G',
        color=TEAL, fontsize=8.5, ha='left', va='center', fontweight='bold', zorder=6)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(7.0, 7.82, 'Current Architecture',
        color='#1a1a1a', fontsize=14, fontweight='bold', ha='center', va='top', zorder=6)

plt.tight_layout(pad=0)
plt.savefig('/Users/C271831/Project/compute-layer/diagram-current-architecture.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Saved diagram-current-architecture.png")

"""
diagram_venn.py — Two-person card for slide 5: AIR + Digital Core = Trusted Advisor Team
Recolors Picture1.png (Lilly template avatar) per team using PIL colorize.
Output: diagram_venn.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image, ImageOps
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMERALD  = '#10b981'
BLUE     = '#3b82f6'
INDIGO   = '#6366f1'
LIGHT_BG = '#f7f7f7'


def tint_avatar(path, dark_color, light_color='#f7f7f7'):
    """Recolor avatar: dark pixels → dark_color, light pixels → light_color."""
    img   = Image.open(path).convert('RGBA')
    alpha = img.split()[3]
    gray  = img.convert('L')
    tinted = ImageOps.colorize(gray, black=dark_color, white=light_color)
    tinted = tinted.convert('RGBA')
    tinted.putalpha(alpha)
    return np.array(tinted) / 255.0


def place_avatar(ax, arr, cx, cy, size):
    ax.imshow(arr, extent=[cx - size/2, cx + size/2, cy - size/2, cy + size/2],
              aspect='auto', zorder=5)


fig, ax = plt.subplots(figsize=(13, 4.2), facecolor=LIGHT_BG)
ax.set_facecolor(LIGHT_BG)
ax.axis('off')
ax.set_xlim(0, 13)
ax.set_ylim(0, 4.2)

air_avatar = tint_avatar(os.path.join(BASE_DIR, 'assets', 'Picture1.png'), EMERALD)
dc_avatar  = tint_avatar(os.path.join(BASE_DIR, 'assets', 'Picture1.png'), BLUE)

icon_size = 1.50
icon_cy   = 3.10

# AIR
place_avatar(ax, air_avatar, 4.5, icon_cy, icon_size)
ax.text(4.5, icon_cy - icon_size / 2 - 0.20, 'AIR',
        ha='center', va='top', fontsize=17, fontweight='bold', color=EMERALD, zorder=6)

# Digital Core
place_avatar(ax, dc_avatar, 8.5, icon_cy, icon_size)
ax.text(8.5, icon_cy - icon_size / 2 - 0.20, 'Digital Core',
        ha='center', va='top', fontsize=17, fontweight='bold', color=BLUE, zorder=6)

# Together — divider line + plain text
ax.plot([3.2, 9.8], [0.95, 0.95], color=INDIGO, lw=1.0, alpha=0.30, zorder=4)
ax.text(6.5, 0.62, 'Trusted Advisor Team to LRL teams',
        ha='center', va='center', fontsize=13, fontweight='bold', color=INDIGO, zorder=5)

plt.tight_layout(pad=0.2)
plt.savefig(os.path.join(BASE_DIR, 'diagram_venn.png'), dpi=200, facecolor=LIGHT_BG, bbox_inches='tight')
print('saved diagram_venn.png')

"""
diagram_dag.py — Generates the compute-tier card diagram for slide 2.
Ported directly from 04-10-2026/gen_slides.py slide_02() card logic.
No "COMPUTE LAYER" label or footer caption.
Output: diagram_dag.png (2880 x 925 px)
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

W, H = 2880, 520

LIGHT_BG  = '#f7f7f7'
WHITE     = '#ffffff'
EMERALD   = '#10b981'

FONT_BLACK   = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
FONT_BOLD    = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def font(path, size):
    return ImageFont.truetype(path, size)

def draw_rounded_rect(draw, x, y, w, h, radius, fill):
    draw.rounded_rectangle([(x, y), (x + w, y + h)],
                            radius=radius, fill=hex2rgb(fill))

img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
draw = ImageDraw.Draw(img)

cards = [
    ('#64748b', 'PREPROCESSING',  'Pre/post-processing work\nNon-GPU-accelerated\napplications'),
    ('#7c3aed', 'SIMULATION',     'Physics-based simulation\ne.g. molecular dynamics\nGPU-accelerated, distinct profile'),
    ('#3b82f6', 'INFERENCE',      'Applying trained models\nHigh throughput'),
    (EMERALD,   'TRAINING',       'Building and fine-tuning\nmodels\nComputationally intensive'),
    ('#f59e0b', 'DATA MOVEMENT',  'First-class concern\nVolume can be large\nEgress cost matters on hybrid infra'),
]

n        = len(cards)
margin_x = 95
margin_y = 60
card_gap = 28
card_w   = (W - 2 * margin_x - (n - 1) * card_gap) // n
card_h   = 390
radius   = 18

for i, (color, title, body) in enumerate(cards):
    cx = margin_x + i * (card_w + card_gap)
    cy = margin_y

    draw_rounded_rect(draw, cx, cy, card_w, card_h, radius, color)

    f_title = font(FONT_BLACK, 34)
    draw.text((cx + 28, cy + 28), title, fill=hex2rgb(WHITE), font=f_title)

    div_y = cy + 82
    draw.rectangle([(cx + 28, div_y), (cx + card_w - 28, div_y + 2)],
                   fill=(255, 255, 255, 80))

    f_body = font(FONT_REGULAR, 30)
    by = div_y + 24
    for line in body.split('\n'):
        draw.text((cx + 28, by), line,
                  fill=(255, 255, 255, 220), font=f_body)
        by += 46

img.save(os.path.join(BASE_DIR, 'diagram_dag.png'))
print('saved diagram_dag.png')

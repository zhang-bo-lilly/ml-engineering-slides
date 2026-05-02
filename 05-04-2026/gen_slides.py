import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 2880, 1620
MARGIN = 194
BOTTOM_BAR = 18
BREADCRUMB = 'AIOS  ·  ADVANCED INTELLIGENCE & RESEARCH  ·  ELI LILLY'

_fcache = {}

def _font(name, size):
    key = (name, size)
    if key in _fcache:
        return _fcache[key]
    paths = {
        'Arial-Black': [
            '/System/Library/Fonts/Supplemental/Arial Black.ttf',
            '/Library/Fonts/Arial Black.ttf',
        ],
        'Arial-Bold': [
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
            '/Library/Fonts/Arial Bold.ttf',
        ],
        'Arial': [
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/Library/Fonts/Arial.ttf',
        ],
    }
    for p in paths.get(name, []):
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            _fcache[key] = f
            return f
    f = ImageFont.load_default(size)
    _fcache[key] = f
    return f


def _chrome(draw):
    draw.text((MARGIN, 139), BREADCRUMB, font=_font('Arial-Bold', 28),
              fill='#d32030', anchor='lm')
    draw.rectangle([0, H - BOTTOM_BAR, W, H], fill='#d32030')


def _hero(draw, line1, line2, dark=False):
    fh = _font('Arial-Black', 110)
    c1 = '#ffffff' if dark else '#1a1a1a'
    y = 189
    bb1 = draw.textbbox((0, 0), line1, font=fh)
    h1 = bb1[3] - bb1[1]
    draw.text((MARGIN, y), line1, font=fh, fill=c1)
    y2 = y + h1 + 7
    bb2 = draw.textbbox((0, 0), line2, font=fh)
    h2 = bb2[3] - bb2[1]
    draw.text((MARGIN, y2), line2, font=fh, fill='#d32030')
    return y2 + h2


def slide_01():
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)
    _chrome(draw)
    hero_bottom = _hero(draw, 'Three clusters, three fabrics.', 'One team.')

    diag = Image.open(os.path.join(BASE_DIR, 'diagram_clusters.png'))
    dw, dh = diag.size

    content_top = hero_bottom + 36
    content_bottom = H - BOTTOM_BAR - 24
    avail_h = content_bottom - content_top
    avail_w = W - 2 * MARGIN

    scale = min(1.0, avail_h / dh, avail_w / dw)
    if scale < 1.0:
        diag = diag.resize((int(dw * scale), int(dh * scale)), Image.LANCZOS)
        dw, dh = diag.size

    dy = content_top + (avail_h - dh) // 2
    img.paste(diag, (MARGIN, dy))

    out = os.path.join(BASE_DIR, 'slide_01.png')
    img.save(out)
    print(f'saved {out}')


def _wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        if draw.textlength(test, font=font) <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(' '.join(cur))
            cur = [w]
    if cur:
        lines.append(' '.join(cur))
    return lines


def slide_02():
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)
    _chrome(draw)
    hero_bottom = _hero(draw, 'The unit of value:', 'the workflow.')

    bullets = [
        ('Scientific AI is a pipeline',
         'Raw data, featurization, model training, and simulation are interconnected steps — each feeding the others, all demanding shared, fast data access.'),
        ('Islands break the pipeline',
         'Manual staging between clusters, NFS bottlenecks, and separate schedulers add latency at every hand-off.'),
        ('One platform changes what is possible',
         'A single fabric and filesystem let the workflow — not the job — become the unit of optimization.'),
    ]

    ACCENT_W = 6
    ACCENT_GAP = 24
    TEXT_X = MARGIN + ACCENT_W + ACCENT_GAP
    TEXT_W = W - TEXT_X - MARGIN

    content_top = hero_bottom + 80
    content_bottom = H - BOTTOM_BAR - 40

    ft = _font('Arial-Black', 46)
    fb = _font('Arial', 36)

    # Measure all block heights first
    block_data = []
    for title, body in bullets:
        bb_t = draw.textbbox((0, 0), title, font=ft)
        th = bb_t[3] - bb_t[1]
        lines = _wrap(draw, body, fb, TEXT_W)
        block_h = th + 10 + len(lines) * 46
        block_data.append((title, lines, th, block_h))

    # Distribute evenly across available height
    total_block_h = sum(d[3] for d in block_data)
    gap = (content_bottom - content_top - total_block_h) / (len(block_data) + 1)
    ty = content_top + gap

    for title, lines, th, block_h in block_data:
        draw.rectangle([MARGIN, ty, MARGIN + ACCENT_W, ty + block_h], fill='#d32030')
        draw.text((TEXT_X, ty), title, font=ft, fill='#1a1a1a')
        by = ty + th + 10
        for line in lines:
            draw.text((TEXT_X, by), line, font=fb, fill='#333333')
            by += 46
        ty += block_h + gap

    out = os.path.join(BASE_DIR, 'slide_02.png')
    img.save(out)
    print(f'saved {out}')


def slide_03():
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)
    _chrome(draw)
    hero_bottom = _hero(draw, 'Five moves.', 'One platform.')

    cards = [
        ('01', 'Migrate MagTrain into LillyPod',
         'Connect all MagTrain GPUs (72×H100, 64×H200, 32×L40S) to the 800G Weka fabric — eliminates the NFS bottleneck.'),
        ('02', 'Add 4K CPU cores for bioinformatics',
         '16 × Dell R7625 (256 cores, 4TB RAM each) to run mmseqs, jackhmmer, and CPU-heavy pipeline steps natively on platform.'),
        ('03', 'Add 256 RTX 6000 Blackwell to LillyPod',
         '32 × 8-way servers for physics-based simulation steps that are part of the scientific-AI workflow.'),
        ('04', 'Expand Weka storage',
         '+2PB hot tier, +3PB warm tier. Growing from 4PB/7PB to 6PB/10PB on the 800G fabric.'),
        ('05', 'Expand MD3 now, integrate over time',
         'Near-term: deploy the additional 256 RTX 6000 Pro GPUs into MD3 to meet business demand. Over time: migrate onto the Weka fabric — Slurm-managed is acceptable, but a fast storage fabric is required.'),
    ]

    BORDER = 5
    PAD = 24
    BODY_LEAD = 38
    card_w = W - 2 * MARGIN
    CONTENT_TOP = hero_bottom + 44
    CONTENT_BOTTOM = H - BOTTOM_BAR - 40

    fn_num = _font('Arial-Bold', 26)
    fn_title = _font('Arial-Black', 48)
    fn_body = _font('Arial', 28)

    # Measure natural height for each card
    measured = []
    for num, title, body in cards:
        num_h = draw.textbbox((0, 0), num, font=fn_num)[3] - draw.textbbox((0, 0), num, font=fn_num)[1]
        title_h = draw.textbbox((0, 0), title, font=fn_title)[3] - draw.textbbox((0, 0), title, font=fn_title)[1]
        body_lines = _wrap(draw, body, fn_body, card_w - PAD * 2)
        card_h = BORDER + PAD + num_h + 10 + title_h + 12 + len(body_lines) * BODY_LEAD + PAD
        measured.append((num, title, body_lines, num_h, title_h, card_h))

    total_card_h = sum(m[5] for m in measured)
    avail_h = CONTENT_BOTTOM - CONTENT_TOP
    gap = max(8, (avail_h - total_card_h) // (len(measured) + 1))

    cy = CONTENT_TOP + gap
    for num, title, body_lines, num_h, title_h, card_h in measured:
        cx = MARGIN
        draw.rectangle([cx, cy, cx + card_w, cy + card_h], fill='#ffffff',
                       outline='#f3f4f6', width=1)
        draw.rectangle([cx, cy, cx + card_w, cy + BORDER], fill='#d32030')

        ty = cy + BORDER + PAD
        draw.text((cx + PAD, ty), num, font=fn_num, fill='#d32030')
        ty += num_h + 10
        draw.text((cx + PAD, ty), title, font=fn_title, fill='#1a1a1a')
        ty += title_h + 12
        for line in body_lines:
            draw.text((cx + PAD, ty), line, font=fn_body, fill='#333333')
            ty += BODY_LEAD

        cy += card_h + gap

    out = os.path.join(BASE_DIR, 'slide_03.png')
    img.save(out)
    print(f'saved {out}')


def assemble_pptx():
    from pptx import Presentation
    from pptx.util import Pt

    prs = Presentation()
    prs.slide_width = Pt(W * 72 / 96)
    prs.slide_height = Pt(H * 72 / 96)
    blank = prs.slide_layouts[6]

    for i in range(1, 4):
        slide = prs.slides.add_slide(blank)
        png = os.path.join(BASE_DIR, f'slide_0{i}.png')
        slide.shapes.add_picture(png, 0, 0, prs.slide_width, prs.slide_height)

    out = os.path.join(BASE_DIR, 'deck.pptx')
    prs.save(out)
    print(f'saved {out}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--slide', type=int, default=0,
                        help='0=all+pptx, 1-3=single slide')
    args = parser.parse_args()

    for script in ['diagram_clusters.py']:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, script)], check=True)

    if args.slide == 0:
        slide_01(); slide_02(); slide_03()
        assemble_pptx()
    elif args.slide == 1:
        slide_01()
    elif args.slide == 2:
        slide_02()
    elif args.slide == 3:
        slide_03()

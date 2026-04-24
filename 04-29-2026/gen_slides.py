import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

W, H = 2880, 1620

C = {
    'bg':      (247, 247, 247),
    'dark':    (26,  26,  26),
    'red':     (228, 0,   43),
    'gray':    (51,  51,  51),
    'caption': (153, 153, 153),
    'blue':    (59,  130, 246),
    'emerald': (16,  185, 129),
    'white':   (255, 255, 255),
}

BREADCRUMB = 'LILLYPOD UPDATE  ·  ADVANCED INTELLIGENCE  ·  ELI LILLY'

_fcache = {}

def _font(name, size):
    key = (name, size)
    if key in _fcache:
        return _fcache[key]
    paths = {
        'Arial Black': [
            '/Library/Fonts/Arial Black.ttf',
            '/System/Library/Fonts/Supplemental/Arial Black.ttf',
        ],
        'Arial Bold': [
            '/Library/Fonts/Arial Bold.ttf',
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        ],
        'Arial': [
            '/Library/Fonts/Arial.ttf',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
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


def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = ' '.join(cur + [word])
        if draw.textlength(test, font=fnt) > max_w and cur:
            lines.append(' '.join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(' '.join(cur))
    return lines


def line_height(draw, fnt, extra=8):
    bb = draw.textbbox((0, 0), 'Ag', font=fnt)
    return bb[3] - bb[1] + extra


def new_canvas():
    img = Image.new('RGB', (W, H), C['bg'])
    return img, ImageDraw.Draw(img)


def chrome(draw):
    draw.text((95, 52), BREADCRUMB, font=_font('Arial', 28), fill=C['red'], anchor='lm')
    draw.rectangle([(0, H - 18), (W, H)], fill=C['red'])


def hero(draw, line1, line2, y=130, size=110):
    f = _font('Arial Black', size)
    draw.text((120, y), line1, font=f, fill=C['dark'], anchor='lt')
    bb = draw.textbbox((0, 0), line1, font=f)
    lh = bb[3] - bb[1] + 14
    draw.text((120, y + lh), line2, font=f, fill=C['red'], anchor='lt')


def save_slide(img, name):
    p = os.path.join(BASE_DIR, name)
    img.save(p)
    print(f'  -> {p}')
    return p


def fmt_hours(h):
    if h >= 1000:
        return f'{h / 1000:.0f}K'
    return f'{h:.0f}'


def load_metrics():
    path = os.path.join(BASE_DIR, 'metrics.json')
    if not os.path.exists(path):
        raise FileNotFoundError(
            'metrics.json not found — run extract_metrics.py first'
        )
    with open(path) as f:
        return json.load(f)


# ── Slide 01 ──────────────────────────────────────────────────────────────

def slide_01(metrics):
    img, draw = new_canvas()
    chrome(draw)
    hero(draw, 'LillyPod,', 'by the numbers.')

    stats = [
        (str(metrics['projects']),         'active projects'),
        (str(metrics['users']),            'registered users'),
        (metrics['workloads_label'],       'workloads completed'),
        (metrics['cloud_cost_label'],      'equivalent cloud value'),
    ]
    margin = 120
    gap = 40
    tile_w = (W - 2 * margin - 3 * gap) // 4   # 630
    tile_h = 250
    tile_y = 450

    for i, (num, label) in enumerate(stats):
        tx = margin + i * (tile_w + gap)
        draw.rectangle([(tx, tile_y), (tx + tile_w, tile_y + tile_h)], fill=C['white'])
        draw.rectangle([(tx, tile_y), (tx + tile_w, tile_y + 5)], fill=C['red'])

        fn = _font('Arial Black', 110)
        nb = draw.textbbox((0, 0), num, font=fn)
        nw, nh = nb[2] - nb[0], nb[3] - nb[1]
        nx = tx + (tile_w - nw) // 2 - nb[0]
        ny = tile_y + (tile_h - nh) // 2 - 22 - nb[1]
        draw.text((nx, ny), num, font=fn, fill=C['dark'])

        fl = _font('Arial', 30)
        lb = draw.textbbox((0, 0), label, font=fl)
        lw = lb[2] - lb[0]
        draw.text((tx + (tile_w - lw) // 2, tile_y + tile_h - 44),
                  label, font=fl, fill=C['caption'])

    # Time-series chart
    chart = Image.open(os.path.join(BASE_DIR, 'timeseries.png')).convert('RGB')
    chart_y = tile_y + tile_h + 48
    chart_w = W - 2 * margin
    chart_h = int(chart_w * chart.height / chart.width)
    chart = chart.resize((chart_w, chart_h), Image.LANCZOS)
    img.paste(chart, (margin, chart_y))

    # Caption — use date range from metrics
    since = metrics.get('since_date', '')
    fc = _font('Arial', 28)
    cap_y = chart_y + chart_h + 16
    draw.text((W // 2, cap_y),
              f'Daily workload submissions · {since} – present',
              font=fc, fill=C['caption'], anchor='mt')

    return save_slide(img, 'slide_01.png')


# ── Slide 02 ──────────────────────────────────────────────────────────────

SQUADS = [
    {
        'name': 'alchemy',
        'type': 'internal',
        'statement': (
            'Scaling genomic language models to full training capacity '
            'to enable genome-wide impact prediction for human genetic variation.'
        ),
    },
    {
        'name': 'large-mol',
        'type': 'internal',
        'statement': (
            'Training protein folding and design models on all publicly available '
            'protein structures to accelerate in-silico protein design campaigns.'
        ),
    },
    {
        'name': 'small-mol',
        'type': 'internal',
        'statement': (
            'Pre-training a graph-based molecular foundation model on over one billion '
            'molecules to enable generalizable property prediction across diverse chemical space.'
        ),
    },
    {
        'name': 'tunelab-ai',
        'type': 'external',
        'statement': (
            'Training chemistry and antibody molecular models and developing a universal '
            'protein–small molecule binding model to advance computational drug design.'
        ),
    },
]


def _squad_card(draw, sq, x, y, w, gpu_h):
    color = C['emerald'] if sq['type'] == 'external' else C['blue']

    pad = 18
    fhdr = _font('Arial Bold', 38)
    fbod = _font('Arial', 26)
    fstat = _font('Arial Black', 34)
    header_h = 62

    # Measure content to size card to fit
    lines = wrap_text(draw, sq['statement'], fbod, w - 2 * pad)
    lh = line_height(draw, fbod)
    body_h = len(lines) * lh
    stat_h = draw.textbbox((0, 0), '000K GPU-hrs', font=fstat)[3] - \
             draw.textbbox((0, 0), '000K GPU-hrs', font=fstat)[1]
    card_h = header_h + pad + body_h + pad + stat_h + pad

    # Card background
    draw.rectangle([(x, y), (x + w, y + card_h)], fill=C['white'])

    # Header strip
    draw.rectangle([(x, y), (x + w, y + header_h)], fill=color)
    draw.text((x + pad, y + header_h // 2), sq['name'], font=fhdr, fill=C['white'], anchor='lm')

    # External badge
    if sq['type'] == 'external':
        badge = 'External'
        fb = _font('Arial', 22)
        bw = int(draw.textlength(badge, font=fb)) + 20
        bh = 30
        bx = x + w - bw - 14
        by = y + (header_h - bh) // 2
        draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=6, fill=C['white'])
        draw.text((bx + bw // 2, by + bh // 2), badge, font=fb, fill=color, anchor='mm')

    # Body text
    ty = y + header_h + pad
    for line in lines:
        draw.text((x + pad, ty), line, font=fbod, fill=C['gray'])
        ty += lh

    # GPU-hours stat
    draw.text((x + w - pad, ty + pad),
              f'{fmt_hours(gpu_h)} GPU-hrs',
              font=fstat, fill=C['dark'], anchor='rt')


def slide_02(metrics):
    img, draw = new_canvas()
    chrome(draw)
    hero(draw, 'One cluster,', 'touching every part of the business.')

    chart = Image.open(os.path.join(BASE_DIR, 'projects_gpuhours.png')).convert('RGB')
    margin = 120
    chart_w = W - 2 * margin
    chart_h = int(chart_w * chart.height / chart.width)
    img.paste(chart.resize((chart_w, chart_h), Image.LANCZOS), (margin, 430))

    return save_slide(img, 'slide_02.png')


# ── Slide 03 ──────────────────────────────────────────────────────────────

CTAS = [
    {
        'title': 'Not on LillyPod yet?',
        'body': (
            "If you're in AIR but not yet running workloads, now is the time to think about "
            "where GPU compute fits in your roadmap. Getting started is simpler than you think "
            "— reach out and we'll set you up."
        ),
    },
    {
        'title': "Onboarded but haven't run workloads yet?",
        'body': (
            'Active workloads help keep the cluster healthy for everyone. '
            'The more of us running jobs, the more we cover each other. '
            'The cluster is ready — we\'re here to help you get your first job running.'
        ),
    },
    {
        'title': 'Bring your partners along.',
        'body': (
            'Working with teams outside AIR who could benefit from GPU compute? '
            'Introduce them to LillyPod. Every new user adds coverage '
            '— helping them is helping all of us.'
        ),
    },
]


def slide_03():
    img, draw = new_canvas()
    chrome(draw)
    hero(draw, 'Not everyone has access like this.', 'At its best when we all use it.')

    margin = 120
    cta_top = 400
    card_gap = 44
    card_w = W - 2 * margin
    pad_v = 80
    pad_h = 30

    fn = _font('Arial Bold', 26)
    ft = _font('Arial Bold', 52)
    fb = _font('Arial', 34)
    lh_title = line_height(draw, ft, extra=10)
    lh_body = line_height(draw, fb, extra=8)
    text_w = card_w - 2 * pad_h

    cy = cta_top
    for i, cta in enumerate(CTAS):
        num_bb = draw.textbbox((0, 0), f'0{i + 1}', font=fn)
        num_h = num_bb[3] - num_bb[1]
        title_lines = wrap_text(draw, cta['title'], ft, text_w)
        body_lines = wrap_text(draw, cta['body'], fb, text_w)

        card_h = (5 + pad_v
                  + num_h + 8
                  + len(title_lines) * lh_title
                  + 14
                  + len(body_lines) * lh_body
                  + pad_v)

        draw.rectangle([(margin, cy), (margin + card_w, cy + card_h)], fill=C['white'])
        draw.rectangle([(margin, cy), (margin + card_w, cy + 5)], fill=C['red'])

        iy = cy + 5 + pad_v
        draw.text((margin + pad_h, iy), f'0{i + 1}', font=fn, fill=C['red'])
        iy += num_h + 8

        for line in title_lines:
            draw.text((margin + pad_h, iy), line, font=ft, fill=C['dark'])
            iy += lh_title
        iy += 14

        for line in body_lines:
            draw.text((margin + pad_h, iy), line, font=fb, fill=C['gray'])
            iy += lh_body

        cy += card_h + card_gap

    return save_slide(img, 'slide_03.png')


# ── PPTX assembly ─────────────────────────────────────────────────────────

def assemble_pptx(slide_paths, filename='LillyPod_Update_20260429.pptx'):
    prs = Presentation()
    prs.slide_width = Emu(12192000)    # 13.333"
    prs.slide_height = Emu(6858000)    # 7.5"
    blank = prs.slide_layouts[6]
    for path in slide_paths:
        sl = prs.slides.add_slide(blank)
        sl.shapes.add_picture(path, 0, 0, prs.slide_width, prs.slide_height)
    out = os.path.join(BASE_DIR, filename)
    prs.save(out)
    print(f'  -> {out}')
    return out


# ── Entry point ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Extracting metrics...')
    subprocess.run([sys.executable, os.path.join(BASE_DIR, 'extract_metrics.py')], check=True)

    print('Running diagram generators...')
    for script in ['diagram_timeseries.py', 'diagram_projects.py']:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, script)], check=True)

    metrics = load_metrics()

    print('Building slides...')
    slides = [
        slide_01(metrics),
        slide_02(metrics),
        slide_03(),
    ]

    print('Assembling pptx...')
    assemble_pptx(slides)
    print('Done.')

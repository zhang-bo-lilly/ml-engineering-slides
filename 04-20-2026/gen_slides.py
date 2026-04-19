"""
gen_slides.py — Generates all 5 slides for the Scientific AI CoE deck.
Canvas: 2880 × 1620 px, 16:9
Output: slide_01.png through slide_05.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2880, 1620

DARK_BG   = '#1a2035'
LIGHT_BG  = '#f7f7f7'
LILLY_RED = '#e4002b'
WHITE     = '#ffffff'
DARK      = '#1a1a1a'
BULLETS   = '#333333'
CAPTION   = '#999999'
MID_GRAY  = '#555555'
EMERALD   = '#10b981'
INDIGO    = '#6366f1'
BLUE      = '#3b82f6'

FONT_BLACK   = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
FONT_BOLD    = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

BREADCRUMB = 'SCIENTIFIC AI COE  \u00b7  AIR + DIGITAL CORE  \u00b7  ELI LILLY'


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def fnt(path, size):
    return ImageFont.truetype(path, size)


def make_slide(bg):
    img = Image.new('RGB', (W, H), hex2rgb(bg))
    draw = ImageDraw.Draw(img)
    return img, draw


def draw_chrome(draw):
    f = fnt(FONT_REGULAR, 28)
    draw.text((95, 52), BREADCRUMB, fill=hex2rgb(LILLY_RED), font=f)
    draw.rectangle([(0, H - 18), (W, H)], fill=hex2rgb(LILLY_RED))


def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines, current = [], ''
    for word in words:
        test = (current + ' ' + word).strip()
        if draw.textlength(test, font=f) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, f, x, y, max_width, fill, line_h):
    lines = wrap_text(draw, text, f, max_width)
    c = hex2rgb(fill) if isinstance(fill, str) else fill
    for line in lines:
        draw.text((x, y), line, fill=c, font=f)
        y += line_h
    return y


def text_height(draw, text, f, max_width, line_h):
    lines = wrap_text(draw, text, f, max_width)
    return len(lines) * line_h


# ── Slide 1 — Dark Anchor ────────────────────────────────────────────────────
def slide_01():
    img, draw = make_slide(DARK_BG)
    draw_chrome(draw)

    f_hero = fnt(FONT_BLACK, 118)
    f_sub  = fnt(FONT_REGULAR, 48)

    l1  = 'A Center of Excellence'
    l2  = 'for Scientific AI Compute.'
    sub = 'A Joint Initiative for AIR and Digital Core'

    bb1 = draw.textbbox((0, 0), l1, font=f_hero)
    bb2 = draw.textbbox((0, 0), l2, font=f_hero)
    bbs = draw.textbbox((0, 0), sub, font=f_sub)

    h1 = bb1[3] - bb1[1]
    h2 = bb2[3] - bb2[1]
    hs = bbs[3] - bbs[1]
    total_h = h1 + 20 + h2 + 56 + hs

    y = (H - total_h) // 2 - 30

    def cx(text, f):
        return (W - int(draw.textlength(text, font=f))) // 2

    draw.text((cx(l1, f_hero), y), l1, fill=hex2rgb(WHITE), font=f_hero)
    y += h1 + 20
    draw.text((cx(l2, f_hero), y), l2, fill=hex2rgb(LILLY_RED), font=f_hero)
    y += h2 + 56
    draw.text((cx(sub, f_sub), y), sub, fill=hex2rgb(CAPTION), font=f_sub)

    img.save('slide_01.png')
    print('saved slide_01.png')


# ── Slide 2 — The Inflection Point ───────────────────────────────────────────
def slide_02():
    img, draw = make_slide(LIGHT_BG)
    draw_chrome(draw)

    f_hero = fnt(FONT_BLACK, 100)
    f_body = fnt(FONT_REGULAR, 34)

    # Hero left
    y = 165
    draw.text((95, y), 'The language has changed.', fill=hex2rgb(DARK), font=f_hero)
    y += 120
    draw.text((95, y), "The compute problem hasn't.", fill=hex2rgb(LILLY_RED), font=f_hero)

    # Body text — full width below hero
    body = (
        "Agentic workflows, autonomous discovery, AI-driven pipelines \u2014 beneath the vocabulary, "
        "the challenge is the same: a directed graph of heterogeneous model execution, where "
        "physics-based simulations, ML inference, and generative AI steps each carry distinct "
        "resource requirements. What has changed is the scale of that graph and the caliber of "
        "hardware each node demands. Tech@Lilly has a near-term window to define how this compute "
        "is owned before fragmentation becomes entrenched."
    )
    body_w = W - 95 - 95
    draw_wrapped(draw, body, f_body, 95, 430, body_w, MID_GRAY, 54)

    # Embed diagram_dag.png at bottom, scaled to fill width
    dag = Image.open('diagram_dag.png')
    scale = W / dag.width
    new_h = int(dag.height * scale)
    dag_r = dag.resize((W, new_h), Image.LANCZOS)
    paste_y = 720
    img.paste(dag_r, (0, paste_y))

    img.save('slide_02.png')
    print('saved slide_02.png')


# ── Slide 3 — The Current Pattern ────────────────────────────────────────────
def slide_03():
    img, draw = make_slide(LIGHT_BG)
    draw_chrome(draw)

    f_hero  = fnt(FONT_BLACK,   100)
    f_intro = fnt(FONT_REGULAR,  36)
    f_label = fnt(FONT_BOLD,     34)
    f_body  = fnt(FONT_REGULAR,  34)

    MAX_W = W - 95 - 95

    # Hero
    y = 165
    draw.text((95, y), 'Multiple teams are building', fill=hex2rgb(DARK), font=f_hero)
    y += 118
    draw.text((95, y), 'in isolation.', fill=hex2rgb(LILLY_RED), font=f_hero)
    y += 118 + 36

    # Intro sentence
    intro = (
        "AI4D (Discovery Oncology) and Data Foundry (LSMD) \u2014 each recruiting at AVP level, "
        "each building independently. A natural response to urgency. A compounding risk."
    )
    y = draw_wrapped(draw, intro, f_intro, 95, y, MAX_W, MID_GRAY, 56)
    y += 44

    # Separator line
    draw.rectangle([(95, y), (W - 95, y + 2)], fill=hex2rgb('#dddddd'))
    y += 20

    # 3 bullets
    bullets = [
        (
            'Scalability ceiling',
            "Built on cheap cloud GPU tiers. As workloads demand H100/H200/B300-class compute, "
            "cost and availability assumptions break down. Leadership doesn\u2019t see the cliff ahead.",
        ),
        (
            'Operational fragility',
            "Teams lack true HPC expertise. Inefficient patterns \u2014 e.g., using expensive GPU "
            "instances as data staging vehicles \u2014 are tolerable at low tiers; punishing at scale. "
            "Pivoting takes months, not a budget line.",
        ),
        (
            'Duplicated investment',
            "Separate tooling, separate staffing, no shared learning across functions.",
        ),
    ]

    INDENT = 48
    for label, body_text in bullets:
        y += 10
        # Red accent bar
        draw.rectangle([(95, y + 4), (99, y + 36)], fill=hex2rgb(LILLY_RED))
        draw.text((95 + INDENT, y), label, fill=hex2rgb(BULLETS), font=f_label)
        label_h = draw.textbbox((0, 0), label, font=f_label)[3]
        y += label_h + 10
        y = draw_wrapped(draw, body_text, f_body, 95 + INDENT, y, MAX_W - INDENT, '#666666', 50)
        y += 30

    img.save('slide_03.png')
    print('saved slide_03.png')


# ── Slide 4 — The Cost Reality ────────────────────────────────────────────────
def slide_04():
    img, draw = make_slide(LIGHT_BG)
    draw_chrome(draw)

    f_hero  = fnt(FONT_BLACK,   100)
    f_frame = fnt(FONT_REGULAR,  34)

    # Hero
    y = 165
    draw.text((95, y), 'On-premise compute costs', fill=hex2rgb(DARK), font=f_hero)
    y += 120
    draw.text((95, y), '2.7\u00d7 less at scale.', fill=hex2rgb(LILLY_RED), font=f_hero)
    y += 120 + 30

    # Framing sentence — full width below hero
    frame = (
        "These numbers cover compute only \u2014 a comparable high-performance parallel "
        "filesystem on cloud would widen the gap further."
    )
    draw_wrapped(draw, frame, f_frame, 95, y, W - 190, MID_GRAY, 54)

    # Embed cost chart — widened and centered below text
    if os.path.exists('diagram_cost.png'):
        chart = Image.open('diagram_cost.png')
        target_w = 2200
        scale = target_w / chart.width
        ch = int(chart.height * scale)
        chart_r = chart.resize((target_w, ch), Image.LANCZOS)
        paste_x = (W - target_w) // 2
        paste_y = 490
        img.paste(chart_r, (paste_x, paste_y))
    else:
        print('  WARNING: diagram_cost.png not found — skipping chart embed')

    img.save('slide_04.png')
    print('saved slide_04.png')


# ── Slide 5 — The Proposal ────────────────────────────────────────────────────
def slide_05():
    img, draw = make_slide(LIGHT_BG)
    draw_chrome(draw)

    f_hero    = fnt(FONT_BLACK,   100)
    f_closing = fnt(FONT_REGULAR,  38)

    # Hero
    y = 165
    draw.text((95, y), 'AIR and Digital Core', fill=hex2rgb(DARK), font=f_hero)
    y += 118
    draw.text((95, y), 'own this together.', fill=hex2rgb(LILLY_RED), font=f_hero)
    y += 118 + 44

    # Venn diagram — cap height at 880px so closing quote always fits
    VENN_Y = y
    if os.path.exists('diagram_venn.png'):
        venn = Image.open('diagram_venn.png')
        MAX_VENN_H = 880
        venn_w = int(venn.width * MAX_VENN_H / venn.height)
        venn = venn.resize((venn_w, MAX_VENN_H), Image.LANCZOS)
        x_offset = (W - venn_w) // 2
        img.paste(venn, (x_offset, VENN_Y))
        venn_bottom = VENN_Y + MAX_VENN_H
    else:
        venn_bottom = VENN_Y + 600

    img.save('slide_05.png')
    print('saved slide_05.png')


if __name__ == '__main__':
    slide_01()
    slide_02()
    slide_03()
    slide_04()
    slide_05()
    print('\nAll slides saved.')

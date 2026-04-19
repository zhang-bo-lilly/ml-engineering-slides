"""
gen_slides.py — Generate compute_layer_pptx_slides/ PNGs for the Compute Layer deck.

Run: python gen_slides.py   (diagram generators are called automatically)

Outputs (2880×1620 px each):
  compute_layer_pptx_slides/slide_01_anchor.png
  compute_layer_pptx_slides/slide_02_dag.png
  compute_layer_pptx_slides/slide_03a_estate_full.png
  compute_layer_pptx_slides/slide_03b_estate_runai.png
  compute_layer_pptx_slides/slide_04_current_arch.png
  compute_layer_pptx_slides/slide_05_runai_cost.png
  compute_layer_pptx_slides/slide_06_two_paths.png
"""

import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Output directory ────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), 'compute_layer_pptx_slides')
os.makedirs(OUT_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(__file__)

# ── Canvas ──────────────────────────────────────────────────────────────────
W, H = 2880, 1620

# ── Palette ─────────────────────────────────────────────────────────────────
DARK_BG      = '#1a2035'
LIGHT_BG     = '#f7f7f7'
WHITE_BG     = '#ffffff'
LILLY_RED    = '#e4002b'
WHITE        = '#ffffff'
BLACK_TEXT   = '#1a1a1a'
DARK_TEXT    = '#333333'
GREY_TEXT    = '#999999'
BODY_TEXT    = '#555555'
EMERALD      = '#10b981'
BLUE         = '#3b82f6'
INDIGO       = '#6366f1'
AMBER        = '#f59e0b'
GREY_CARD    = '#9ca3af'

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Font paths ───────────────────────────────────────────────────────────────
FONT_BLACK   = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
FONT_BOLD    = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

# ── Common chrome helpers ────────────────────────────────────────────────────

def draw_chrome(draw, dark_mode=True):
    """Draw breadcrumb top-left and red bottom bar."""
    # Bottom red bar
    draw.rectangle([(0, H - 18), (W, H)], fill=hex2rgb(LILLY_RED))

    # Breadcrumb
    crumb = "COMPUTE LAYER  ·  ADVANCED INTELLIGENCE  ·  ELI LILLY"
    f = font(FONT_REGULAR, 28)
    draw.text((95, 52), crumb, fill=hex2rgb(LILLY_RED), font=f)


def draw_hero(draw, line1, line2, x=95, y=130, size=118, dark_mode=True):
    """Two-line hero: line1 white/black, line2 Lilly Red ending with period."""
    f = font(FONT_BLACK, size)
    text_color = hex2rgb(WHITE) if dark_mode else hex2rgb(BLACK_TEXT)
    draw.text((x, y), line1, fill=text_color, font=f)
    _, _, _, h1 = draw.textbbox((0, 0), line1, font=f)
    draw.text((x, y + h1 + 8), line2, fill=hex2rgb(LILLY_RED), font=f)


def draw_rounded_rect(draw, x, y, w, h, radius, fill, outline=None, outline_width=0):
    """Draw a rounded rectangle."""
    r = radius
    fill_rgb = hex2rgb(fill)
    out_rgb  = hex2rgb(outline) if outline else None

    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=r,
                            fill=fill_rgb,
                            outline=out_rgb,
                            width=outline_width)


def wrap_text(draw, text, font_obj, max_width):
    """Wrap text to fit within max_width pixels, return list of lines."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] > max_width and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Anchor (dark, centred)
# ════════════════════════════════════════════════════════════════════════════

def slide_01():
    img  = Image.new('RGB', (W, H), hex2rgb(DARK_BG))
    draw = ImageDraw.Draw(img)

    # Hero — centred
    line1 = "Compute"
    line2 = "Layer."
    f_hero = font(FONT_BLACK, 160)
    b1 = draw.textbbox((0, 0), line1, font=f_hero)
    b2 = draw.textbbox((0, 0), line2, font=f_hero)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    gap = 16
    total_h = h1 + gap + h2
    top_y = (H - total_h) // 2 - 80

    draw.text(((W - w1) // 2, top_y), line1,
              fill=hex2rgb(WHITE), font=f_hero)
    draw.text(((W - w2) // 2, top_y + h1 + gap), line2,
              fill=hex2rgb(LILLY_RED), font=f_hero)

    # Subline
    subline = "End-to-end orchestration, not just GPU allocation."
    f_sub = font(FONT_REGULAR, 44)
    bs = draw.textbbox((0, 0), subline, font=f_sub)
    ws = bs[2] - bs[0]
    sub_y = top_y + h1 + gap + h2 + 60
    draw.text(((W - ws) // 2, sub_y), subline,
              fill=hex2rgb(WHITE), font=f_sub)

    # Mandate line
    mandate = "Our job: make heterogeneous scientific AI workflows run end to end, invisibly to the scientist."
    f_mandate = font(FONT_REGULAR, 34)
    f_mandate_lines = wrap_text(draw, mandate, f_mandate, W - 400)
    mandate_y = sub_y + 80
    for line in f_mandate_lines:
        bm = draw.textbbox((0, 0), line, font=f_mandate)
        wm = bm[2] - bm[0]
        draw.text(((W - wm) // 2, mandate_y), line,
                  fill=hex2rgb(GREY_TEXT), font=f_mandate)
        mandate_y += bm[3] - bm[1] + 10

    draw_chrome(draw, dark_mode=True)
    out = os.path.join(OUT_DIR, 'slide_01_anchor.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — The problem space (light, four-layer stack style)
# ════════════════════════════════════════════════════════════════════════════

def slide_02():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero top-left
    draw_hero(draw, "A pipeline is", "a DAG.", x=95, y=100, size=110, dark_mode=False)

    # Right-side context paragraph (includes the per-node insight)
    ctx = (
        "Scientific AI workflows are not monolithic model jobs.\n"
        "Whether exploring, building models, or running applications,\n"
        "each node in the pipeline may require different hardware —\n"
        "from CPU preprocessing to large-scale training."
    )
    f_ctx = font(FONT_REGULAR, 34)
    ctx_x = W // 2 + 60
    ctx_y = 140
    for line in ctx.split('\n'):
        draw.text((ctx_x, ctx_y), line, fill=hex2rgb(GREY_TEXT), font=f_ctx)
        ctx_y += 52

    # Section label — pushed down to clear the hero block
    f_label = font(FONT_BOLD, 26)
    draw.text((95, 390), "COMPUTE TIERS PER DAG NODE",
              fill=hex2rgb(LILLY_RED), font=f_label)

    # Five compute-tier cards (horizontal stack)
    cards = [
        ("#64748b", "PREPROCESSING",  "Pre/post-processing work\nNon-GPU-accelerated\napplications"),
        ("#7c3aed", "SIMULATION",     "Physics-based simulation\ne.g. molecular dynamics\nGPU-accelerated, distinct profile"),
        ("#3b82f6", "INFERENCE",      "Applying trained models\nHigh throughput"),
        (EMERALD,   "TRAINING",       "Building and fine-tuning\nmodels\nComputationally intensive"),
        ("#f59e0b", "DATA MOVEMENT",  "First-class concern\nVolume can be large\nEgress cost matters on hybrid infra"),
    ]

    n = len(cards)
    margin_x = 95
    margin_y = 480
    card_gap  = 28
    card_w    = (W - 2 * margin_x - (n - 1) * card_gap) // n
    card_h    = 480
    radius    = 18

    for i, (color, title, body) in enumerate(cards):
        cx = margin_x + i * (card_w + card_gap)
        cy = margin_y

        # Card background
        draw_rounded_rect(draw, cx, cy, card_w, card_h, radius, color)

        # Card title
        f_title = font(FONT_BLACK, 34)
        draw.text((cx + 28, cy + 28), title, fill=hex2rgb(WHITE), font=f_title)

        # Divider line
        div_y = cy + 82
        draw.rectangle([(cx + 28, div_y), (cx + card_w - 28, div_y + 2)],
                       fill=(255, 255, 255, 80))

        # Body text
        f_body = font(FONT_REGULAR, 30)
        by = div_y + 24
        for line in body.split('\n'):
            draw.text((cx + 28, by), line,
                      fill=(255, 255, 255, 220), font=f_body)
            by += 46

    # Footer note
    f_note = font(FONT_REGULAR, 30)
    note = "The compute layer must handle all tiers and hide the complexity from the scientist."
    draw.text((95, H - 80), note, fill=hex2rgb(EMERALD), font=f_note)

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_02_dag.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3a — Estate full (light bg + diagram inset)
# ════════════════════════════════════════════════════════════════════════════

def slide_03a():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Title — same vertical position as hero on other slides
    f_title = font(FONT_BLACK, 72)
    draw.text((95, 110), "What we govern vs. what exists.",
              fill=hex2rgb(BLACK_TEXT), font=f_title)

    # Diagram inset — takes lower ~78% of slide
    diag_src = Image.open(os.path.join(BASE_DIR, 'diagram-estate-full.png')).convert('RGB')
    panel_y = 240
    panel_h = H - panel_y - 30
    panel_w = W - 190
    panel_x = 95

    diag_aspect = diag_src.width / diag_src.height
    fit_w = panel_w
    fit_h = int(fit_w / diag_aspect)
    if fit_h > panel_h:
        fit_h = panel_h
        fit_w = int(fit_h * diag_aspect)

    diag_resized = diag_src.resize((fit_w, fit_h), Image.LANCZOS)
    paste_x = panel_x + (panel_w - fit_w) // 2
    paste_y = panel_y + (panel_h - fit_h) // 2
    img.paste(diag_resized, (paste_x, paste_y))

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_03a_estate_full.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3b — Estate Run:ai (light bg + diagram inset)
# ════════════════════════════════════════════════════════════════════════════

def slide_03b():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Title
    f_title = font(FONT_BLACK, 72)
    draw.text((95, 110), "Where Run:ai licensing makes economic sense.",
              fill=hex2rgb(BLACK_TEXT), font=f_title)

    # Diagram inset
    diag_src = Image.open(os.path.join(BASE_DIR, 'diagram-estate-runai.png')).convert('RGB')
    panel_y = 240
    panel_h = H - panel_y - 30
    panel_w = W - 190
    panel_x = 95

    diag_aspect = diag_src.width / diag_src.height
    fit_w = panel_w
    fit_h = int(fit_w / diag_aspect)
    if fit_h > panel_h:
        fit_h = panel_h
        fit_w = int(fit_h * diag_aspect)

    diag_resized = diag_src.resize((fit_w, fit_h), Image.LANCZOS)
    paste_x = panel_x + (panel_w - fit_w) // 2
    paste_y = panel_y + (panel_h - fit_h) // 2
    img.paste(diag_resized, (paste_x, paste_y))

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_03b_estate_runai.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Current architecture pain (light bg + diagram inset)
# ════════════════════════════════════════════════════════════════════════════

def slide_04():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero
    draw_hero(draw, "Two environments.", "No bridge.", x=95, y=110, size=100, dark_mode=False)

    # Section label
    f_label = font(FONT_BOLD, 26)
    draw.text((95, 375), "TODAY'S REALITY",
              fill=hex2rgb(LILLY_RED), font=f_label)

    # 3 bullets in the header band (right of hero, between hero and diagram)
    bullets = [
        "Two manual submissions for cross-cluster pipelines",
        "No step chaining across Run:ai and Slurm",
        "The abstraction leaks — users must know which env to target",
    ]
    f_bullet = font(FONT_REGULAR, 34)
    bx = W // 2 + 60
    by = 130
    for b in bullets:
        draw.text((bx, by), f"•  {b}", fill=hex2rgb(DARK_TEXT), font=f_bullet)
        by += 72

    # Diagram — takes the lower portion of the slide
    diag_src = Image.open(os.path.join(BASE_DIR, 'diagram-current-architecture.png')).convert('RGB')
    panel_y = 430
    panel_h = H - panel_y - 30
    panel_w = W - 190
    panel_x = 95

    diag_aspect = diag_src.width / diag_src.height
    fit_w = panel_w
    fit_h = int(fit_w / diag_aspect)
    if fit_h > panel_h:
        fit_h = panel_h
        fit_w = int(fit_h * diag_aspect)

    diag_resized = diag_src.resize((fit_w, fit_h), Image.LANCZOS)
    paste_x = panel_x + (panel_w - fit_w) // 2
    paste_y = panel_y + (panel_h - fit_h) // 2
    img.paste(diag_resized, (paste_x, paste_y))

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_04_current_arch.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Run:ai cost constraint (light bg, stat drama preserved)
# ════════════════════════════════════════════════════════════════════════════

def slide_05():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero (light mode — black + red)
    draw_hero(draw, "Run:ai is powerful.", "But not free.", x=95, y=110, size=100, dark_mode=False)

    # Left column: advantages
    f_label = font(FONT_BOLD, 26)
    draw.text((95, 385), "RUN:AI ADVANTAGES",
              fill=hex2rgb(LILLY_RED), font=f_label)

    advantages = [
        "Dynamic GPU fractioning",
        "Quota management",
        "Fine-grained workload scheduling",
    ]
    f_adv = font(FONT_REGULAR, 36)
    ay = 430
    for adv in advantages:
        draw.text((95, ay), f"→  {adv}", fill=hex2rgb(DARK_TEXT), font=f_adv)
        ay += 62

    # Vertical divider
    div_x = W // 2 - 80
    draw.rectangle([(div_x, 380), (div_x + 2, H - 60)],
                   fill=hex2rgb('#d0d5e0'))

    # Right column: large red stat — still dramatically large on white
    stat_x = div_x + 80
    f_stat = font(FONT_BLACK, 200)
    draw.text((stat_x, 250), "$3K", fill=hex2rgb(LILLY_RED), font=f_stat)

    f_stat_label = font(FONT_REGULAR, 38)
    draw.text((stat_x, 500), "per GPU  ·  per year",
              fill=hex2rgb(GREY_TEXT), font=f_stat_label)

    # Callout box — light grey with Lilly Red left border
    box_x, box_y = stat_x, 610
    box_w, box_h = W - stat_x - 90, 340
    draw_rounded_rect(draw, box_x, box_y, box_w, box_h, 16, '#ebebeb')
    draw.rectangle([(box_x, box_y), (box_x + 8, box_y + box_h)],
                   fill=hex2rgb(LILLY_RED))

    callout_lines = [
        "Unification of the full estate under",
        "one scheduler is not on the roadmap.",
        " ",
        "We design around that.",
    ]
    f_callout = font(FONT_BOLD, 36)
    cy = box_y + 40
    for line in callout_lines:
        draw.text((box_x + 40, cy), line, fill=hex2rgb(BLACK_TEXT), font=f_callout)
        cy += 58

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_05_runai_cost.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Two paths forward (light, two-priorities layout)
# ════════════════════════════════════════════════════════════════════════════

def slide_06():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero
    draw_hero(draw, "Fix the floor.", "Raise the ceiling.", x=95, y=110, size=100, dark_mode=False)

    # Two large side-by-side cards — light tinted fills, coloured borders
    EMERALD_TINT  = '#e6f7f1'
    EMERALD_BORDER= '#10b981'
    EMERALD_LABEL = '#0a7c57'
    INDIGO_TINT   = '#eeeffd'
    INDIGO_BORDER = '#6366f1'
    INDIGO_LABEL  = '#4338ca'

    margin_x = 95
    card_y   = 400
    gap      = 40
    card_w   = (W - 2 * margin_x - gap) // 2
    card_h   = H - card_y - 90
    radius   = 20

    # Left card — Near-term (light emerald)
    lx = margin_x
    draw_rounded_rect(draw, lx, card_y, card_w, card_h, radius,
                      EMERALD_TINT, outline=EMERALD_BORDER, outline_width=3)

    f_card_label = font(FONT_BOLD, 26)
    draw.text((lx + 40, card_y + 36), "NEAR-TERM  ·  EXECUTION",
              fill=hex2rgb(EMERALD_LABEL), font=f_card_label)

    f_card_title = font(FONT_BLACK, 52)
    draw.text((lx + 40, card_y + 82), "Consolidate into LillyPod",
              fill=hex2rgb(BLACK_TEXT), font=f_card_title)

    left_bullets = [
        "Move H100 / H200 / L40s under Run:ai",
        "Add fat CPU-only nodes to LillyPod",
        "Unified Weka storage across all tiers",
        "Users get the right tier — without knowing where it lives",
        "Aligned with Greg & Jon, 2025 RFP",
    ]
    f_lb = font(FONT_REGULAR, 32)
    ly = card_y + 160
    for b in left_bullets:
        draw.text((lx + 40, ly), f"•  {b}", fill=hex2rgb(DARK_TEXT), font=f_lb)
        ly += 54

    # Inset diagram in left card
    diag_src = Image.open(os.path.join(BASE_DIR, 'diagram-target-architecture.png')).convert('RGB')
    inset_y = ly + 24
    inset_h = card_y + card_h - inset_y - 24
    inset_w = card_w - 80
    if inset_h > 40:
        aspect  = diag_src.width / diag_src.height
        fit_w   = inset_w
        fit_h   = int(fit_w / aspect)
        if fit_h > inset_h:
            fit_h = inset_h
            fit_w = int(fit_h * aspect)
        d_resized = diag_src.resize((fit_w, fit_h), Image.LANCZOS)
        img.paste(d_resized, (lx + 40, inset_y))

    # Right card — Long-term (light indigo)
    rx = margin_x + card_w + gap
    draw_rounded_rect(draw, rx, card_y, card_w, card_h, radius,
                      INDIGO_TINT, outline=INDIGO_BORDER, outline_width=3)

    draw.text((rx + 40, card_y + 36), "LONG-TERM  ·  RESEARCH FRONTIER",
              fill=hex2rgb(INDIGO_LABEL), font=f_card_label)

    draw.text((rx + 40, card_y + 82), "Meta-orchestrator",
              fill=hex2rgb(BLACK_TEXT), font=font(FONT_BLACK, 52))

    right_bullets = [
        "Routing layer above Run:ai, Slurm, and cloud",
        "Chains pipeline steps across schedulers transparently",
        "Makes the full estate — including cloud — available to scientists",
        "Novel work: high risk, high reward",
        "Publication potential: MLSys, GTC, and beyond",
    ]
    ry = card_y + 160
    for b in right_bullets:
        draw.text((rx + 40, ry), f"•  {b}", fill=hex2rgb(DARK_TEXT), font=f_lb)
        ry += 54

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_06_two_paths.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Quota governance structure + tier system (light bg)
# ════════════════════════════════════════════════════════════════════════════

def slide_07():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero
    draw_hero(draw, "Quota by", "design.", x=95, y=110, size=110, dark_mode=False)

    # ── Shared label font ──────────────────────────────────────────────────
    f_label   = font(FONT_BOLD, 26)
    f_caption = font(FONT_REGULAR, 28)
    f_body    = font(FONT_REGULAR, 30)

    # ── LEFT COLUMN (x: 95–1380) ──────────────────────────────────────────
    lx    = 95
    l_w   = 1260   # usable width in left column
    y     = 405    # start below hero

    # ── Section 1: Governance Structure ───────────────────────────────────
    draw.text((lx, y), "GOVERNANCE STRUCTURE",
              fill=hex2rgb(LILLY_RED), font=f_label)
    y += 48

    # Hierarchy diagram
    hier_w = l_w - 60
    hier_h = 265

    # Dept box (emerald)
    dept_w, dept_h = 600, 66
    dept_x = lx + (hier_w - dept_w) // 2
    dept_y = y + 16
    draw_rounded_rect(draw, dept_x, dept_y, dept_w, dept_h, 12, EMERALD)
    dept_txt = 'Run:ai Department: "ai"'
    f_dept = font(FONT_BOLD, 28)
    tb = draw.textbbox((0, 0), dept_txt, font=f_dept)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    draw.text((dept_x + (dept_w - tw) // 2, dept_y + (dept_h - th) // 2 - tb[1]),
              dept_txt, fill=hex2rgb(WHITE), font=f_dept)

    # Vertical stem
    stem_x  = lx + hier_w // 2
    stem_y1 = dept_y + dept_h
    stem_y2 = y + 165
    draw.line([(stem_x, stem_y1), (stem_x, stem_y2)], fill=hex2rgb('#888888'), width=3)

    # Project boxes
    proj_w, proj_h = 310, 64
    gap_proj = 60
    total_proj_w = 2 * proj_w + gap_proj
    proj1_cx = lx + (hier_w - total_proj_w) // 2 + proj_w // 2
    proj2_cx = proj1_cx + proj_w + gap_proj

    # Horizontal fork line
    draw.line([(proj1_cx, stem_y2), (proj2_cx, stem_y2)],
              fill=hex2rgb('#888888'), width=3)

    # Drops to project boxes
    proj_y = y + 175
    for px in (proj1_cx, proj2_cx):
        draw.line([(px, stem_y2), (px, proj_y)],
                  fill=hex2rgb('#888888'), width=3)

    # Draw project boxes and text
    f_proj_title = font(FONT_BOLD, 22)
    f_proj_sub   = font(FONT_REGULAR, 20)
    for px, squad_name in [(proj1_cx, 'Squad A'), (proj2_cx, 'Squad B')]:
        draw_rounded_rect(draw, px - proj_w // 2, proj_y, proj_w, proj_h, 10, BLUE)
        t1 = 'Run:ai Project'
        t2 = f'= {squad_name}'
        tb1 = draw.textbbox((0, 0), t1, font=f_proj_title)
        tb2 = draw.textbbox((0, 0), t2, font=f_proj_sub)
        h1  = tb1[3] - tb1[1]
        h2  = tb2[3] - tb2[1]
        block_h = h1 + 6 + h2
        y_top   = proj_y + (proj_h - block_h) // 2
        draw.text((px - (tb1[2] - tb1[0]) // 2, y_top - tb1[1]),
                  t1, fill=hex2rgb(WHITE), font=f_proj_title)
        draw.text((px - (tb2[2] - tb2[0]) // 2, y_top + h1 + 6 - tb2[1]),
                  t2, fill=hex2rgb(WHITE), font=f_proj_sub)

    # "…" for more squads
    f_ellipsis = font(FONT_BOLD, 40)
    draw.text((proj2_cx + proj_w // 2 + 22, proj_y + proj_h // 2 - 20),
              '…', fill=hex2rgb('#999999'), font=f_ellipsis)

    y += hier_h + 8

    # Caption
    draw.text((lx, y), "All AIOS-governed GPUs live in one department.",
              fill=hex2rgb(GREY_TEXT), font=f_caption)
    y += 40
    draw.text((lx, y), "Each Run:ai project maps 1-to-1 to a squad.",
              fill=hex2rgb(GREY_TEXT), font=f_caption)
    y += 68

    # ── Section 2: Effective Quota ─────────────────────────────────────────
    draw.text((lx, y), "EFFECTIVE QUOTA",
              fill=hex2rgb(LILLY_RED), font=f_label)
    y += 48

    eq_box_h = 155
    draw_rounded_rect(draw, lx, y, l_w, eq_box_h, 12,
                      WHITE_BG, outline='#d0d5e0', outline_width=2)

    eq_formula = "EQ  =  allocated GPU-hrs  /  evaluation period hours"
    f_eq = font(FONT_BOLD, 30)
    draw.text((lx + 30, y + 26), eq_formula,
              fill=hex2rgb(BLACK_TEXT), font=f_eq)

    eq_sub = ("Always computable. Expressed in GPUs — "
              "directly comparable against a squad's quota Q.")
    f_eq_sub = font(FONT_REGULAR, 26)
    sub_lines = wrap_text(draw, eq_sub, f_eq_sub, l_w - 60)
    sy = y + 82
    for line in sub_lines:
        draw.text((lx + 30, sy), line,
                  fill=hex2rgb(GREY_TEXT), font=f_eq_sub)
        sy += 34

    y += eq_box_h + 28

    # ── Section 3: Design Principle ────────────────────────────────────────
    draw.text((lx, y), "DESIGN PRINCIPLE",
              fill=hex2rgb(LILLY_RED), font=f_label)
    y += 48

    dp_box_h = 190
    draw_rounded_rect(draw, lx, y, l_w, dp_box_h, 12,
                      WHITE_BG, outline='#d0d5e0', outline_width=2)
    draw.rectangle([(lx, y), (lx + 8, y + dp_box_h)],
                   fill=hex2rgb(LILLY_RED))

    principle = (
        "Fair and proportional. Squads that allocate and "
        "utilize more earn more quota — maximizing cluster "
        "utilization above 80%."
    )
    f_principle = font(FONT_BOLD, 30)
    p_lines = wrap_text(draw, principle, f_principle, l_w - 80)
    py = y + 28
    for line in p_lines:
        draw.text((lx + 40, py), line,
                  fill=hex2rgb(BLACK_TEXT), font=f_principle)
        py += 48

    # ── RIGHT COLUMN: Tier system cards (x: 1455–2785) ────────────────────
    rx    = 1455
    r_w   = W - rx - 95   # ≈ 1330 px

    draw.text((rx, 110), "TIER SYSTEM",
              fill=hex2rgb(LILLY_RED), font=f_label)

    tier_cards = [
        (EMERALD,   'TIER 1', 'EQ > Q  ·  avg util > 80%',
         'Exceeding quota — high utilization'),
        (BLUE,      'TIER 2', 'EQ > Q  ·  avg util ≤ 80%',
         'Exceeding quota — utilization gap'),
        (AMBER,     'TIER 3', '0.8Q ≤ EQ ≤ Q',
         'On-quota range  ·  new squads default here'),
        (GREY_CARD, 'TIER 4', 'EQ < 0.8Q',
         'Under-utilizing quota'),
    ]

    card_gap     = 20
    card_y_start = 165
    avail_h      = H - 18 - card_y_start - card_gap * (len(tier_cards) - 1) - 20
    card_h       = avail_h // len(tier_cards)

    cy = card_y_start
    f_tier_num  = font(FONT_BLACK, 42)
    f_cond      = font(FONT_BOLD, 34)
    f_meaning   = font(FONT_REGULAR, 30)

    for color, tier_label, condition, meaning in tier_cards:
        draw_rounded_rect(draw, rx, cy, r_w, card_h, 18, color)

        # Tier label
        draw.text((rx + 40, cy + 30), tier_label,
                  fill=hex2rgb(WHITE), font=f_tier_num)

        # Divider
        div_y = cy + 100
        draw.rectangle([(rx + 40, div_y), (rx + r_w - 40, div_y + 2)],
                       fill=(255, 255, 255, 60))

        # Condition
        draw.text((rx + 40, div_y + 22), condition,
                  fill=hex2rgb(WHITE), font=f_cond)

        # Meaning
        draw.text((rx + 40, div_y + 88), meaning,
                  fill=(220, 220, 220), font=f_meaning)

        cy += card_h + card_gap

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_07_quota_structure.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Biweekly quota adjustment procedure (light bg)
# ════════════════════════════════════════════════════════════════════════════

def slide_08():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # Hero
    draw_hero(draw, "Earned.", "Biweekly.", x=95, y=110, size=110, dark_mode=False)

    # ── LEFT PANEL: decision flowchart (x: 95–1700) ───────────────────────
    diag_src = Image.open(
        os.path.join(BASE_DIR, 'diagram-quota-flow.png')
    ).convert('RGB')

    panel_x = 95
    panel_y = 400
    panel_w = 1600
    panel_h = H - panel_y - 30

    diag_aspect = diag_src.width / diag_src.height
    fit_w = panel_w
    fit_h = int(fit_w / diag_aspect)
    if fit_h > panel_h:
        fit_h = panel_h
        fit_w = int(fit_h * diag_aspect)

    diag_resized = diag_src.resize((fit_w, fit_h), Image.LANCZOS)
    paste_x = panel_x + (panel_w - fit_w) // 2
    paste_y = panel_y + (panel_h - fit_h) // 2
    img.paste(diag_resized, (paste_x, paste_y))

    # ── RIGHT COLUMN (x: 1760–2785) ───────────────────────────────────────
    rx   = 1760
    r_w  = W - rx - 95   # ≈ 1025 px
    f_label = font(FONT_BOLD, 26)

    draw.text((rx, 110), "QUOTA CALCULATION",
              fill=hex2rgb(LILLY_RED), font=f_label)

    # Legend / symbol definitions
    f_legend = font(FONT_REGULAR, 26)
    legend_lines = [
        "ND  =  new demand",
        "DF  =  discount factor",
        "ND, DF, max weight cap — tunable parameters",
    ]
    ly = 160
    for line in legend_lines:
        draw.text((rx, ly), line, fill=hex2rgb(GREY_TEXT), font=f_legend)
        ly += 36

    # ── Callout Box 1 — Final quota formula ───────────────────────────────
    box_y  = ly + 28
    box1_h = 240
    draw_rounded_rect(draw, rx, box_y, r_w, box1_h, 14,
                      WHITE_BG, outline='#d0d5e0', outline_width=2)
    draw.rectangle([(rx, box_y), (rx + 8, box_y + box1_h)],
                   fill=hex2rgb(LILLY_RED))

    f_box_label = font(FONT_BOLD, 24)
    draw.text((rx + 36, box_y + 24), "FINAL QUOTA FORMULA",
              fill=hex2rgb(LILLY_RED), font=f_box_label)

    f_formula      = font(FONT_BOLD, 32)
    f_formula_lg   = font(FONT_BLACK, 38)   # larger Σ / numerator
    f_formula_rhs  = font(FONT_BOLD, 32)

    # "New quota  =" label on its own line
    fy = box_y + 68
    draw.text((rx + 36, fy), "New quota  =",
              fill=hex2rgb(BLACK_TEXT), font=f_formula)
    fy += 50

    # ── fraction block ──────────────────────────────────────────────────
    frac_x = rx + 36          # left edge of fraction
    num_text  = "squad weight"
    den_text  = "Σ all weights"   # Σ inline, same line as "all weights"
    rhs_text  = "×  available pool"

    # measure widths so the bar spans the wider of num/den
    num_w  = draw.textlength(num_text,  font=f_formula_lg)
    den_w  = draw.textlength(den_text,  font=f_formula_lg)
    bar_w  = int(max(num_w, den_w)) + 16   # a little padding on each side

    line_h_lg = 44   # line height for f_formula_lg
    gap       = 8    # gap between text and fraction bar
    bar_h     = 3

    # numerator — centred over bar
    num_offset = (bar_w - int(num_w)) // 2
    draw.text((frac_x + num_offset, fy),
              num_text, fill=hex2rgb(BLACK_TEXT), font=f_formula_lg)

    # fraction bar
    bar_y = fy + line_h_lg + gap
    draw.rectangle([(frac_x, bar_y), (frac_x + bar_w, bar_y + bar_h)],
                   fill=hex2rgb(BLACK_TEXT))

    # denominator — centred under bar
    den_offset = (bar_w - int(den_w)) // 2
    draw.text((frac_x + den_offset, bar_y + bar_h + gap),
              den_text, fill=hex2rgb(BLACK_TEXT), font=f_formula_lg)

    # "× available pool" — vertically centred on the fraction bar
    rhs_x   = frac_x + bar_w + 24
    rhs_mid = bar_y + bar_h // 2   # mid of the fraction bar
    # mid of rhs text (one line of f_formula_rhs ≈ 40px tall)
    rhs_y   = rhs_mid - 20
    draw.text((rhs_x, rhs_y), rhs_text,
              fill=hex2rgb(BLACK_TEXT), font=f_formula_rhs)

    # advance fy past the whole fraction block
    fy = bar_y + bar_h + gap + line_h_lg + 12

    # ── Callout Box 2 — Common pool ───────────────────────────────────────
    box2_y = box_y + box1_h + 28
    box2_h = 430
    draw_rounded_rect(draw, rx, box2_y, r_w, box2_h, 14,
                      WHITE_BG, outline='#d0d5e0', outline_width=2)
    draw.rectangle([(rx, box2_y), (rx + 8, box2_y + box2_h)],
                   fill=hex2rgb(LILLY_RED))

    draw.text((rx + 36, box2_y + 24), "COMMON POOL",
              fill=hex2rgb(LILLY_RED), font=f_box_label)

    f_pool_formula = font(FONT_BOLD, 30)
    draw.text((rx + 36, box2_y + 68),
              "Available pool  =  Total GPUs  −  Common Pool",
              fill=hex2rgb(BLACK_TEXT), font=f_pool_formula)

    f_pool_body = font(FONT_REGULAR, 28)
    pool_label_y = box2_y + 122
    draw.text((rx + 36, pool_label_y), "Reserved for:",
              fill=hex2rgb(GREY_TEXT), font=f_pool_body)

    pool_bullets = [
        "Over-quota bursting across squads",
        "Onboarding new squads mid-cycle",
        "Time-bound project deliveries",
    ]
    by = pool_label_y + 48
    for bullet in pool_bullets:
        draw.text((rx + 36, by), f"·  {bullet}",
                  fill=hex2rgb(DARK_TEXT), font=f_pool_body)
        by += 54

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_08_quota_procedure.png')
    img.save(out)
    print(f"  Saved {out}")


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — BioNova: components (left) + technical flow (right) + tagline
# ════════════════════════════════════════════════════════════════════════════

def slide_09():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    # ── App icon + hero row ───────────────────────────────────────────────
    # Icon: 180×180 at x=95, y=95
    icon_path = os.path.join(BASE_DIR, 'BioNova_Appicon.png')
    icon_src  = Image.open(icon_path).convert('RGBA')
    icon_size = 180
    icon_src  = icon_src.resize((icon_size, icon_size), Image.LANCZOS)
    img.paste(icon_src, (95, 95), icon_src)

    # Hero starts right of icon with a small gap; font size 100 to keep line
    # height compact enough that two lines clear before the cards begin
    draw_hero(draw, 'Science, not', 'infrastructure.', x=300, y=100, size=100, dark_mode=False)

    # Context line (right side, grey) — anchored well below breadcrumb
    f_ctx = font(FONT_REGULAR, 32)
    draw.text((1480, 130),
              'A platform for scientists, built by the data science team —',
              fill=hex2rgb(GREY_TEXT), font=f_ctx)
    draw.text((1480, 172),
              'so scientists focus on discovery, not infrastructure.',
              fill=hex2rgb(GREY_TEXT), font=f_ctx)

    # ── Content zone: y=400 to y=1395, then tagline y=1415 to y=1580 ─────
    content_start = 400
    content_end   = 1395   # tagline starts below this

    # ── Left column: 3 component cards (x=95, w=1275) ────────────────────
    card_x, card_w = 95, 1275
    card_gap = 20
    # Heights sum to content_end - content_start = 995:
    # 385 + 290 + 280 + 2*20 = 995
    card_defs = [
        {
            'h':       385,
            'color':   INDIGO,
            'label':   'DESKTOP APPLICATION  ·  APPLICATION LAYER',
            'title':   'Desktop App',
            'bullets': [
                'Build and run pipelines visually',
                'Share and reuse pipelines with colleagues',
                'No-code fine-tuning campaigns',
                'Step result caching',
                'Automated data management (trash can)',
                'LillyFlow integration',
            ],
        },
        {
            'h':       290,
            'color':   EMERALD,
            'label':   'BIONOVA CLI  ·  COMPUTE LAYER',
            'title':   'BioNova CLI',
            'bullets': [
                'Translates pipeline YAML → cluster job scripts',
                'Currently deployed on MagTrain (Slurm backend)',
                'New Argo backend for LillyPod (Run:ai) in progress',
                'Handles submit, scheduling, GPU dispatch',
            ],
        },
        {
            'h':       280,
            'color':   BLUE,
            'label':   'MODEL REGISTRY  ·  MODEL LAYER INTERFACE',
            'title':   'Model Registry',
            'bullets': [
                'Curated collection of optimized AI models',
                'GPU-optimized, containerized',
                'CLI enumerates available models at runtime',
                'Model addition today requires CLI code expansion',
            ],
        },
    ]

    f_label  = font(FONT_BOLD, 22)
    f_title  = font(FONT_BLACK, 38)
    f_bullet = font(FONT_REGULAR, 25)
    f_sec    = font(FONT_BOLD, 26)

    draw.text((card_x, content_start - 32), 'COMPONENTS',
              fill=hex2rgb(LILLY_RED), font=f_sec)

    card_y = content_start
    for card in card_defs:
        ch = card['h']
        draw_rounded_rect(draw, card_x, card_y, card_w, ch, 16, card['color'])
        draw.text((card_x + 26, card_y + 16), card['label'],
                  fill=hex2rgb(WHITE), font=f_label)
        draw.text((card_x + 26, card_y + 46), card['title'],
                  fill=hex2rgb(WHITE), font=f_title)
        ty = card_y + 46 + 44
        draw.rectangle([(card_x + 26, ty), (card_x + card_w - 26, ty + 1)],
                       fill=(255, 255, 255))
        by = ty + 12
        for bullet in card['bullets']:
            draw.text((card_x + 26, by), f'·  {bullet}',
                      fill=hex2rgb(WHITE), font=f_bullet)
            by += 38
        card_y += ch + card_gap

    # ── Vertical divider ──────────────────────────────────────────────────
    draw.rectangle([(1420, content_start - 10), (1422, content_end + 8)],
                   fill=hex2rgb('#d0d5e0'))

    # ── Right column: technical flow (x=1440, w=1345) ────────────────────
    fx, fw = 1440, 1345

    draw.text((fx, content_start - 32), 'THE TECHNICAL FLOW',
              fill=hex2rgb(LILLY_RED), font=f_sec)

    flow_boxes = [
        {
            'lines': [
                'Desktop app launches → SSH into cluster',
                'BioNova CLI pull → outputs model metadata as JSON',
                'Desktop copies JSON back, stores in local SQLite DB',
            ],
            'badge': 'Desktop App + CLI', 'badge_color': INDIGO,
        },
        {
            'lines': [
                'Scientist configures model or DAG of models',
                'via the Desktop GUI (per-model parameter walkthrough)',
            ],
            'badge': 'Desktop App', 'badge_color': INDIGO,
        },
        {
            'lines': [
                'Scientist hits Submit',
                'Desktop transfers collected data to cluster',
                'Calls BioNova CLI submit command',
            ],
            'badge': 'Desktop App + CLI', 'badge_color': INDIGO,
        },
        {
            'lines': [
                'BioNova CLI translates pipeline YAML → job scripts',
                'Slurm (MagTrain, live) / Argo (LillyPod, in progress)',
                'Submits to scheduler → GPU dispatch',
            ],
            'badge': 'CLI + Slurm / Argo', 'badge_color': EMERALD, 'solid': True,
        },
    ]

    # 4 boxes in 995px: (995 - 3*48) / 4 = (995 - 144) / 4 = 212
    box_h   = 212
    box_gap = 48
    arrow_h = 24
    f_flow  = font(FONT_REGULAR, 27)
    f_badge = font(FONT_BOLD, 21)

    fy = content_start
    for i, box in enumerate(flow_boxes):
        solid = box.get('solid', False)
        if solid:
            draw_rounded_rect(draw, fx, fy, fw, box_h, 14, EMERALD)
            text_col = WHITE
        else:
            draw_rounded_rect(draw, fx, fy, fw, box_h, 14, WHITE,
                              outline='#d0d5e0', outline_width=2)
            text_col = DARK_TEXT

        ty = fy + 18
        for line in box['lines']:
            draw.text((fx + 26, ty), line, fill=hex2rgb(text_col), font=f_flow)
            ty += 44

        # actor badge (top-right)
        badge_fill = WHITE if solid else box['badge_color']
        badge_tc   = EMERALD if solid else WHITE
        bb = draw.textbbox((0, 0), box['badge'], font=f_badge)
        bw, bh = bb[2] - bb[0] + 20, 32
        bx = fx + fw - bw - 14
        draw_rounded_rect(draw, bx, fy + 12, bw, bh, 16, badge_fill)
        draw.text((bx + 10, fy + 12 + (bh - (bb[3] - bb[1])) // 2),
                  box['badge'], fill=hex2rgb(badge_tc), font=f_badge)

        # downward arrow connector
        if i < len(flow_boxes) - 1:
            ax = fx + fw // 2
            ay = fy + box_h + 8
            draw.rectangle([(ax - 3, ay), (ax + 3, ay + arrow_h)],
                           fill=hex2rgb(GREY_TEXT))
            draw.polygon([(ax - 12, ay + arrow_h),
                          (ax + 12, ay + arrow_h),
                          (ax,      ay + arrow_h + 16)],
                         fill=hex2rgb(GREY_TEXT))
        fy += box_h + box_gap

    # ── Full-width dark tagline (bottom callout) ───────────────────────────
    tag_y, tag_h = 1415, 148
    draw_rounded_rect(draw, 95, tag_y, 2690, tag_h, 14, DARK_BG)
    f_tag  = font(FONT_BOLD, 30)
    f_tags = font(FONT_REGULAR, 24)
    draw.text((136, tag_y + 20),
              '"If the compute layer is the engine,',
              fill=hex2rgb(WHITE), font=f_tag)
    draw.text((136, tag_y + 60),
              'BioNova is the dashboard + ignition key."',
              fill=hex2rgb(LILLY_RED), font=f_tag)
    draw.text((136, tag_y + 104),
              '— production today on MagTrain  ·  LillyPod backend in progress',
              fill=hex2rgb(GREY_TEXT), font=f_tags)

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_09_bionova_components.png')
    img.save(out)
    print(f'  Saved {out}')


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — BioNova layer coverage (full-width bars)
# ════════════════════════════════════════════════════════════════════════════

def slide_10():
    img  = Image.new('RGB', (W, H), hex2rgb(LIGHT_BG))
    draw = ImageDraw.Draw(img)

    draw_hero(draw, 'Four layers.', 'Two active.', x=95, y=110, size=110, dark_mode=False)

    # Context (right of hero)
    f_ctx = font(FONT_REGULAR, 32)
    draw.text((1250, 140),
              'BioNova is designed to span the full AIOS stack.',
              fill=hex2rgb(GREY_TEXT), font=f_ctx)
    draw.text((1250, 182),
              'APPLICATION and COMPUTE are live today.',
              fill=hex2rgb(GREY_TEXT), font=f_ctx)
    draw.text((1250, 224),
              'MODEL and DATA integration is on the roadmap.',
              fill=hex2rgb(GREY_TEXT), font=f_ctx)

    # Full-width layer bars — APPLICATION (top) → MODEL → COMPUTE → DATA
    # (1602 - 390 - 3*14) / 4 = (1212 - 42) / 4 = 292  →  bar_h=292
    bar_x, bar_w = 95, 2690
    bar_h        = 292
    bar_gap      = 14
    bar_y_start  = 390

    layer_bars = [
        {
            'color':   INDIGO,
            'name':    'APPLICATION',
            'pill':    'ACTIVE',
            'pill_bg': INDIGO,
            'sub1_col': (220, 220, 220),
            'sub2_col': (210, 210, 210),
            'sub1':    'Desktop App — scientist-facing GUI for running pipelines, fine-tuning, and result management.',
            'sub2':    'Components: pipeline builder · pipeline sharing · no-code fine-tuning · step caching · LillyFlow integration',
        },
        {
            'color':   BLUE,
            'name':    'MODEL',
            'pill':    'ROADMAP',
            'pill_bg': None,
            'sub1_col': (220, 220, 220),
            'sub2_col': (210, 210, 210),
            'sub1':    'Bidirectional W&B integration — pull published model metadata; push fine-tuned checkpoints back.',
            'sub2':    'Today: each new model requires CLI code expansion.  Goal: metadata-driven discovery from W&B.',
        },
        {
            'color':   EMERALD,
            'name':    'COMPUTE',
            'pill':    'ACTIVE',
            'pill_bg': EMERALD,
            'sub1_col': (255, 255, 255),
            'sub2_col': (230, 255, 245),   # bright tinted white — legible on green
            'sub1':    'BioNova CLI — translates pipeline YAML into cluster job scripts and manages GPU dispatch.',
            'sub2':    'Live: MagTrain (Slurm).  In progress: LillyPod (Argo + Run:ai).',
        },
        {
            'color':   AMBER,
            'name':    'DATA',
            'pill':    'ROADMAP',
            'pill_bg': None,
            'sub1_col': (60, 30, 0),       # dark brown — legible on bright amber
            'sub2_col': (80, 40, 0),
            'sub1':    'Bidirectional data integration — consume upstream data into pipelines.',
            'sub2':    'Write workflow outputs back to the data layer.',
        },
    ]

    f_name = font(FONT_BLACK, 52)
    f_sub1 = font(FONT_REGULAR, 30)
    f_sub2 = font(FONT_REGULAR, 26)
    f_pill = font(FONT_BOLD, 24)
    pill_w, pill_h = 240, 50

    for i, bar in enumerate(layer_bars):
        by_ = bar_y_start + i * (bar_h + bar_gap)
        draw_rounded_rect(draw, bar_x, by_, bar_w, bar_h, 14, bar['color'])

        # Layer name
        draw.text((bar_x + 36, by_ + 28), bar['name'],
                  fill=hex2rgb(WHITE), font=f_name)

        # Sub-text lines (avoid pill area on far right)
        max_sub_w = bar_w - pill_w - 100
        sub1_lines = wrap_text(draw, bar['sub1'], f_sub1, max_sub_w)
        sub2_lines = wrap_text(draw, bar['sub2'], f_sub2, max_sub_w)

        sy = by_ + 110
        for line in sub1_lines:
            draw.text((bar_x + 36, sy), line,
                      fill=bar['sub1_col'], font=f_sub1)
            sy += 38
        sy += 4
        for line in sub2_lines:
            draw.text((bar_x + 36, sy), line,
                      fill=bar['sub2_col'], font=f_sub2)
            sy += 34

        # Status pill (right-aligned, vertically centred)
        px = bar_x + bar_w - pill_w - 36
        py = by_ + (bar_h - pill_h) // 2
        if bar['pill_bg']:
            draw_rounded_rect(draw, px, py, pill_w, pill_h, 25, WHITE)
            pill_tc = bar['pill_bg']
        else:
            draw_rounded_rect(draw, px, py, pill_w, pill_h, 25, '#ebebeb')
            pill_tc = GREY_TEXT
        bb = draw.textbbox((0, 0), bar['pill'], font=f_pill)
        draw.text((px + (pill_w - (bb[2] - bb[0])) // 2,
                   py + (pill_h - (bb[3] - bb[1])) // 2),
                  bar['pill'], fill=hex2rgb(pill_tc), font=f_pill)

    draw_chrome(draw, dark_mode=False)
    out = os.path.join(OUT_DIR, 'slide_10_bionova_flow.png')
    img.save(out)
    print(f'  Saved {out}')


# ── Run all ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Generating diagrams...")
    for script in [
        'gen_diagram_estate_a.py',
        'gen_diagram_estate_b.py',
        'gen_diagram_current.py',
        'gen_diagram_target.py',
        'gen_diagram_quota_flow.py',
    ]:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, script)], check=True)

    print("Generating slides...")
    slide_01()
    slide_02()
    slide_03a()
    slide_03b()
    slide_04()
    slide_05()
    slide_06()
    slide_07()
    slide_08()
    slide_09()
    slide_10()
    print("Done. PNGs written to compute_layer_pptx_slides/")

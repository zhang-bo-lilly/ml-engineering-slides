import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 2880, 1620
MARGIN = 194
BOTTOM_BAR = 18

_fcache = {}

def _font(name, size):
    key = (name, size)
    if key in _fcache:
        return _fcache[key]
    paths = {
        'Arial-Black': ['/System/Library/Fonts/Supplemental/Arial Black.ttf', '/Library/Fonts/Arial Black.ttf'],
        'Arial-Bold':  ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',  '/Library/Fonts/Arial Bold.ttf'],
        'Arial':       ['/System/Library/Fonts/Supplemental/Arial.ttf',        '/Library/Fonts/Arial.ttf'],
    }
    for p in paths.get(name, []):
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            _fcache[key] = f
            return f
    return ImageFont.load_default(size)


def _grid(draw):
    # Faint grid lines every 180px
    grid_col = (200, 210, 230, 60)
    for x in range(0, W, 180):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 180):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)
    # Margin guides
    margin_col = (255, 100, 100, 80)
    draw.line([(MARGIN, 0), (MARGIN, H)], fill=margin_col, width=2)
    draw.line([(W - MARGIN, 0), (W - MARGIN, H)], fill=margin_col, width=2)


def _label_band(draw, y_top, y_bot, label, color, tag_x=None):
    """Draw a semi-transparent band and a label tag on the right."""
    r, g, b = color
    # Horizontal rule at top and bottom of band
    draw.line([(0, y_top), (W, y_top)], fill=(r, g, b, 160), width=3)
    draw.line([(0, y_bot), (W, y_bot)], fill=(r, g, b, 160), width=3)
    # Side brace on the right
    brace_x = W - 60
    draw.line([(brace_x, y_top), (brace_x, y_bot)], fill=(r, g, b, 200), width=4)
    draw.line([(brace_x, y_top), (brace_x + 20, y_top)], fill=(r, g, b, 200), width=4)
    draw.line([(brace_x, y_bot), (brace_x + 20, y_bot)], fill=(r, g, b, 200), width=4)
    # Label pill
    f = _font('Arial-Bold', 38)
    bb = draw.textbbox((0, 0), label, font=f)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    mid_y = (y_top + y_bot) // 2
    pad_x, pad_y = 24, 14
    pill_x = W - 70 - tw - pad_x * 2
    pill_y = mid_y - th // 2 - pad_y
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + tw + pad_x * 2, pill_y + th + pad_y * 2],
        radius=12, fill=(r, g, b, 220)
    )
    draw.text((pill_x + pad_x, pill_y + pad_y), label, font=f, fill='white')


def anatomy():
    img = Image.new('RGB', (W, H), '#f0f2f6')
    draw = ImageDraw.Draw(img, 'RGBA')

    _grid(draw)

    # ── Zone coordinates (mirroring slide_01 layout) ─────────────────────────
    # Breadcrumb
    bc_top, bc_bot = 110, 170

    # Hero (two lines ~90px Arial-Black)
    hero_top = 189
    hero_bot = 189 + 110 + 7 + 110 + 10   # approx two lines

    # Body text paragraph
    body_top = hero_bot + 44
    body_bot = body_top + 52 * 3           # ~3 lines at 52px leading

    # Lead-in
    lead_top = body_bot + 20
    lead_bot = lead_top + 58

    # Card area + footer (mirroring slide_02a: CALLOUT_H=210, gap=32 above footer, gap=48 below)
    CALLOUT_H = 210
    content_bottom = H - BOTTOM_BAR - 48
    footer_top = content_bottom - CALLOUT_H
    card_top = lead_bot + 40
    card_bot = footer_top - 32

    # Bottom bar
    bar_top = H - BOTTOM_BAR

    # ── Draw zone fills ───────────────────────────────────────────────────────
    zones = [
        (bc_top,   bc_bot,   (200, 50,  50),  'breadcrumb'),
        (hero_top, hero_bot, (30,  80,  180), 'hero'),
        (body_top, body_bot, (30,  140, 100), 'body text'),
        (lead_top, lead_bot, (160, 80,  200), 'lead-in'),
        (card_top, card_bot, (200, 120, 30),  'card area'),
        (footer_top, content_bottom, (0, 160, 160), 'footer'),
    ]

    for y0, y1, col, label in zones:
        r, g, b = col
        draw.rectangle([0, y0, W, y1], fill=(r, g, b, 28))
        _label_band(draw, y0, y1, label, col)

    # Bottom bar fill
    draw.rectangle([0, bar_top, W, H], fill=(200, 50, 50, 180))
    draw.text((W // 2, bar_top + BOTTOM_BAR // 2),
              'bottom bar', font=_font('Arial-Bold', 22),
              fill='white', anchor='mm')

    # ── Placeholder text in each zone ────────────────────────────────────────
    # Breadcrumb
    draw.text((MARGIN, (bc_top + bc_bot) // 2), 'BREADCRUMB',
              font=_font('Arial-Bold', 34), fill=(200, 50, 50), anchor='lm')

    # Hero
    draw.text((MARGIN, hero_top + 10), 'Hero line one',
              font=_font('Arial-Black', 90), fill=(30, 80, 180, 200))
    draw.text((MARGIN, hero_top + 10 + 110 + 7), 'hero line two (accent color).',
              font=_font('Arial-Black', 90), fill=(30, 80, 180, 140))

    # Body text
    draw.text((MARGIN, body_top + 10), 'Body text — supporting paragraph, regular weight, ~36px',
              font=_font('Arial', 40), fill=(30, 140, 100, 200))

    # Lead-in
    draw.text((MARGIN, lead_top + 10), 'Lead-in — bold bridge sentence into cards.',
              font=_font('Arial-Bold', 40), fill=(160, 80, 200, 220))

    # Card area — two placeholder cards
    GAP = 48
    card_w = (W - 2 * MARGIN - GAP) // 2
    for i, label in enumerate(['left card', 'right card']):
        cx = MARGIN + i * (card_w + GAP)
        draw.rounded_rectangle(
            [cx, card_top, cx + card_w, card_bot],
            radius=10,
            outline=(200, 120, 30, 200), width=4,
            fill=(200, 120, 30, 18)
        )
        draw.text((cx + card_w // 2, (card_top + card_bot) // 2),
                  label, font=_font('Arial-Bold', 56),
                  fill=(200, 120, 30, 200), anchor='mm')

    # Footer placeholder
    draw.rounded_rectangle(
        [MARGIN, footer_top, W - MARGIN, content_bottom],
        radius=6,
        outline=(0, 160, 160, 200), width=4,
        fill=(0, 160, 160, 18)
    )
    draw.rectangle([MARGIN, footer_top, MARGIN + 8, content_bottom], fill=(0, 160, 160, 200))
    draw.text((MARGIN + 8 + 26, (footer_top + content_bottom) // 2),
              'footer — contextual callout, left red border, ~210px tall',
              font=_font('Arial', 40), fill=(0, 160, 160, 220), anchor='lm')

    # ── Dimension callouts ────────────────────────────────────────────────────
    # Canvas size label
    draw.text((W // 2, 50), f'canvas  {W} × {H} px',
              font=_font('Arial', 34), fill=(80, 80, 80), anchor='mm')
    # Margin callout
    draw.text((MARGIN // 2, H // 2), f'{MARGIN}px',
              font=_font('Arial', 30), fill=(200, 50, 50), anchor='mm')
    draw.text((W - MARGIN // 2, H // 2), f'{MARGIN}px',
              font=_font('Arial', 30), fill=(200, 50, 50), anchor='mm')

    out = os.path.join(BASE_DIR, 'anatomy_slide.png')
    img.save(out)
    print(f'saved → {out}')


if __name__ == '__main__':
    anatomy()

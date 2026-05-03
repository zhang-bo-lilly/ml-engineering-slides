import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


def _text_h(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]


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



def _draw_card(draw, x, y, w, h, name, color, specs, badge_num=None):
    HEADER_H = 88
    PAD = 22
    BADGE_D = 38

    # Card
    draw.rectangle([x, y, x + w, y + h], fill='#ffffff', outline='#e5e7eb', width=1)
    draw.rectangle([x, y, x + w, y + HEADER_H], fill=color)

    # Numbered badge (white circle with number in card color)
    if badge_num is not None:
        fb = _font('Arial-Bold', 24)
        bt = str(badge_num)
        bx = x + w - BADGE_D - 10
        by = y + (HEADER_H - BADGE_D) // 2
        draw.ellipse([bx, by, bx + BADGE_D, by + BADGE_D], fill='#ffffff')
        btw = int(draw.textlength(bt, font=fb))
        bth = _text_h(draw, bt, fb)
        draw.text((bx + (BADGE_D - btw) // 2, by + (BADGE_D - bth) // 2),
                  bt, font=fb, fill=color)

    # Cluster name — fit to header width
    fn = _font('Arial-Black', 42)
    fn_sm = _font('Arial-Black', 30)
    avail_name_w = w - PAD * 2 - (BADGE_D + 20 if badge_num is not None else 0)
    actual_font = fn if draw.textlength(name, font=fn) <= avail_name_w else fn_sm
    nh = _text_h(draw, name, actual_font)
    draw.text((x + PAD, y + (HEADER_H - nh) // 2), name, font=actual_font, fill='#ffffff')

    # Specs
    fl = _font('Arial-Bold', 24)
    fv = _font('Arial', 30)
    fs = _font('Arial', 24)
    text_w = w - PAD * 2
    ty = y + HEADER_H + PAD
    for spec in specs:
        label = spec[0]
        value = spec[1]
        sub = spec[2] if len(spec) > 2 else None
        if label:
            draw.text((x + PAD, ty), label.upper(), font=fl, fill='#9ca3af')
            ty += 28
        for line in _wrap(draw, value, fv, text_w):
            draw.text((x + PAD, ty), line, font=fv, fill='#1a1a1a')
            ty += 40
        if sub:
            for line in _wrap(draw, sub, fs, text_w - 24):
                draw.text((x + PAD + 24, ty), line, font=fs, fill='#6b7280')
                ty += 32


def draw_platform_map():
    W, H = 2492, 950

    CONSOL_W = 1495
    BOX_GAP = 40
    STAYS_W = W - CONSOL_W - BOX_GAP   # 957

    MAIN_H = 810
    WEKA_GAP = 18
    WEKA_H = H - MAIN_H - WEKA_GAP     # 122

    LABEL_H = 52
    OUTER_PAD = 20
    INNER_GAP = 16
    BORDER_W = 3

    card_h = MAIN_H - LABEL_H * 2 - OUTER_PAD * 2   # 666

    # Consolidated: 3 inner cards
    consol_avail_w = CONSOL_W - OUTER_PAD * 2 - INNER_GAP * 2   # 1423
    consol_cw = consol_avail_w // 3                               # 474

    # Stays: 2 inner cards
    stays_avail_w = STAYS_W - OUTER_PAD * 2 - INNER_GAP          # 901
    stays_cw = stays_avail_w // 2                                 # 450

    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    fl_label = _font('Arial-Bold', 28)
    fl_label_sm = _font('Arial-Bold', 24)

    # ── CONSOLIDATED BOX ────────────────────────────────────────────────────
    draw.rectangle([0, 0, CONSOL_W, MAIN_H], fill='#f0fdf9', outline='#10b981', width=BORDER_W)
    draw.text((20, 12), 'CONSOLIDATED', font=fl_label, fill='#059669')
    lbl_text = 'JOINS THE WEKA FABRIC'
    draw.text((20, MAIN_H - LABEL_H + 14), lbl_text, font=fl_label, fill='#059669')
    # Badge ① after the label
    lbl_w = int(draw.textlength(lbl_text, font=fl_label))
    lbl_h = _text_h(draw, lbl_text, fl_label)
    BADGE_D = 34
    bx1 = 20 + lbl_w + 14
    by1 = MAIN_H - LABEL_H + 14 + (lbl_h - BADGE_D) // 2
    draw.ellipse([bx1, by1, bx1 + BADGE_D, by1 + BADGE_D], fill='#059669')
    fb_n = _font('Arial-Bold', 22)
    n1w = int(draw.textlength('1', font=fb_n))
    n1h = _text_h(draw, '1', fb_n)
    draw.text((bx1 + (BADGE_D - n1w) // 2, by1 + (BADGE_D - n1h) // 2), '1', font=fb_n, fill='#ffffff')

    inner_y = LABEL_H + OUTER_PAD
    consol_cards = [
        ('LillyPod',      '#10b981', None, [
            ('GPUs',   '1,016 × B300'),
            ('Fabric', '800G compute + storage'),
        ]),
        ('MagTrain',      '#6366f1', None, [
            ('GPUs',   '72× H100'),
            ('',       '64× H200'),
            ('',       '32× L40S'),
            ('Fabric', '400G compute + storage'),
        ]),
        ('New hardware',  '#0ea5e9', 2,    [
            ('GPUs',  '256× RTX 6000 Pro', '96 GB  ·  32 servers'),
            ('Nodes', '16× CPU fat nodes', '4K cores  ·  32TB RAM'),
        ]),
    ]
    for i, (name, color, badge_num, specs) in enumerate(consol_cards):
        ix = OUTER_PAD + i * (consol_cw + INNER_GAP)
        _draw_card(draw, ix, inner_y, consol_cw, card_h, name, color, specs, badge_num)

    # ── STAYS DISTRIBUTED BOX ───────────────────────────────────────────────
    sx0 = CONSOL_W + BOX_GAP
    draw.rectangle([sx0, 0, sx0 + STAYS_W, MAIN_H], fill='#fffbeb', outline='#f59e0b', width=BORDER_W)
    draw.text((sx0 + 20, 12), 'STAYS DISTRIBUTED', font=fl_label, fill='#d97706')
    draw.text((sx0 + 20, MAIN_H - LABEL_H + 14), 'Weka NFS mount in 2026  ·  fabric membership Q1 2027',
              font=fl_label_sm, fill='#d97706')

    stays_cards = [
        ('MD3',               '#f59e0b', None, [
            ('GPUs',    '600× L4  (24 GB)'),
            ('',        '256× RTX 6000 Pro  (96 GB)'),
        ]),
        ('+256× RTX 6000 Pro', '#fb923c', 3, [
            ('GPUs',    '256× RTX 6000 Pro  (96 GB)'),
        ]),
    ]
    for i, (name, color, badge_num, specs) in enumerate(stays_cards):
        sx = sx0 + OUTER_PAD + i * (stays_cw + INNER_GAP)
        _draw_card(draw, sx, inner_y, stays_cw, card_h, name, color, specs, badge_num)

    # ── WEKA BAR ────────────────────────────────────────────────────────────
    wy = MAIN_H + WEKA_GAP
    draw.rectangle([0, wy, W, wy + WEKA_H], fill='#eff6ff', outline='#3b82f6', width=BORDER_W)
    fw = _font('Arial-Black', 36)
    fb_n = _font('Arial-Bold', 22)
    weka_text = 'Weka hot tier  +2PB  ·  4PB → 6PB  ·  additional nodes, not drive expansion'
    wb = draw.textbbox((0, 0), weka_text, font=fw)
    ww, wh = wb[2] - wb[0], wb[3] - wb[1]
    tx = (W - ww) // 2
    ty_w = wy + (WEKA_H - wh) // 2
    draw.text((tx, ty_w), weka_text, font=fw, fill='#1d4ed8')
    # Badge ④ after the text
    BADGE_D = 34
    bx4 = tx + ww + 16
    by4 = ty_w + (wh - BADGE_D) // 2
    draw.ellipse([bx4, by4, bx4 + BADGE_D, by4 + BADGE_D], fill='#3b82f6')
    n4w = int(draw.textlength('4', font=fb_n))
    n4h = _text_h(draw, '4', fb_n)
    draw.text((bx4 + (BADGE_D - n4w) // 2, by4 + (BADGE_D - n4h) // 2), '4', font=fb_n, fill='#ffffff')

    out = os.path.join(BASE_DIR, 'diagram_platform_map.png')
    img.save(out)
    print(f'saved {out}')


if __name__ == '__main__':
    draw_platform_map()

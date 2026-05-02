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


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        if draw.textlength(test, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines


def draw_cluster_diagram():
    W, H = 2492, 860
    CARD_GAP = 36
    CARD_W = (W - 2 * CARD_GAP) // 3
    HEADER_H = 108
    PAD = 40
    PAIN_H = 140

    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    clusters = [
        {
            'name': 'LillyPod',
            'color': '#10b981',
            'specs': [
                ('GPUs',        '1,016 × B300'),
                ('Fabric',      '800G compute + storage'),
                ('Filesystem',  'Weka (native)'),
                ('Hot tier',    '4 PB'),
                ('Warm tier',   '7 PB'),
            ],
            'status': 'Platform anchor',
            'pain': None,
        },
        {
            'name': 'MagTrain',
            'color': '#6366f1',
            'specs': [
                ('GPUs',        '72 × H100  ·  64 × H200  ·  32 × L40S'),
                ('Fabric',      '400G compute + storage'),
                ('Filesystem',  'Dell Isilon  500 TB'),
                ('Weka',        'NFS mount only'),
            ],
            'status': None,
            'pain': 'Weka via NFS → GPU idle when users accidentally use it inside workloads',
        },
        {
            'name': 'MD3',
            'color': '#f59e0b',
            'specs': [
                ('GPUs',        '600 × L4  (24 GB, 6-way)'),
                ('',            '256 × RTX 6000 Pro  (96 GB, 8-way)'),
                ('Fabric',      'None  ·  NFS over Isilon'),
                ('Weka',        'NFS mount only'),
            ],
            'status': None,
            'pain': 'No fast storage or compute fabric — GPU servers behind a plain queue',
        },
    ]

    for i, c in enumerate(clusters):
        cx = i * (CARD_W + CARD_GAP)

        # Card body
        draw.rectangle([cx, 0, cx + CARD_W, H - 1], fill='#f8f9fa')
        draw.rectangle([cx, 0, cx + CARD_W, H - 1], outline='#e5e7eb', width=2)

        # Colored header
        draw.rectangle([cx, 0, cx + CARD_W, HEADER_H], fill=c['color'])
        draw.text((cx + PAD, 20), c['name'], font=_font('Arial-Black', 54), fill='#ffffff')

        # Specs
        ty = HEADER_H + 32
        flabel = _font('Arial-Bold', 26)
        fvalue = _font('Arial', 30)

        for label, value in c['specs']:
            if label:
                draw.text((cx + PAD, ty), label.upper(), font=flabel, fill='#9ca3af')
                ty += 32
            draw.text((cx + PAD, ty), value, font=fvalue, fill='#1a1a1a')
            ty += 46

        # Status badge
        if c['status']:
            bw = int(draw.textlength(c['status'], font=flabel)) + 44
            by = H - PAIN_H - 4
            draw.rectangle([cx + PAD, by, cx + PAD + bw, by + 44], fill=c['color'])
            draw.text((cx + PAD + 22, by + 8), c['status'], font=flabel, fill='#ffffff')

        # Pain point strip
        if c['pain']:
            py = H - PAIN_H
            draw.rectangle([cx + 2, py, cx + CARD_W - 2, H - 2], fill='#fff1f2')
            draw.rectangle([cx + 2, py, cx + 10, H - 2], fill='#d32030')
            fpain = _font('Arial', 27)
            lines = wrap_text(draw, c['pain'], fpain, CARD_W - PAD * 2 - 14)
            lty = py + 18
            for line in lines:
                draw.text((cx + 26, lty), line, font=fpain, fill='#b91c1c')
                lty += 38

    out = os.path.join(BASE_DIR, 'diagram_clusters.png')
    img.save(out)
    print(f'saved {out}')


if __name__ == '__main__':
    draw_cluster_diagram()

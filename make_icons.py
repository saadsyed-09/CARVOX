import os
from PIL import Image, ImageDraw

RES = 'android/app/src/main/res'
fg = Image.open('assets/icon-foreground.png').convert('RGBA')
full = Image.open('assets/icon-only.png').convert('RGBA')
DENS = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

for name, m in DENS.items():
    out = os.path.join(RES, 'mipmap-' + name)
    os.makedirs(out, exist_ok=True)
    a = int(108 * m)
    fg.resize((a, a), Image.LANCZOS).save(os.path.join(out, 'ic_launcher_foreground.png'))
    l = int(48 * m)
    sq = full.resize((l, l), Image.LANCZOS)
    sq.save(os.path.join(out, 'ic_launcher.png'))
    big = 4
    mask = Image.new('L', (l * big, l * big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, l * big - 1, l * big - 1), fill=255)
    mask = mask.resize((l, l), Image.LANCZOS)
    rd = Image.new('RGBA', (l, l), (0, 0, 0, 0))
    rd.paste(sq, (0, 0), mask)
    rd.save(os.path.join(out, 'ic_launcher_round.png'))

vals = os.path.join(RES, 'values')
os.makedirs(vals, exist_ok=True)
with open(os.path.join(vals, 'ic_launcher_background.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#050608</color>\n</resources>\n')
print('icons written')

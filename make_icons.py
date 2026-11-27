#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path('.')
RES = ROOT / 'android/app/src/main/res'
SIZES = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

def choose(*names):
    for folder in (ROOT, ROOT / 'assets'):
        for name in names:
            path = folder / name
            if path.exists():
                return path
    raise SystemExit('Missing logo asset. Upload icon-only.png and icon-foreground.png.')

full = Image.open(choose('icon-only.png', 'Icon.png')).convert('RGB').resize((512, 512), Image.Resampling.LANCZOS)
foreground = Image.open(choose('icon-foreground.png')).convert('RGBA')

for density, scale in SIZES.items():
    size = round(192 * scale)
    folder = RES / f'mipmap-{density}'
    folder.mkdir(parents=True, exist_ok=True)
    full.resize((size, size), Image.Resampling.LANCZOS).save(folder / 'ic_launcher.png', optimize=True)
    round_icon = full.resize((size, size), Image.Resampling.LANCZOS).convert('RGBA')
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    round_icon.putalpha(mask)
    round_icon.save(folder / 'ic_launcher_round.png', optimize=True)
    fg_canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    fg = foreground.copy()
    fg.thumbnail((round(size * .66), round(size * .66)), Image.Resampling.LANCZOS)
    fg_canvas.alpha_composite(fg, ((size - fg.width) // 2, (size - fg.height) // 2))
    fg_canvas.save(folder / 'ic_launcher_foreground.png', optimize=True)

values = RES / 'values'
values.mkdir(parents=True, exist_ok=True)
(values / 'ic_launcher_background.xml').write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">#05070C</color></resources>\n',
    encoding='utf-8'
)
adaptive = RES / 'mipmap-anydpi-v26'
adaptive.mkdir(parents=True, exist_ok=True)
xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@mipmap/ic_launcher_foreground"/></adaptive-icon>
'''
(adaptive / 'ic_launcher.xml').write_text(xml, encoding='utf-8')
(adaptive / 'ic_launcher_round.xml').write_text(xml, encoding='utf-8')
print('CARVOX launcher icons generated. Existing splash screen files were not changed.')

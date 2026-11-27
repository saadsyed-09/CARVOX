#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

ROOT = Path('.')
RES = ROOT / 'android/app/src/main/res'
SIZES = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

def choose(*names):
    for folder in (ROOT, ROOT / 'assets'):
        for name in names:
            p = folder / name
            if p.exists():
                return p
    raise SystemExit('Missing logo asset. Upload icon-only.png (or Icon.png) to repository root.')

# icon-only is the full white-background square artwork. icon-foreground is
# transparent foreground art; fall back safely if only one image was uploaded.
full_path = choose('icon-only.png', 'Icon.png', 'icon-foreground.png')
full = Image.open(full_path).convert('RGB')
full = full.resize((512, 512), Image.Resampling.LANCZOS)
try:
    fg = Image.open(choose('icon-foreground.png')).convert('RGBA')
except SystemExit:
    fg = full.convert('RGBA')

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
    # Android adaptive foreground: use the full safe area, not the old 108dp
    # thumbnail which made the mark look extremely small.
    fg_canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    fg_fit = fg.copy()
    fg_fit.thumbnail((round(size * .66), round(size * .66)), Image.Resampling.LANCZOS)
    fg_canvas.alpha_composite(fg_fit, ((size-fg_fit.width)//2, (size-fg_fit.height)//2))
    fg_canvas.save(folder / 'ic_launcher_foreground.png', optimize=True)

values = RES / 'values'
values.mkdir(parents=True, exist_ok=True)
(values / 'ic_launcher_background.xml').write_text("""<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources><color name=\"ic_launcher_background\">#FFFFFF</color></resources>\n""", encoding='utf-8')

adaptive = RES / 'mipmap-anydpi-v26'
adaptive.mkdir(parents=True, exist_ok=True)
xml = """<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<adaptive-icon xmlns:android=\"http://schemas.android.com/apk/res/android\"><background android:drawable=\"@color/ic_launcher_background\"/><foreground android:drawable=\"@mipmap/ic_launcher_foreground\"/></adaptive-icon>\n"""
(adaptive / 'ic_launcher.xml').write_text(xml, encoding='utf-8')
(adaptive / 'ic_launcher_round.xml').write_text(xml, encoding='utf-8')

# Android 12+ requires a system splash window. Make it white and visually blank
# (transparent centered drawable) so the oversized/tiny old logo is not shown.
drawable = RES / 'drawable-nodpi'
drawable.mkdir(parents=True, exist_ok=True)
Image.new('RGBA', (1, 1), (255, 255, 255, 0)).save(drawable / 'splash_blank.png')
styles = values / 'styles.xml'
if styles.exists():
    text = styles.read_text(encoding='utf-8')
    # Keep existing styles/parents intact and inject splash items into launch style.
    pattern = r'(<style\s+name="AppTheme\.NoActionBarLaunch"[^>]*>)(.*?)(</style>)'
    match = __import__('re').search(pattern, text, flags=__import__('re').S)
    if match:
        body = match.group(2)
        for item in ('windowSplashScreenBackground', 'windowSplashScreenAnimatedIcon', 'postSplashScreenTheme', 'android:windowBackground', 'android:background'):
            body = __import__('re').sub(r'<item\s+name="'+item+r'"[^>]*>.*?</item>\s*', '', body)
        body += '\n        <item name="windowSplashScreenBackground">#FFFFFF</item>\n        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_blank</item>\n        <item name="postSplashScreenTheme">@style/AppTheme.NoActionBar</item>\n        <item name="android:windowBackground">@android:color/white</item>\n        <item name="android:background">@android:color/white</item>\n    '
        text = text[:match.start(2)] + body + text[match.end(2):]
        styles.write_text(text, encoding='utf-8')
print('Launcher assets generated; white background and splash configuration applied.')

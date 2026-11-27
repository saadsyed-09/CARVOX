
import os
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
SIZES = {
    "mdpi": 1,
    "hdpi": 1.5,
    "xhdpi": 2,
    "xxhdpi": 3,
    "xxxhdpi": 4
}

def pick(name):
    for folder in (".", "assets"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return path
    raise SystemExit(f"Missing {name}. Upload it to repo root.")

# Transparent black logo foreground
fg = Image.open(pick("icon-foreground.png")).convert("RGBA")

# Complete white-background launcher icon
full = Image.open(pick("icon-only.png")).convert("RGBA")

for name, scale in SIZES.items():
    size = int(192 * scale)
    out = os.path.join(RES, f"mipmap-{name}")
    os.makedirs(out, exist_ok=True)

    # Adaptive foreground with transparent padding
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fg.thumbnail((int(108 * scale), int(108 * scale)),
                 Image.Resampling.LANCZOS)

    x = (size - fg.width) // 2
    y = (size - fg.height) // 2
    canvas.alpha_composite(fg, (x, y))

    canvas.save(os.path.join(out, "ic_launcher_foreground.png"))

    # Standard launcher icon
    icon = full.resize(
        (size, size), Image.Resampling.LANCZOS
    )
    icon.save(os.path.join(out, "ic_launcher.png"))

    # Round launcher icon
    round_icon = icon.copy()
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    round_icon.putalpha(mask)
    round_icon.save(os.path.join(out, "ic_launcher_round.png"))

# Pure white adaptive background
values = os.path.join(RES, "values")
os.makedirs(values, exist_ok=True)

with open(os.path.join(values, "ic_launcher_background.xml"),
          "w", encoding="utf-8") as f:
    f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#FFFFFF</color>
</resources>
''')

print("CARVOX launcher icons generated successfully!")

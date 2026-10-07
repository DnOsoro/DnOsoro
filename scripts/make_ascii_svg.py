"""Convert source-prepped.png into a self-typing monochrome ASCII SVG.
On a dark card, lit areas should be DENSE glyphs, so density follows brightness
inside the subject; the white background becomes blank. STATIC=1 = frozen frame."""
import os, sys
from html import escape
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 100
FONT, CW, LH = 7, 4.2, 7.6
STATIC = os.environ.get("STATIC") == "1"
src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"

img = Image.open(src).convert("L")
rows_n = max(1, round(COLS * img.height / img.width * 0.5))
small = img.resize((COLS, rows_n), Image.LANCZOS)
try:                                              # local contrast at grid resolution (sharper eyes/brows)
    import cv2
    arr = np.asarray(small)
    bg0 = arr > 247
    arr = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(5, 5)).apply(arr)
    arr[bg0] = 255
    small = Image.fromarray(arr)
except ImportError:
    pass
a = np.asarray(small, dtype=float) / 255.0
bgmask = a > 0.97                               # background -> blank
# histogram-equalise the subject so every glyph level gets used (keeps detail on dark skin)
vals = a[~bgmask]
order = np.argsort(np.argsort(vals)) / max(len(vals) - 1, 1)
d = np.zeros_like(a)
d[~bgmask] = order
d = 0.04 + 0.96 * (d ** 1.15)                 # bright -> dense; slight push for deeper shadows
d[bgmask] = 0.0

W, H = COLS * CW + 16, rows_n * LH + 16
parts = []
for r in range(rows_n):
    line = "".join(RAMP[int(v * (len(RAMP) - 1) + 0.5)] for v in d[r]).rstrip()
    if not line.strip():
        continue
    y = 8 + (r + 1) * LH
    txt = (f'<text x="8" y="{y:.1f}" textLength="{len(line)*CW:.1f}" lengthAdjust="spacing" '
           f'xml:space="preserve"@@ATTR@@>{escape(line)}</text>')
    if STATIC:
        parts.append(txt.replace("@@ATTR@@", ""))
    else:
        parts.append(
          f'<clipPath id="c{r}"><rect x="8" y="{y-LH:.1f}" width="0" height="{LH+1:.1f}">'
          f'<animate attributeName="width" from="0" to="{COLS*CW:.1f}" begin="{0.15 + r*0.07:.2f}s" dur="0.9s" fill="freeze"/>'
          f'</rect></clipPath>' + txt.replace("@@ATTR@@", f' clip-path="url(#c{r})"'))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<style>text{{font:{FONT}px ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace;fill:#c9d1d9;white-space:pre}}</style>
<rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="#0d1117" stroke="#30363d"/>
{chr(10).join(parts)}
</svg>'''
open("portrait-ascii.svg", "w").write(svg)
print("wrote portrait-ascii.svg", COLS, "x", rows_n)

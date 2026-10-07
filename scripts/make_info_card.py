"""Neofetch-style info card SVG. STATIC=1 emits a frozen frame."""
import os
from html import escape
from config import HANDLE, INFO

STATIC = os.environ.get("STATIC") == "1"
W, LH, TOP = 490, 24, 66
H = TOP + (len(INFO) + 3) * LH + 20
COLORS = ["#7ee787", "#79c0ff", "#d2a8ff", "#ffa657", "#ff7b72", "#f2cc60"]

rows = [
    f'<g class="l" style="animation-delay:0.2s"><text x="24" y="{TOP}" class="k" fill="#7ee787">{escape(HANDLE)}</text></g>',
    f'<g class="l" style="animation-delay:0.35s"><text x="24" y="{TOP+LH}" class="v">{"-"*len(HANDLE)}</text></g>',
]
for i, (k, v) in enumerate(INFO):
    y = TOP + (i + 2) * LH
    c = COLORS[i % len(COLORS)]
    rows.append(f'<g class="l" style="animation-delay:{0.5 + i*0.18:.2f}s">'
                f'<text x="24" y="{y}" class="k" fill="{c}">{escape(k)}</text>'
                f'<text x="128" y="{y}" class="v">{escape(v)}</text></g>')
y = TOP + (len(INFO) + 2) * LH + 8
rows.append(f'<g class="l" style="animation-delay:{0.6+len(INFO)*0.18:.2f}s">'
            + "".join(f'<rect x="{24+i*26}" y="{y-12}" width="22" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(COLORS))
            + '</g>')

anim = "" if STATIC else (
  ".l{opacity:0;animation:f .5s ease-out forwards}"
  "@keyframes f{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}")
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
  .k{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
  .v{{font:14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#c9d1d9}}
  {anim}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M0 34V10a10 10 0 0 1 10-10h{W-20}a10 10 0 0 1 10 10v24z" fill="#161b22"/>
<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="38" cy="17" r="5" fill="#ffbd2e"/><circle cx="56" cy="17" r="5" fill="#27c93f"/>
<text x="{W//2}" y="22" text-anchor="middle" class="v" style="font-size:12px;fill:#8b949e">neofetch</text>
{chr(10).join(rows)}
</svg>'''
open("info-card.svg", "w").write(svg)
print("wrote info-card.svg")

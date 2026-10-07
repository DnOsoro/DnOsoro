"""Grouped skills panel."""
from html import escape
from config import STACK
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
W, LABW, ROWH, TOP = 860, 190, 46, 52
COLORS = ["#79c0ff", "#7ee787", "#f2cc60", "#d2a8ff", "#ffa657"]
H = TOP + len(STACK) * ROWH + 8
rows = []
n = 0
for r, (label, items) in enumerate(STACK):
    y = TOP + r * ROWH
    c = COLORS[r % len(COLORS)]
    rows.append(f'<g class="f" style="animation-delay:{0.15*r:.2f}s"><text x="22" y="{y+19}" class="l" fill="{c}">{escape(label)}</text>')
    x = LABW
    for it in items:
        w = len(it) * 7.6 + 24
        rows.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".6"/>'
                    f'<text x="{x+w/2:.0f}" y="{y+19}" text-anchor="middle" class="c">{escape(it)}</text>')
        x += w + 10
    rows.append('</g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} .l{{font-size:13px;font-weight:700}} .c{{font-size:12px;fill:#c9d1d9}} .t{{font-size:13px;font-weight:600;fill:#c9d1d9}}
.f{{opacity:0;animation:f .5s ease-out forwards}}@keyframes f{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}</style>
<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>
<text x="22" y="30" class="t">$ ls ~/stack</text>
{chr(10).join(rows)}
</svg>'''
open("stack.svg", "w").write(svg); print("wrote stack.svg")

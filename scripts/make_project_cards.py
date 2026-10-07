"""One clickable-friendly SVG card per featured project."""
import textwrap
from html import escape
from config import PROJECTS
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
W, H = 424, 150
for i, (repo, pitch, tags) in enumerate(PROJECTS, 1):
    lines = textwrap.wrap(pitch, 46)[:3]
    body = "".join(f'<text x="22" y="{66+j*19}" class="d">{escape(l)}</text>' for j, l in enumerate(lines))
    x, chips = 22, ""
    for t in tags:
        w = len(t) * 6.8 + 18
        chips += (f'<rect x="{x:.0f}" y="116" width="{w:.0f}" height="22" rx="11" fill="#79c0ff" fill-opacity=".12" stroke="#79c0ff" stroke-opacity=".5"/>'
                  f'<text x="{x+w/2:.0f}" y="131" text-anchor="middle" class="g">{escape(t)}</text>')
        x += w + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} .r{{font-size:15px;font-weight:700;fill:#58a6ff}} .d{{font-size:12px;fill:#c9d1d9}} .g{{font-size:10.5px;fill:#79c0ff}} .a{{font-size:12px;fill:#7ee787}}
.f{{opacity:0;animation:f .6s ease-out {0.15*i:.2f}s forwards}}@keyframes f{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
<g class="f"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<text x="22" y="34" class="r">{escape(repo)}</text><text x="{W-22}" y="34" text-anchor="end" class="a">view repo →</text>
{body}{chips}</g></svg>'''
    open(f"card-{i}.svg", "w").write(svg)
print("wrote", len(PROJECTS), "cards")

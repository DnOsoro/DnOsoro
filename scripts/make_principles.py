"""Three engineering principles (from the openstore design) + link buttons."""
import textwrap
from html import escape
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
P = [("Validate before you transform", "Pandera checks on raw tables: non-null keys, valid statuses, positive prices.", "#7ee787"),
     ("Guard what AI generates", "LLM-written SQL must pass SELECT-only guardrails before touching the database.", "#ff7b72"),
     ("Show your work", "The UI displays the exact SQL that ran, so every answer can be audited.", "#79c0ff")]
W, H, CWD, G = 860, 132, 272, 22
parts = []
for i, (t, d, c) in enumerate(P):
    x = i * (CWD + G)
    lines = "".join(f'<text x="{x+18}" y="{66+j*17}" class="d">{escape(l)}</text>' for j, l in enumerate(textwrap.wrap(d, 36)))
    parts.append(f'<g class="f" style="animation-delay:{0.2*i:.2f}s"><rect x="{x+.5}" y=".5" width="{CWD-1}" height="{H-1}" rx="12" fill="#0d1117" stroke="#30363d"/>'
                 f'<rect x="{x+18}" y="20" width="26" height="4" rx="2" fill="{c}"/>'
                 f'<text x="{x+18}" y="46" class="h" fill="{c}">{escape(t)}</text>{lines}</g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} .h{{font-size:13.5px;font-weight:700}} .d{{font-size:11.5px;fill:#c9d1d9}}
.f{{opacity:0;animation:f .6s ease-out forwards}}@keyframes f{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
{chr(10).join(parts)}</svg>'''
open("principles.svg", "w").write(svg)

def button(name, label, fill, stroke, color, w):
    open(name, "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 42" width="{w}" height="42">
<style>text{{font-family:{FONT};font-size:13px;font-weight:700;fill:{color}}}</style>
<rect x=".5" y=".5" width="{w-1}" height="41" rx="21" fill="{fill}" stroke="{stroke}"/>
<text x="{w/2}" y="26" text-anchor="middle">{label}</text></svg>''')
button("btn-demo.svg",   "▶  Live demo",   "#238636", "#2ea043", "#ffffff", 170)
button("btn-source.svg", "{ }  Source code", "#161b22", "#30363d", "#c9d1d9", 190)
button("btn-linkedin.svg", "in  Connect on LinkedIn", "#0a66c2", "#378fe9", "#ffffff", 240)
print("wrote principles + buttons")

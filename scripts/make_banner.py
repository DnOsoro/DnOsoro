"""Hero banner: name, typed positioning line, animated data-flow motif. STATIC=1 = frozen frame."""
import os
from html import escape
from config import NAME, TAGLINE
STATIC = os.environ.get("STATIC") == "1"
W, H = 860, 190
CW = 9.6
tw = len(TAGLINE) * CW
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
anim_w = "" if STATIC else f'<animate attributeName="width" from="0" to="{tw:.0f}" begin="0.7s" dur="3s" fill="freeze"/>'
cur = (f'<rect x="{32+tw+4:.0f}" y="116" width="9" height="19" fill="#79c0ff" opacity="{1 if STATIC else 0}">'
       + ("" if STATIC else '<animate attributeName="opacity" values="1;0;1" dur="1s" begin="3.8s" repeatCount="indefinite"/>') + '</rect>')
# data-flow motif (right): source -> bronze -> silver -> gold with travelling dots
nodes = [(676, "#79c0ff"), (726, "#cd7f32"), (776, "#c0c0c0"), (826, "#f2cc60")]
y = 95
motif = f'<path id="p" d="M{nodes[0][0]} {y} H{nodes[-1][0]}" stroke="#30363d" stroke-width="2" fill="none"/>'
for x, c in nodes:
    motif += f'<circle cx="{x}" cy="{y}" r="9" fill="#0d1117" stroke="{c}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3.5" fill="{c}"/>'
if not STATIC:
    for k in range(3):
        motif += (f'<circle r="3" fill="#7ee787"><animateMotion dur="3.2s" begin="{k*1.07:.2f}s" repeatCount="indefinite">'
                  f'<mpath href="#p"/></animateMotion></circle>')
for x, lab in zip([n[0] for n in nodes], ["ingest", "bronze", "silver", "gold"]):
    motif += f'<text x="{x}" y="{y+30}" text-anchor="middle" class="m">{lab}</text>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} .p{{font-size:12px;fill:#7ee787}} .n{{font-size:42px;font-weight:700;fill:#e6edf3}}
.t{{font-size:16px;fill:#79c0ff}} .m{{font-size:10px;fill:#8b949e}} .r{{font-size:12px;fill:#8b949e}}</style>
<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect width="5" height="{H}" rx="2" fill="#26a641"/>
<text x="32" y="40" class="p">$ whoami</text>
<text x="32" y="92" class="n">{escape(NAME)}</text>
<text x="34" y="154" class="r">Data Engineer · pipelines · lakehouses · RAG</text>
<clipPath id="tc"><rect x="32" y="102" width="{tw if STATIC else 0:.0f}" height="34">{anim_w}</rect></clipPath>
<text x="32" y="130" class="t" clip-path="url(#tc)" textLength="{tw:.0f}" lengthAdjust="spacing" xml:space="preserve">{escape(TAGLINE)}</text>
{cur}
{motif}
</svg>'''
open("banner.svg", "w").write(svg); print("wrote banner.svg")

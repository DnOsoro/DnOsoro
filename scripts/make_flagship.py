"""openstore: real architecture, two lanes (data pipeline + AI query path)."""
from html import escape
W, H = 860, 336
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
BW, BH, GAP, X0 = 130, 74, 40.5, 24
A_Y, B_Y = 68, 216
laneA = [("Data lake", "CSV · S3 API", "SeaweedFS", "#79c0ff"),
         ("raw", "untouched copy", "PostgreSQL", "#cd7f32"),
         ("staging", "typed + renamed", "casts · cleanup", "#c0c0c0"),
         ("core", "dim + fact tables", "dim_customers · fct_orders", "#f2cc60"),
         ("analytics", "business-ready views", "3 curated views", "#7ee787")]
laneB = [("Question", "plain English", "Next.js UI", "#79c0ff"),
         ("LLM", "writes the SQL", "Gemini · OpenRouter", "#d2a8ff"),
         ("Guardrails", "SELECT-only · LIMIT", "blocks DDL / DML", "#ff7b72"),
         ("PostgreSQL", "runs validated SQL", "analytics views", "#7ee787"),
         ("Answer", "SQL + table + chart", "FastAPI · Recharts", "#f2cc60")]
parts = []
def lane(items, y, base, label):
    parts.append(f'<text x="{X0}" y="{y-12}" class="lane">{label}</text>')
    for i, (t, sub, tech, c) in enumerate(items):
        x = X0 + i * (BW + GAP); d = base + i * 0.3
        parts.append(f'<g class="f" style="animation-delay:{d:.2f}s"><rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="10" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-width="1.5"/>'
                     f'<text x="{x+BW/2}" y="{y+24}" text-anchor="middle" class="h" fill="{c}">{escape(t)}</text>'
                     f'<text x="{x+BW/2}" y="{y+43}" text-anchor="middle" class="s">{escape(sub)}</text>'
                     f'<text x="{x+BW/2}" y="{y+61}" text-anchor="middle" class="k">{escape(tech)}</text></g>')
        if i < len(items) - 1:
            ax1, ax2, ay = x + BW + 6, x + BW + GAP - 6, y + BH / 2
            parts.append(f'<g class="f" style="animation-delay:{d+0.2:.2f}s"><line class="flow" x1="{ax1}" x2="{ax2-4}" y1="{ay}" y2="{ay}"/>'
                         f'<path d="M{ax2-8} {ay-5} L{ax2} {ay} L{ax2-8} {ay+5}" fill="none" stroke="#8b949e" stroke-width="1.6"/></g>')
lane(laneA, A_Y, 0.2, "DATA PIPELINE")
lane(laneB, B_Y, 1.9, "AI QUERY PATH")
# Pandera pill on staging box
sx = X0 + 2 * (BW + GAP) + BW / 2
parts.append(f'<g class="f" style="animation-delay:1.0s"><rect x="{sx-56}" y="{A_Y-10}" width="112" height="19" rx="9.5" fill="#0d1117" stroke="#7ee787"/>'
             f'<text x="{sx}" y="{A_Y+3}" text-anchor="middle" class="b">✓ Pandera checks</text></g>')
# analytics -> PostgreSQL connector
ax = X0 + 4 * (BW + GAP) + BW / 2; bx = X0 + 3 * (BW + GAP) + BW / 2
ymid = (A_Y + BH + B_Y) / 2
parts.append(f'<g class="f" style="animation-delay:2.4s"><path class="flow" d="M{ax} {A_Y+BH} V{ymid} H{bx} V{B_Y-2}" fill="none"/>'
             f'<path d="M{bx-5} {B_Y-9} L{bx} {B_Y-2} L{bx+5} {B_Y-9}" fill="none" stroke="#8b949e" stroke-width="1.6"/>'
             f'<text x="{(ax+bx)/2}" y="{ymid-6}" text-anchor="middle" class="s">AI reads curated views only</text></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
 text{{font-family:{FONT}}} .h{{font-size:15px;font-weight:700}} .s{{font-size:10.5px;fill:#8b949e}} .k{{font-size:11px;fill:#c9d1d9}}
 .t{{font-size:13px;font-weight:600;fill:#c9d1d9}} .lane{{font-size:10.5px;font-weight:700;fill:#6e7681;letter-spacing:1.5px}} .b{{font-size:10px;fill:#7ee787;font-weight:600}}
 .f{{opacity:0;animation:f .6s ease-out forwards}} @keyframes f{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
 .flow{{stroke:#8b949e;stroke-width:1.6;stroke-dasharray:5 4;animation:d 1s linear infinite}} @keyframes d{{to{{stroke-dashoffset:-9}}}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>
<text x="{X0}" y="32" class="t">$ ./openstore --architecture</text>
<text x="{W-24}" y="32" text-anchor="end" class="s">end-to-end · deployed on Vercel</text>
{chr(10).join(parts)}
</svg>'''
open("openstore-architecture.svg", "w").write(svg); print("wrote openstore-architecture.svg")

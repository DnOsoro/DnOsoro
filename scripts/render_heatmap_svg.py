"""Render data/contributions.json as an animated heatmap SVG."""
import json, datetime as dt
from config import USERNAME

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, PAD_L, PAD_T = 13, 3, 40, 52
STEP = CELL + GAP

data = json.load(open("data/contributions.json"))
days = data["days"]
first = dt.date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7          # GitHub weeks start on Sunday

cells, months_seen = [], {}
for i, d in enumerate(days):
    w, row = divmod(i + offset, 7)
    date = dt.date.fromisoformat(d["date"])
    months_seen.setdefault(date.strftime("%Y-%m"), (w, date.strftime("%b")))
    level = 5 if d["count"] >= 12 else min(d["level"], 4)   # level 5 = neon top end
    delay = (w + row) * 0.022
    x, y = PAD_L + w * STEP, PAD_T + row * STEP
    cells.append(
        f'<rect class="c" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[level]}"/>')

weeks = (len(days) + offset + 6) // 7
W = PAD_L + weeks * STEP + 16
H = PAD_T + 7 * STEP + 56

labels, last_w = [], -10
for _, (w, name) in months_seen.items():
    if w - last_w >= 3:
        labels.append(f'<text x="{PAD_L + w*STEP}" y="{PAD_T-10}" class="t">{name}</text>')
        last_w = w
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    labels.append(f'<text x="6" y="{PAD_T + r*STEP + 11}" class="t">{name}</text>')

legend_x = W - 16 - (len(PALETTE) * STEP + 80)
legend = [f'<text x="{legend_x}" y="{H-18}" class="t">Less</text>']
for i, c in enumerate(PALETTE):
    legend.append(f'<rect x="{legend_x + 32 + i*STEP}" y="{H-29}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
legend.append(f'<text x="{legend_x + 36 + len(PALETTE)*STEP}" y="{H-18}" class="t">More</text>')

bd = data["best_day"]
footer = (f'{data["total"]:,} contributions in the last year  |  '
          f'streak {data["current_streak"]}d (longest {data["longest_streak"]}d)  |  '
          f'best day {bd["count"]}')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
  .t{{font:11px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e}}
  .title{{font:600 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#c9d1d9}}
  .c{{opacity:0;transform-box:fill-box;animation:in .45s ease-out forwards}}
  @keyframes in{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<text x="{PAD_L}" y="22" class="title">$ ./contributions.sh --user {USERNAME}</text>
{chr(10).join(labels)}
{chr(10).join(cells)}
<text x="{PAD_L}" y="{H-18}" class="t">{footer}</text>
{chr(10).join(legend)}
</svg>'''
open("contrib-heatmap.svg", "w").write(svg)
print("wrote contrib-heatmap.svg", W, "x", H)

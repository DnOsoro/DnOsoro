"""Scrape the public contribution calendar (no token needed)."""
import json, re, sys, datetime as dt
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
from config import USERNAME

URL = f"https://github.com/users/{USERNAME}/contributions"

def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    counts = {}
    for tip in soup.select("tool-tip"):
        m = re.match(r"(No|\d+) contributions?", tip.get_text(strip=True))
        if m and tip.get("for"):
            counts[tip["for"]] = 0 if m.group(1) == "No" else int(m.group(1))

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        if not td.get("data-date"):
            continue
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": counts.get(td.get("id"), 0),
        })
    days.sort(key=lambda d: d["date"])
    if not days:
        sys.exit("No contribution cells found; GitHub markup may have changed.")

    total = sum(d["count"] for d in days)
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["count"] > 0:
            current += 1
        elif i == 0:
            continue          # today may not have activity yet
        else:
            break
    best = max(days, key=lambda d: d["count"])
    months = OrderedDict()
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]

    out = {
        "username": USERNAME, "generated": dt.datetime.now(dt.timezone.utc).isoformat(),
        "total": total, "current_streak": current, "longest_streak": longest,
        "best_day": best, "months": months, "days": days,
    }
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"{len(days)} days, {total} contributions, streak {current}/{longest}")

if __name__ == "__main__":
    main()

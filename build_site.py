#!/usr/bin/env python3
"""
Assemble the publishable, self-contained index.html.

  python3 build_data.py     # regenerate route_weather.json from the model
  python3 build_site.py     # inline data + Chart.js into index.html

Produces a single file with no network dependencies, so it renders on a phone
with no signal — which is where it will actually get used.
"""
import json, datetime, pathlib, sys

VERSION = "1.0"
REPO = "https://github.com/YOUR-USERNAME/plateau-passage-weather"

here = pathlib.Path(__file__).parent
tpl = (here / "template.html").read_text()
data = json.loads((here / "route_weather.json").read_text())

vendor = here / "vendor" / "chart.umd.js"
if not vendor.exists():
    sys.exit("Missing vendor/chart.umd.js — run:  npm install chart.js@4.4.1  "
             "and copy node_modules/chart.js/dist/chart.umd.js into vendor/")

html = (tpl
        .replace("__CHARTJS__", vendor.read_text())
        .replace("__DATA__", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
        .replace("__VERSION__", VERSION)
        .replace("__BUILT__", datetime.date.today().strftime("%B %Y"))
        .replace("__REPO__", REPO))

for token in ("__CHARTJS__", "__DATA__", "__VERSION__", "__BUILT__", "__REPO__"):
    assert token not in html, f"unsubstituted placeholder: {token}"

out = here / "index.html"
out.write_text(html)
print(f"wrote {out.name}  ({len(html)/1024:.0f} KB, {len(data)} days, no external requests)")

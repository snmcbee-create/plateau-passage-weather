#!/usr/bin/env python3
"""
Assemble the publishable, self-contained index.html.

  python3 build_data.py     # regenerate route_weather.json from the model
  python3 build_site.py     # inline data + Chart.js into index.html

Produces a single file with no network dependencies, so it renders on a phone
with no signal — which is where it will actually get used.
"""
import json, datetime, pathlib, sys

VERSION = "1.2"
REPO = "https://github.com/snmcbee-create/plateau-passage-weather"

here = pathlib.Path(__file__).parent
def load(name):
    p = here / name
    if not p.exists():
        sys.exit(f"Missing {name} — run:  python3 build_data.py && python3 build_guide.py")
    return json.loads(p.read_text())


tpl = (here / "template.html").read_text()
data = load("route_weather.json")
resupply = load("resupply.json")
packing = load("packing.json")
seasonal = load("seasonal.json")


def j(o):
    return json.dumps(o, separators=(",", ":"), ensure_ascii=False)

vendor = here / "vendor" / "chart.umd.js"
if not vendor.exists():
    sys.exit("Missing vendor/chart.umd.js — run:  npm install chart.js@4.4.1  "
             "and copy node_modules/chart.js/dist/chart.umd.js into vendor/")

SUBS = {
    "__CHARTJS__": vendor.read_text(),
    "__DATA__": j(data),
    "__RESUPPLY__": j(resupply),
    "__PACKING__": j(packing),
    "__SEASONAL__": j(seasonal),
    "__VERSION__": VERSION,
    "__BUILT__": datetime.date.today().strftime("%B %Y"),
    "__REPO__": REPO,
}

html = tpl
for token, value in SUBS.items():
    html = html.replace(token, value)

for token in SUBS:
    assert token not in html, f"unsubstituted placeholder: {token}"
assert 'src="http' not in html, "index.html must have no external requests"

out = here / "index.html"
out.write_text(html)
print(f"wrote {out.name}  ({len(html)/1024:.0f} KB)")
print(f"  {len(data)} days · {len(resupply['stops'])} resupply stops · "
      f"{sum(len(v) for v in packing.values())} packing items · "
      f"{len(seasonal)} access notes · no external requests")

#!/usr/bin/env python3
"""
Apply community reports and rebuild.

Workflow when someone files a water or business report via the GitHub issue forms:

  1. Read the issue. Sanity-check it — does the mile match a point that exists?
     Does the date make sense? Is the reporter describing the source you think
     they are?
  2. Append an entry to the "reports" array in reports.json:

        {"kind":"water", "mile":845, "date":"2026-10-15",
         "status":"none", "text":"Both tanks bone dry, ash in the basin.",
         "by":"@handle"}

  3. Run this script. It validates, rebuilds, and tells you what changed.
  4. Commit, push. Close the issue with a link to the live page.

Reports OUTRANK my defaults: a reported point shows the reporter's status, is
tagged "Rider reported", and displays their note inline with the date. Newest
report wins for status; all reports are kept and shown.
"""
import json, pathlib, subprocess, sys

VALID_WATER = {"tap","developed","perennial","seasonal","intermittent","none"}
here = pathlib.Path(__file__).parent

data = json.loads((here / "reports.json").read_text())
reports = data.get("reports", [])

import build_supply
biz_miles = {b[0] for b in build_supply.BIZ}
water_miles = {w[0] for w in build_supply.WATER}

errs = []
for i, r in enumerate(reports):
    where = f"reports[{i}]"
    for f in ("kind", "mile", "date", "text"):
        if f not in r:
            errs.append(f"{where}: missing '{f}'")
    if r.get("kind") == "water":
        if r.get("status") not in VALID_WATER:
            errs.append(f"{where}: status must be one of {sorted(VALID_WATER)}")
        if r.get("mile") not in water_miles:
            errs.append(f"{where}: mile {r.get('mile')} is not a known water point. "
                        f"Nearest: {sorted(water_miles, key=lambda m: abs(m-r.get('mile',0)))[:3]}")
    elif r.get("kind") == "business":
        if r.get("mile") not in biz_miles:
            errs.append(f"{where}: mile {r.get('mile')} has no business entry")
        if "name" not in r:
            errs.append(f"{where}: business reports need 'name' to match against")
    else:
        errs.append(f"{where}: kind must be 'water' or 'business'")
    d = str(r.get("date", ""))
    if len(d) != 10 or d[4] != "-" or d[7] != "-":
        errs.append(f"{where}: date must be YYYY-MM-DD, got {d!r}")

if errs:
    print("REPORTS REJECTED — nothing was rebuilt:\n")
    for e in errs:
        print("  ✗ " + e)
    sys.exit(1)

print(f"{len(reports)} report(s) validated.")
for r in reports:
    extra = f" → {r['status']}" if r["kind"] == "water" else ""
    print(f"  ✓ {r['date']}  mi {r['mile']:<5} {r['kind']}{extra}  ({r.get('by','anonymous')})")

for script in ("build_supply.py", "build_site.py"):
    print(f"\n$ python3 {script}")
    subprocess.run([sys.executable, str(here / script)], check=True, cwd=here)
print("\nDone. Review index.html, then commit and push.")

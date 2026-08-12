#!/usr/bin/env python3
"""
Business directory + water sources, with explicit provenance on every field.

TWO THINGS THIS FILE REFUSES TO DO
  1. Present hours as fact. Rural hours drift seasonally and aggregators lag by
     months. Every hours string carries a source and a date-checked stamp, and
     the UI renders them as unverified.
  2. Invent water. Water is the most safety-critical and least verifiable data
     on this route. Anything not a town tap or an agency-maintained spigot is
     marked low confidence and says so. See CONFIDENCE below.

CONFIDENCE LADDER (applies to both tables)
  verified  multiple independent sources agree, or confirmed by managing agency
  listed    single aggregator/business listing, plausible, NOT confirmed
  reported  submitted by a rider or local via the report form (see reports.json)
  inferred  my reasoning from context — treat as a hypothesis
  unknown   listed so you know it exists, nothing more

Community reports in reports.json OVERRIDE these defaults and bump confidence
to "reported" with the reporter's date. Run merge_reports.py after adding any.
"""
import json, pathlib, datetime

CHECKED = "August 2026"   # when the listings below were last pulled

# ---------------------------------------------------------------------------
# BUSINESSES — keyed to route mile. Phones and addresses cross-checked across
# at least two sources where marked "verified".
# (mile, town, name, kind, address, phone, hours, closed_days, conf, note)
# ---------------------------------------------------------------------------
BIZ = [
 (180, "St. George, UT", "Supermarkets (multiple)", "grocery",
  "Bluff St / St George Blvd", None, "Generally 6am–11pm, 7 days", "",
  "verified", "Chain supermarkets, open Sundays. Full outdoor and bike shops in town. "
  "Best gear town on the western half — sort cold-weather kit here, not Cedar City."),

 (295, "Cedar City, UT", "Supermarkets (multiple)", "grocery",
  "Main St corridor", None, "Generally 6am–midnight, 7 days", "",
  "verified", "Last full-service town before the high plateaus. Open Sundays. "
  "Outdoor shop and bike shop in town."),

 (400, "Panguitch, UT", "Joe's Main Street Market", "grocery",
  "10 S Main St, Panguitch, UT 84759", "(435) 676-2361",
  "Mon–Sat 7:30am–9pm", "Sun",
  "listed", "First real grocery since Cedar City. CLOSED SUNDAYS. Sources disagree on "
  "the opening hour (7:00 / 7:30 / 8:00) — call ahead."),

 (450, "Bryce Canyon, UT", "Ruby's Inn General Store", "grocery",
  "26 S Main St, Bryce Canyon City, UT 84764", "(435) 834-5341",
  "Seasonal; typically 7am–9pm, 7 days", "",
  "listed", "Large general store, tourist pricing, open 7 days — which makes it the "
  "Sunday fallback in a stretch where everything else shuts."),

 (570, "Escalante, UT", "Griffin's Grocery & General Merchandise", "grocery",
  "30 W Main St, Escalante, UT 84726", "(435) 826-4226",
  "Mon–Sat 8am–7pm", "Sun",
  "verified", "The bigger of Escalante's two groceries and the last real one for ~285 mi. "
  "CLOSED SUNDAYS."),

 (570, "Escalante, UT", "Escalante Mercantile & Natural Grocery", "grocery",
  "210 W Main St, Escalante, UT 84726", "(435) 826-4114",
  "Mon–Sat 8am–5pm", "Sun",
  "verified", "Smaller, natural-foods leaning, closes earlier. Also CLOSED SUNDAYS. "
  "Post office in town is the smart mail-drop for the eastern half."),

 (625, "Boulder, UT", "Hills & Hollows Market", "store",
  "840 W Hwy 12, Boulder, UT 84716", "(435) 335-7349",
  "Daily 9am–7pm", "",
  "listed", "Small but genuinely useful, and open 7 days. A meal and a partial top-up, "
  "not a resupply."),

 (625, "Boulder, UT", "Burr Trail Grill", "restaurant",
  "10 N State Hwy 12, Boulder, UT 84716", "(435) 335-7511",
  "Mon–Wed & Fri 11am–5pm, Thu 11am–2:30pm", "Sat, Sun (varies)",
  "listed", "Seasonal and short hours. Do not plan a day around it."),

 (680, "Torrey, UT", "Chuckwagon General Store (Austin's)", "grocery",
  "12 W Main St, Torrey, UT 84775", "(435) 425-3335",
  "Daily 7am–10pm", "",
  "verified", "~9 mi off route and worth it. Bakery/deli plus groceries, open 7 days. "
  "Best food between Escalante and Blanding, and the last before the Hwy 95 void."),

 (680, "Loa, UT", "Royal's Foodtown", "grocery",
  "135 W Main St, Loa, UT 84747", "(435) 836-2841",
  "Mon–Thu 7am–7:30pm, Fri–Sat 7am–8pm", "Sun",
  "listed", "NOTE: this is in Loa, ~13 mi past Torrey — often mislabelled as Torrey's "
  "store. Bigger than the Chuckwagon but a real detour, and closed Sundays."),

 (745, "Hanksville, UT", "Hollow Mountain", "gas",
  "60 N Hwy 95, Hanksville, UT 84734", "(435) 542-3298",
  "Approx. 7am–10pm, 7 days", "",
  "listed", "Gas station and convenience store built into the rock. Open 7 days, which "
  "matters because this is the load before 110 mi of nothing. Listed hours vary by "
  "source and one listing was self-inconsistent — call."),

 (745, "Hanksville, UT", "Duke's Slickrock Grill", "restaurant",
  "275 E Hwy 24, Hanksville, UT 84734", "(435) 542-3235",
  "Mon–Sat 7am–10pm", "Sun (varies)",
  "listed", "Hot meal before the Hwy 95 stretch. Seasonal hours."),

 (800, "Hite, UT", "Hite Outpost — CLOSED", "closed",
  "Hwy 95 at Colorado River", None, "All services suspended since 2021", "All",
  "verified", "Store, fuel, ranger station and marina all closed 'until further notice' "
  "per NPS. Older route notes still list this as a resupply. THEY ARE WRONG."),

 (830, "Natural Bridges NM, UT", "Visitor Center", "water",
  "Hwy 275, Lake Powell, UT 84533", "(435) 692-1234",
  "Typically 9am–5pm, seasonal", "",
  "verified", "NO FOOD SOLD. Potable water at the VC is the only reliable water in a long "
  "dry stretch — and it is shut off after the first hard freeze. Call before you rely on it."),

 (855, "Blanding, UT", "Clark's Market", "grocery",
  "820 S Main St, Blanding, UT 84511", "(435) 678-2721",
  "Mon–Sat 7am–9pm", "Sun",
  "verified", "~14 mi off route. The supermarket that breaks the Hwy 95 carry — "
  "and it is CLOSED SUNDAYS. Arriving Sunday after a 110 mi carry is the classic mistake."),

 (915, "Monticello, UT", "Blue Mountain Foods", "grocery",
  "64 W Center St, Monticello, UT 84535", "(435) 587-2451",
  "Mon–Sat 7am–9pm", "Sun",
  "listed", "Full grocery, laundry and motels in town. CLOSED SUNDAYS. A second listing "
  "gives (435) 587-2727 — try both."),

 (1020, "Moab, UT", "City Market & others", "grocery",
  "425 S Main St, Moab, UT 84532", "(435) 259-5181",
  "Typically 6am–11pm, 7 days", "",
  "verified", "Full supermarket, open Sundays. Multiple bike shops — best on the route. "
  "Fix everything here; nothing comparable until Durango."),

 (1125, "Naturita, CO", "Wild Gal's Market", "grocery",
  "152 E Main St, Naturita, CO 81422", "(970) 738-0067",
  "Tue–Fri 10am–6pm, Sat–Sun 10am–4pm", "Mon",
  "verified", "Real groceries and produce. NOTE THE MONDAY CLOSURE and the late 10am "
  "opening — this is not a dawn-departure resupply."),

 (1125, "Nucla, CO", "Naturita Sales", "gas",
  "150 W Main St, Nucla, CO 81424", "(970) 865-2616",
  "Mon–Sat 5am–9pm, Sun 6am–9pm", "",
  "verified", "Gas, deli, pizza slices, convenience goods. Open 7 days with long hours — "
  "the reliable backstop when Wild Gal's is shut."),

 (1165, "Norwood, CO", "Mesa Rose Kitchen + Grocery", "grocery",
  "Grand Ave, Norwood, CO 81423", None, "Hours not confirmed", "",
  "unknown", "Small grocery section plus coffee and a rotating menu. I could not confirm "
  "phone or hours from a reliable source — treat as unverified and have a fallback. "
  "The Divide Restaurant is the other option in town."),

 (1185, "Telluride, CO", "Supermarket & bike shops", "grocery",
  "Downtown Telluride, CO 81435", None, "Generally 7am–9pm, 7 days", "",
  "verified", "~13 mi off route and a descent you must climb back out of. Worth it only "
  "for a bike shop or a weather bail-out. Open Sundays."),

 (1195, "Rico, CO", "Rico cafe / small store", "restaurant",
  "Glasgow Ave, Rico, CO 81332", None, "Very limited, seasonal", "",
  "unknown", "A hot meal on the cold side of Lizard Head Pass if you are lucky. "
  "Do not plan food around it."),

 (1210, "Durango, CO", "Full services", "grocery",
  "Durango, CO 81301", None, "Everything, 7 days", "",
  "verified", "Eastern terminus. Supermarkets, bike shops, train, airport."),
]

# ---------------------------------------------------------------------------
# WATER — the honest table.
# reliability: tap | developed | perennial | seasonal | intermittent | none
# (mile, name, reliability, conf, treat, note)
# ---------------------------------------------------------------------------
WATER = [
 (0,    "Las Vegas — town water",            "tap",       "verified", False,
  "Fill to full capacity. Next certain water is Mesquite."),
 (55,   "Lovell Canyon / Spring Mtns",       "seasonal",  "inferred", True,
  "Springs exist in the Spring Mountains but I cannot confirm any specific one is "
  "flowing in October. Plan the Las Vegas → Mesquite leg as a full dry carry."),
 (120,  "Mesquite — town water",             "tap",       "verified", False, ""),
 (180,  "St. George — town water",           "tap",       "verified", False, ""),
 (235,  "Springdale / Virgin River",         "perennial", "verified", True,
  "Town taps in Springdale. The Virgin River is perennial but silty — pre-filter."),
 (295,  "Cedar City — town water",           "tap",       "verified", False, ""),
 (340,  "Cedar Breaks NM",                   "seasonal",  "listed",   False,
  "Visitor centre water is seasonal and the facility closes for winter in October. "
  "Do not count on it. Brian Head village is largely shut this month."),
 (400,  "Panguitch — town water",            "tap",       "verified", False, ""),
 (450,  "Bryce Canyon NP / Ruby's Inn",      "tap",       "verified", False,
  "NPS visitor centre and the general store both have water."),
 (510,  "Cannonville / Paria River",         "intermittent","inferred", True,
  "Tiny town taps if anything is open. The Paria is heavily silted — a pre-filter is "
  "the difference between filtering and destroying a filter."),
 (570,  "Escalante — town water",            "tap",       "verified", False, ""),
 (625,  "Boulder — town water",              "tap",       "verified", False,
  "Boulder Creek nearby and generally flowing."),
 (680,  "Torrey / Fremont River",            "tap",       "verified", True,
  "Town taps. Capitol Reef's Fruita campground has potable water seasonally."),
 (745,  "Hanksville — town water",           "tap",       "verified", False,
  "LAST CERTAIN WATER before the Hwy 95 stretch. Fill everything. The Dirty Devil "
  "and Fremont here are silty and mineralised — poor sources even filtered."),
 (762,  "Poison Spring",                     "intermittent","unknown", True,
  "~17 mi south of Hanksville off SR-95. Named Poison Spring, which is reason enough "
  "for caution, and I have no reliable report of its current state or potability. "
  "TREAT AS UNAVAILABLE when planning."),
 (778,  "Hog Springs rest area",             "seasonal",  "listed",   True,
  "Developed BLM rest stop on Hwy 95 with picnic tables, vault toilet and a creek. "
  "The creek is the water — there is no confirmed potable spigot. Reported as the most "
  "useful source in this stretch, but unconfirmed for October."),
 (800,  "Hite / Colorado River",             "perennial", "verified", True,
  "ALL SERVICES CLOSED. The river is there but access is degraded by very low lake "
  "levels, and the water is heavily silted. A last resort, not a plan."),
 (830,  "Natural Bridges NM visitor centre", "developed", "verified", False,
  "The one dependable tap between Hanksville and Blanding — AND IT IS TURNED OFF after "
  "the first hard freeze, which the weather model puts near 29% on your arrival night. "
  "Call (435) 692-1234 before you plan the carry around it."),
 (845,  "Elk Ridge springs & stock tanks",   "intermittent","unknown", True,
  "Bikepacking Roots' own guidance is 'do not plan on every stock tank having water'. "
  "Post-Babylon-Fire, ash contamination is an additional unknown. LOWEST CONFIDENCE "
  "POINT ON THE ROUTE."),
 (855,  "Blanding — town water",             "tap",       "verified", False, ""),
 (915,  "Monticello — town water",           "tap",       "verified", False, ""),
 (960,  "Canyonlands rim / Lockhart Basin",  "none",      "verified", False,
  "NO WATER. Potholes hold water after rain and are otherwise dry and ecologically "
  "sensitive. Carry everything from Monticello."),
 (1020, "Moab — town water",                 "tap",       "verified", False, ""),
 (1050, "La Sal Mountains creeks",           "perennial", "listed",   True,
  "Montane creeks, generally flowing in October and the best natural water on the route."),
 (1075, "Paradox Valley",                    "intermittent","inferred", True,
  "Scarce and unreliable. Carry from the La Sals."),
 (1125, "Naturita / San Miguel River",       "tap",       "verified", True,
  "Town water in both Naturita and Nucla."),
 (1165, "Norwood — town water",              "tap",       "verified", False, ""),
 (1195, "Rico / Dolores River",              "perennial", "listed",   True, ""),
 (1210, "Durango — finish",                  "tap",       "verified", False, ""),
]

RELIABLE = {"tap", "developed"}   # what counts when computing dry stretches

# Sources that are reliable UNTIL they aren't. Natural Bridges is the one that
# matters: it is the only dependable tap between Hanksville and Blanding, and it
# is switched off after the first hard freeze — roughly a 1-in-3 chance on the
# night you'd arrive, rising fast through late October. Treating it as reliable
# hides the route's real worst case, so dry stretches are computed twice.
CONDITIONAL = {830: "shut off after the first hard freeze"}


def load_reports(here):
    """Community reports override defaults. See .github/ISSUE_TEMPLATE/."""
    p = here / "reports.json"
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("reports", [])


def build(here):
    reports = load_reports(here)
    by_mile = {}
    for r in reports:
        by_mile.setdefault((r["kind"], r["mile"]), []).append(r)

    biz = []
    for m, town, name, kind, addr, phone, hours, closed, conf, note in BIZ:
        rep = by_mile.get(("business", m), [])
        match = [r for r in rep if r.get("name", "").lower() in name.lower()]
        biz.append({
            "mile": m, "town": town, "name": name, "kind": kind, "addr": addr,
            "phone": phone, "hours": hours, "closed": closed,
            "conf": "reported" if match else conf,
            "note": note, "checked": CHECKED,
            "reports": [{"date": r["date"], "text": r["text"],
                         "by": r.get("by", "anonymous")} for r in match],
        })

    water = []
    for m, name, rel, conf, treat, note in WATER:
        rep = [r for r in by_mile.get(("water", m), [])]
        latest = max(rep, key=lambda r: r["date"]) if rep else None
        water.append({
            "mile": m, "name": name,
            "rel": latest["status"] if latest else rel,
            "conf": "reported" if latest else conf,
            "treat": treat, "note": note, "checked": CHECKED,
            "reports": [{"date": r["date"], "status": r["status"],
                         "text": r["text"], "by": r.get("by", "anonymous")}
                        for r in sorted(rep, key=lambda r: r["date"], reverse=True)],
        })

    for w in water:
        w["conditional"] = CONDITIONAL.get(w["mile"])

    def stretches(include_conditional):
        pts = [w for w in water if w["rel"] in RELIABLE
               and (include_conditional or not w["conditional"])]
        out = []
        for a, b in zip(pts, pts[1:]):
            d = b["mile"] - a["mile"]
            between = [w for w in water if a["mile"] < w["mile"] < b["mile"]]
            unknown = sum(1 for w in between if w["conf"] in ("unknown", "inferred"))
            # distance drives it, but a stretch whose only en-route options are
            # guesses is worse than one with nothing at all, because riders plan
            # around the guesses.
            score = d + 20 * unknown
            out.append({
                "from": a["name"].split(" —")[0], "to": b["name"].split(" —")[0],
                "fromMile": a["mile"], "toMile": b["mile"], "miles": d,
                "litres": round(min(9, max(2, d / 60 * 3)) * 2) / 2,
                "unknown": unknown, "score": round(score),
                "between": [{"name": w["name"], "rel": w["rel"], "conf": w["conf"]}
                            for w in between],
                "severity": "critical" if score >= 110 else "watch" if score >= 60 else "ok",
            })
        return out

    normal = stretches(True)
    worst = stretches(False)
    # the stretches that only appear once conditional taps are off
    new_worst = [g for g in worst
                 if not any(n["fromMile"] == g["fromMile"] and n["toMile"] == g["toMile"]
                            for n in normal)]
    return biz, water, {"normal": normal, "worst": worst, "newInWorst": new_worst}


def sunday_risk(start="2026-10-01"):
    """Which resupply days land on a day the store is shut.

    Every major grocery on the Utah half closes Sundays. Wild Gal's in Naturita
    closes Mondays. This is the single most avoidable way to arrive at a locked
    door after a long carry.
    """
    from datetime import date, timedelta
    MILES = [0, 55, 120, 180, 235, 295, 340, 400, 450, 510, 570, 625, 680,
             745, 800, 855, 915, 970, 1020, 1075, 1125, 1165, 1210]
    y, m, d = map(int, start.split("-"))
    s = date(y, m, d)
    out = []
    for i, mi in enumerate(MILES):
        day = s + timedelta(days=i)
        dow = day.strftime("%a")
        shut = [b for b in BIZ if b[0] == mi and dow in (b[7] or "")]
        if shut:
            out.append({
                "date": day.strftime("%b %-d"), "dow": day.strftime("%A"),
                "mile": mi, "town": shut[0][1],
                "shut": [b[2] for b in shut],
                "open": [b[2] for b in BIZ if b[0] == mi and dow not in (b[7] or "")],
            })
    return {"start": start, "hits": out}


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    biz, water, dry = build(here)
    sun = sunday_risk()

    (here / "businesses.json").write_text(json.dumps(biz, indent=1))
    (here / "water.json").write_text(json.dumps(
        {"points": water, "dry": dry, "sunday": sun}, indent=1))

    print(f"{'Mi':>5}  {'Business':<38}{'Phone':<17}{'Conf':<9}Closed")
    print("-" * 88)
    for b in biz:
        print(f"{b['mile']:>5}  {b['name'][:36]:<38}{(b['phone'] or '—'):<17}"
              f"{b['conf']:<9}{b['closed'] or '—'}")

    print(f"\n{'Mi':>5}  {'Water':<38}{'Reliability':<14}Confidence")
    print("-" * 80)
    for w in water:
        flag = "  " if w["conf"] in ("verified",) else ("??" if w["conf"] == "unknown" else " ~")
        print(f"{flag}{w['mile']:>4}  {w['name'][:36]:<38}{w['rel']:<14}{w['conf']}")

    def show(rows, n=5):
        for g in sorted(rows, key=lambda g: -g["score"])[:n]:
            f = {"critical": "!!", "watch": " !", "ok": "  "}[g["severity"]]
            print(f"{f} {g['from'][:24]:<25}→ {g['to'][:24]:<25}{g['miles']:>4} mi  "
                  f"~{g['litres']}L  {g['unknown']} unknown en route")

    print("\nDRY STRETCHES — normal case (all taps working)")
    print("-" * 80)
    show(dry["normal"])
    print("\nDRY STRETCHES — worst case (Natural Bridges tap shut off)")
    print("-" * 80)
    show(dry["worst"])
    if dry["newInWorst"]:
        print("\n  ⚠ only appears once conditional taps fail:")
        for g in dry["newInWorst"]:
            print(f"    {g['from']} → {g['to']}: {g['miles']} mi, ~{g['litres']}L, "
                  f"{g['unknown']} unknown sources en route")

    print(f"\nSUNDAY/CLOSED-DAY RISK — start {sun['start']}")
    print("-" * 80)
    if not sun["hits"]:
        print("  none")
    for h in sun["hits"]:
        print(f"  {h['date']} ({h['dow']}) mi {h['mile']} {h['town']}: "
              f"{', '.join(h['shut'])} SHUT"
              + (f" · open: {', '.join(h['open'])}" if h["open"] else " · NO ALTERNATIVE"))

    lo = sum(1 for w in water if w["conf"] in ("unknown", "inferred"))
    print(f"\n{len(biz)} businesses · {len(water)} water points "
          f"({lo} low-confidence) · {len(dry['normal'])} dry stretches")
    print(f"{len(load_reports(here))} community reports merged")

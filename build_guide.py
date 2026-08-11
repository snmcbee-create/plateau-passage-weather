#!/usr/bin/env python3
"""
Resupply model + weather-driven packing list for the Plateau Passage.

Resupply mileages are DERIVED, not surveyed. They come from the 23-day itinerary
in build_data.py plus known town locations. Bikepacking Roots' official route
guide has the authoritative mile markers — cross-check before you rely on these.
Confidence is tagged per row so readers can see which numbers are soft.

Writes resupply.json and packing.json.
"""
import json, pathlib

# ---------------------------------------------------------------------------
# TIERS — what you can actually accomplish at a stop
#   full     supermarket; you can rebuild the whole food bag, any diet
#   good     real grocery; a few days of decent food, some fresh
#   moderate small market / gas-and-deli; calories yes, choice no
#   minimal  one tiny store or a cafe; a snack top-up, assume nothing
#   none     no food for sale at all
# ---------------------------------------------------------------------------
R = [
 # mile, name, state, off_route_mi, tier, water, conf, services, note
 (0,   "Las Vegas",                "NV", 0.0, "full", "town", "high",
  "Supermarkets · bike shops · post office · airport",
  "Western terminus. Last true metro until Durango. Buy anything specialised here."),
 (55,  "Mountain Springs / Hwy 160","NV", 1.0, "minimal", "none", "low",
  "Seasonal roadside cafe/bar",
  "Do not count on it. Treat Las Vegas → Mesquite as fully self-supported."),
 (120, "Mesquite",                 "NV", 2.0, "full", "town", "high",
  "Supermarkets · pharmacy · motels · post office",
  "Full rebuild before the climb into Utah. Also last cheap groceries for a while."),
 (180, "St. George",               "UT", 0.0, "full", "town", "high",
  "Supermarkets · outdoor shops · bike shops · post office",
  "Best gear town on the western half. Sort cold-weather kit HERE, not Cedar City."),
 (235, "Springdale / Rockville",   "UT", 1.5, "moderate", "town", "med",
  "Tourist market · cafes · outfitter",
  "Zion gateway. Small selection at resort prices. Fine for a top-up, poor for a rebuild."),
 (295, "Cedar City",               "UT", 0.0, "full", "town", "high",
  "Supermarkets · outdoor shop · bike shop · post office · bus",
  "THE HINGE. Last full-service town before the high plateaus. Freezing nights start "
  "tomorrow — this is the mail-drop and warm-gear decision point."),
 (340, "Brian Head",               "UT", 2.0, "minimal", "town", "low",
  "Resort village, largely seasonal",
  "Between summer and ski season much of it is shut. Assume closed in October."),
 (400, "Panguitch",                "UT", 0.0, "good", "town", "high",
  "Grocery · cafes · motels · post office",
  "First reliable resupply since Cedar City. Also a notorious cold sink — "
  "a motel here is a legitimate way to skip a 20°F night."),
 (450, "Bryce Canyon / Ruby's Inn","UT", 1.0, "moderate", "town", "med",
  "General store · restaurants · showers",
  "Big general store, tourist pricing. Open later in the season than most nearby options."),
 (510, "Cannonville / Henrieville","UT", 0.5, "minimal", "town", "low",
  "Very small store, irregular hours",
  "Two tiny settlements. Snacks and drinks at best. Plan through, not around, them."),
 (570, "Escalante",                "UT", 0.0, "good", "town", "high",
  "Grocery · outfitter · cafes · post office · lodging",
  "START OF THE BIG CARRY. Last good grocery for ~285 mi. Post office here is the "
  "smart mail-drop for the eastern half."),
 (625, "Boulder",                  "UT", 0.0, "minimal", "town", "med",
  "One small store · 1–2 restaurants",
  "Tiny and seasonal-ish. A meal and a partial top-up, not a resupply."),
 (680, "Torrey / Capitol Reef",    "UT", 9.0, "moderate", "town", "med",
  "Small grocery · restaurants · lodging",
  "~9 mi off route and worth it. Best food between Escalante and Blanding, and the "
  "last one before the Hwy 95 void."),
 (745, "Hanksville",               "UT", 0.0, "moderate", "town", "high",
  "Two small markets · gas · cafe · lodging",
  "CRITICAL. Load 3+ days here. Next food is Blanding, 110 mi east, and there is "
  "genuinely nothing in between."),
 (800, "Hite",                     "UT", 0.0, "none", "seasonal", "high",
  "CLOSED — store, fuel, ranger station, marina",
  "Services suspended since 2021, 'until further notice' (NPS). Older route notes and "
  "trip reports still list it as a stop. THEY ARE WRONG. Plan zero here."),
 (830, "Natural Bridges NM",       "UT", 0.5, "none", "seasonal", "med",
  "Visitor centre · vault toilets · no food sold",
  "Potable water at the visitor centre in season, but it can be shut off after the "
  "first hard freeze. Call ahead: (435) 692-1234."),
 (855, "Blanding",                 "UT", 14.0, "good", "town", "med",
  "Supermarket · pharmacy · motels · post office",
  "~14 mi off route. The detour is how most riders break the Hwy 95 carry. Skip it "
  "only if you left Hanksville with 4 full days."),
 (915, "Monticello",               "UT", 0.0, "good", "town", "high",
  "Grocery · cafes · motels · post office · laundry",
  "Coldest town on the route (7,070 ft). Full resupply and a warm bed both available."),
 (1020,"Moab",                     "UT", 0.0, "full", "town", "high",
  "Supermarkets · multiple bike shops · outfitters · post office",
  "Best bike shops on the entire route. Fix everything here — nothing comparable "
  "until Durango. Natural rest day and last warm night."),
 (1075,"La Sal / Paradox",         "UT/CO", 3.0, "minimal", "scarce", "low",
  "Tiny store, unreliable hours",
  "Effectively nothing. Ride Moab → Naturita self-supported."),
 (1125,"Naturita / Nucla",         "CO", 1.0, "moderate", "town", "high",
  "Small market · gas-and-deli · cafes",
  "Twin towns ~2 mi apart. Between them you can eat well and restock adequately. "
  "Last low-elevation night."),
 (1165,"Norwood",                  "CO", 0.0, "moderate", "town", "med",
  "Small grocery/cafe · restaurant",
  "Load 2 days for the San Juans. Weather here is Rocky Mountain, not desert."),
 (1185,"Telluride",                "CO", 13.0, "full", "town", "med",
  "Supermarket · bike shops · gear shops · medical",
  "~13 mi off route and a big descent you must climb back out of. Worth it only if "
  "you need a bike shop or are bailing from bad weather."),
 (1195,"Rico",                     "CO", 0.0, "minimal", "town", "med",
  "Cafe · very small store",
  "A hot meal on the cold side of Lizard Head Pass. Do not plan food around it."),
 (1210,"Durango",                  "CO", 0.0, "full", "town", "high",
  "Everything · bike shops · train · airport",
  "Eastern terminus."),
]

TIER_DAYS = {"full": 6, "good": 4, "moderate": 3, "minimal": 0.5, "none": 0}


def build_resupply():
    rows = []
    for m, name, st, off, tier, water, conf, svc, note in R:
        rows.append({
            "mile": m, "name": name, "state": st, "off": off, "tier": tier,
            "water": water, "conf": conf, "services": svc, "note": note,
            "maxDays": TIER_DAYS[tier],
            # true riding distance including the round trip off route
            "detour": round(off * 2, 1),
        })

    # Gap analysis between stops of at least "moderate" quality --------------
    # Raw distance alone is a poor ranking — a 120 mi gap ending in a supermarket
    # you ride straight past is far easier than a 110 mi gap that dead-ends in a
    # closed outpost and a 28 mi round-trip detour. Score the things that actually
    # bite: dead stops inside the gap, the detour you must ride, and dry country.
    solid = [r for r in rows if r["tier"] in ("full", "good", "moderate")]
    gaps = []
    for a, b in zip(solid, solid[1:]):
        dist = b["mile"] - a["mile"]
        inside = [r for r in rows if a["mile"] < r["mile"] < b["mile"]
                  and r["tier"] in ("minimal", "none")]
        dead = [r["name"] for r in inside if r["tier"] == "none"]
        dry = any(r["water"] in ("scarce", "seasonal") for r in inside) \
            or b["water"] in ("scarce", "seasonal")

        score = dist + 30 * bool(dead) + 2 * b["detour"] + 25 * dry
        gaps.append({
            "from": a["name"], "to": b["name"], "miles": dist,
            "days": round(dist / 55.0, 1),
            "detour": b["detour"], "dead": dead, "dry": dry,
            "skipped": [r["name"] for r in inside],
            "score": round(score),
            "severity": "critical" if score >= 150 else "watch" if score >= 100 else "ok",
        })
    return rows, gaps


# ---------------------------------------------------------------------------
# PACKING LIST
# Driven by the weather model: 88°F in the Mojave on Oct 3 down to a
# 10th-percentile 12°F on Lizard Head Pass on Oct 22. That 76°F operating range
# is the actual design problem — not the cold on its own.
# ---------------------------------------------------------------------------
PACK = [
 # category, item, spec, weight_oz, priority, why
 ("Sleep system", "Sleeping bag / quilt", "15°F rated, 800+ fill down", 30, "critical",
  "Model's coldest 10th-percentile night is 12°F at Lizard Head. A 30°F bag leaves you "
  "cold on roughly a third of the nights on this route."),
 ("Sleep system", "Sleeping pad", "Insulated, R-value 4.5+", 15, "critical",
  "Ground conduction, not air temperature, is what actually ends a night. An R-2 summer "
  "pad on frozen ground at 10,000 ft defeats any bag you pair it with."),
 ("Sleep system", "Pillow / stuff sack", "Inflatable or clothes bag", 3, "comfort",
  "3 oz for real sleep across 23 nights is one of the best trades on the list."),

 ("Shelter", "Tent — recommended", "Freestanding/semi 1P double-wall, 3-season", 40, "critical",
  "THE PICK. Slickrock and frozen ground won't hold stakes, and double-wall manages the "
  "condensation you get from big diurnal swings. Worth ~14 oz over a tarp."),
 ("Shelter", "Tarp + bivy — alternative", "Silnylon/DCF tarp + water-resistant bivy", 22, "optional",
  "Lightest real option and fine for the desert half. On the San Juan nights it is a "
  "genuine sufferfest, and it pitches badly on slickrock."),
 ("Shelter", "Mid / pyramid — alternative", "Single-wall, trekking-pole or bar pitched", 26, "optional",
  "Good compromise: near-tarp weight, real snow shedding. Needs anchors you may not find."),
 ("Shelter", "Groundsheet", "Polycryo or DCF, cut to size", 2, "recommended",
  "Slickrock and cryptobiotic-adjacent grit shred floors."),

 ("Worn / riding", "Bib shorts", "Chamois, 1 pair", 7, "critical",
  "One pair. Wash and dry them — the desert air does this in an hour."),
 ("Worn / riding", "Merino T or sun hoody", "150–190 g/m² merino or synthetic hoody", 6, "critical",
  "Sun hoody wins on the Mojave days; UV index is still 3–6 in October."),
 ("Worn / riding", "Lightweight gloves", "Full-finger, thin", 2, "recommended",
  "Dawn starts are near freezing for two-thirds of the trip."),
 ("Worn / riding", "Cycling shoes", "Stiff sole, drains and dries", 0, "critical",
  "Worn, not carried. Waterproof shoes stay wet once flooded — pick drainage."),

 ("Insulation", "Puffy jacket", "Down or synthetic, 800fp, hooded", 11, "critical",
  "Worn in camp every night from Oct 6 onward. Hooded is not optional at 10,000 ft."),
 ("Insulation", "Fleece / grid mid-layer", "100–150 weight grid fleece", 8, "critical",
  "The layer you actually climb in. Down soaks through with sweat; fleece doesn't."),
 ("Insulation", "Merino base, long sleeve", "200 g/m², sleep-clean", 7, "critical",
  "Doubles as sleepwear. Keeping it dry is what makes the 15°F bag hit its rating."),
 ("Insulation", "Thermal tights / long johns", "200 g/m² merino or fleece", 6, "critical",
  "Legs get ignored and then you're awake at 3am."),
 ("Insulation", "Insulated booties or spare socks", "Down booties, or 2 thick wool pairs", 4, "comfort",
  "Cold feet are the single most common reason people don't sleep in the cold."),
 ("Insulation", "Warm hat + buff", "Merino beanie, neck gaiter", 3, "critical",
  "2 oz that buys roughly 5°F of effective bag rating."),
 ("Insulation", "Insulated gloves", "Softshell or lobster, wind-resistant", 4, "critical",
  "Descending from Cedar Breaks or Lizard Head at 25°F is the coldest you will be."),

 ("Wind & wet", "Rain jacket", "2.5-layer, pit zips, hood", 8, "critical",
  "Precip chance peaks at only ~26%, but at 10,000 ft in late October that's snow."),
 ("Wind & wet", "Rain pants or wind pants", "Lightweight, full or 3/4 zip", 5, "recommended",
  "Wind pants cover 90% of the need at half the weight. Full rain pants if you're "
  "riding late October."),
 ("Wind & wet", "Waterproof socks", "Knee or ankle length", 3, "comfort",
  "Cheaper and lighter than solving wet feet any other way."),

 ("Water", "Capacity", "6 L total — 3 bottles + 3 L bladder/dromedary", 8, "critical",
  "Longest documented dry stretch is ~60 mi. Six litres covers that plus a dry camp "
  "with a margin for a stock tank being empty."),
 ("Water", "Filter", "Squeeze or inline hollow-fibre", 4, "critical",
  "SLEEP WITH IT from Oct 6 onward. One freeze cracks the fibres invisibly and it "
  "then passes everything."),
 ("Water", "Chemical backup", "Tablets or drops", 1, "critical",
  "Weighs nothing and covers a failed or frozen filter."),
 ("Water", "Sediment pre-filter", "Bandana or coffee filter", 1, "recommended",
  "Desert stock tanks and silty potholes will clog a filter in a day without one."),

 ("Cooking", "Stove — recommended", "Upright canister, ~3 oz", 3, "recommended",
  "THE PICK. Simple, fast, and October nights aren't cold enough to cripple isopropane "
  "if you sleep with the canister. Fuel is stocked in Moab, Escalante, Blanding."),
 ("Cooking", "Stove — alternative", "Alcohol or cold-soak", 1, "optional",
  "Lightest. But alcohol is slow and inefficient in cold and wind, and a hot dinner "
  "does real work for morale at 25°F."),
 ("Cooking", "Fuel", "1 × 230 g canister, swap at Moab", 14, "recommended",
  "Cold burns fuel faster. Buy the big one; small ones are unreliably stocked."),
 ("Cooking", "Pot + spork", "750 ml titanium, lid", 5, "recommended",
  "750 ml so you can rehydrate and drink from the same vessel."),
 ("Cooking", "Insulated mug", "500 ml, lidded", 4, "comfort",
  "Underrated. A hot drink before you leave the bag at 20°F changes the whole morning."),

 ("Food carry", "Bag capacity", "Room for 4 full days", 0, "critical",
  "Sized by the Hanksville → Blanding carry: 110 mi with Hite closed. Most riders are "
  "short here, not on water."),
 ("Food carry", "Odour-proof / critter bag", "Roll-top dry bag", 2, "recommended",
  "Ringtails and mice at established desert camps, not bears, are the problem."),

 ("Electronics", "Front light", "300+ lumen, USB", 5, "critical",
  "Daylight drops from 11h50m to 10h50m across the trip, and the hardest days are last."),
 ("Electronics", "Rear light + headlamp", "Blinky + 200 lm headlamp", 4, "critical",
  "Highway 95 and Hwy 145 have real traffic and no shoulder."),
 ("Electronics", "Power bank", "10,000 mAh", 7, "critical",
  "Cold roughly halves usable battery. 5–6 days between reliable outlets on the "
  "Escalante → Blanding stretch."),
 ("Electronics", "GPS / phone + offline maps", "Downloaded before you leave town", 0, "critical",
  "No cell service for hours at a time on Hwy 95."),
 ("Electronics", "Satellite messenger", "Two-way with SOS", 4, "critical",
  "Not optional here. Long unpaved stretches, no traffic, no signal, freezing nights."),

 ("Repair", "Tubes + plugs + patches", "2 tubes, tubeless plugs, patch kit", 10, "critical",
  "Goatheads west of St. George, slickrock cuts east of it."),
 ("Repair", "Pump + tyre boot", "Frame pump, boot or dollar bill", 7, "critical", ""),
 ("Repair", "Multi-tool + chain tool", "With quick links", 6, "critical", ""),
 ("Repair", "Spare derailleur hanger", "Bike-specific", 1, "critical",
  "The one part no shop between Moab and Durango will have for your frame."),
 ("Repair", "Chain lube", "Dry/wax for dust", 2, "recommended",
  "Colorado Plateau dust destroys wet lube in a day."),
 ("Repair", "Spare brake pads", "One set", 2, "recommended",
  "123,000 ft of climbing means 123,000 ft of descending."),
 ("Repair", "Zip ties, tape, voile strap", "Assorted", 3, "recommended", ""),

 ("Health", "First aid kit", "Trimmed personal kit", 6, "critical", ""),
 ("Health", "Sunscreen + SPF lip balm", "High SPF, small", 3, "critical",
  "Snow and slickrock both reflect. UV stays meaningful all month."),
 ("Health", "Chamois cream", "Small tube", 3, "recommended",
  "23 consecutive days. Do not economise here."),
 ("Health", "Electrolytes", "Tabs or powder", 3, "recommended",
  "Dry cold hides dehydration as effectively as heat does."),
 ("Health", "Toothbrush / meds / ID / cash", "Personal", 5, "critical",
  "Carry cash — small-town card readers go down and some places are cash-only."),
]


# ---------------------------------------------------------------------------
# SEASONAL ACCESS
# Two different kinds of thing, deliberately kept in one list because a rider
# only cares whether the road goes:
#   "current" — a dated, year-specific event (fire closure, hunt season)
#   "annual"  — a recurring seasonal window
# kind: closed | marginal | open  = expected status during an OCTOBER ride
# ---------------------------------------------------------------------------
SEASON = [
 # mile_from, mile_to, name, type, oct_status, window, detail, source_label, url
 (800, 970, "Babylon Fire burn scar — Bears Ears / Elk Ridge / Needles",
  "current", "verify",
  "Closure order ran 28 Jun – 31 Aug 2026",
  "Utah's first megafire in eight years: 107,189 acres, 95% contained in early August 2026. "
  "The closure covered the entire Monticello Ranger District, Dark Canyon Wilderness, Bears "
  "Ears NM, and all BLM/FS land south of Hwy 211, west of Hwy 191 and north of Hwy 95 — which "
  "is precisely the Natural Bridges → Elk Ridge → Monticello section. Canyonlands' Needles "
  "District closed too. THE ORDER WAS WRITTEN TO EXPIRE 31 AUG, BUT BURN-AREA CLOSURES ARE "
  "ROUTINELY EXTENDED for hazard trees and road damage, and reopening is not the same as "
  "safe: fresh burn scars produce debris flows and flash floods in rain far beyond the "
  "burn itself, springs and stock tanks run with ash, and shade disappears. If you are "
  "riding this in 2026 or 2027, this is the first phone call you make, not the last.",
  "Manti-La Sal NF closure order",
  "https://www.fs.usda.gov/r04/manti-lasal/alerts/babylon-wildfire-closure-order"),

 (855, 1210, "Utah general deer rifle hunt",
  "current", "open",
  "17–25 Oct 2026 (early units 7–11 Oct)",
  "The nine-day general any-legal-weapon season lands squarely on the Monticello → Moab → "
  "La Sal stretch of a 1 Oct departure. Public land stays open and you are not obliged to do "
  "anything, but dispersed camping gets crowded and noisy, forest roads carry far more "
  "traffic, and blaze orange stops being optional. Colorado's seasons open in October too. "
  "Easiest fix is to be through the Abajos and La Sals before the 17th, or to sleep in towns "
  "through that window.",
  "Utah DWR season dates",
  "https://www.eregulations.com/utah/hunting/hunting-seasons-and-dates"),

 (340, 360, "Cedar Breaks NM — SR-148 rim road",
  "annual", "marginal",
  "Typically closed mid-Nov → late May",
  "The rim road is gated for winter once snowpack is sufficient — usually mid-November, so an "
  "early-October crossing is normally fine. But 'sufficient snowpack' is a judgement call, not "
  "a date, and this is 10,300 ft. An early storm can shut it with no notice. SR-143, the "
  "north/east approach, is plowed in daylight hours and is your fallback.",
  "NPS Cedar Breaks winter access",
  "https://www.nps.gov/cebr/planyourvisit/winter-access.htm"),

 (800, 855, "Elk Ridge Road (FR-088)",
  "annual", "marginal",
  "Generally passable Apr → Nov; best Jun → Oct",
  "Single-lane dirt along a 9,000 ft spine. It is at the very end of its usable window in late "
  "October and the first real snow ends it — there is no plowing and no gate schedule to rely "
  "on. Combined with the Babylon burn scar, this is the least certain link on the whole route. "
  "Have the Hwy 95 pavement bail-out mapped before you commit. Monticello Ranger District: "
  "(435) 636-3340.",
  "Manti-La Sal NF — Elk Ridge",
  "https://www.fs.usda.gov/r04/manti-lasal/recreation/elk-ridge-recreation-area"),

 (1020, 1075, "La Sal Mountains — Geyser Pass Road",
  "annual", "open",
  "Closed 15 Dec → 15 May",
  "Open through October. The Loop Road is plowed to the Geyser Pass turn-off in winter and "
  "less often to Castle Valley. Not a seasonal risk for an October ride, but at 9,600 ft it "
  "holds early snow, and multi-year construction on the Loop Road has produced intermittent "
  "daytime closures — worth a check.",
  "Manti-La Sal NF — Geyser Pass",
  "https://www.fs.usda.gov/r04/manti-lasal/recreation/geyser-pass-trailhead"),

 (215, 250, "Zion — Kolob Terrace Road / Lava Point",
  "annual", "open",
  "Snow closure possible Nov → May",
  "Only the lower ~14 miles are plowed; above that it closes with snow, usually from November. "
  "Lava Point Campground runs May through September or October depending on snow. Fine in early "
  "October in a normal year, but it is the first thing to shut in a cold one.",
  "NPS Zion conditions",
  "https://www.nps.gov/zion/planyourvisit/conditions.htm"),

 (625, 700, "Boulder Mountain — Hwy 12 and the dirt alternates",
  "annual", "open",
  "Hwy 12 plowed year-round",
  "The paved 9,600 ft crossing stays open all year, though it ices and can be briefly "
  "impassable after a storm. The unpaved alternates on the Aquarius Plateau — North Slope, "
  "Deer Creek, Pleasant Creek — are a different matter and gate or become impassable with the "
  "first real snow. Ride the pass in the middle of the day, not at dawn.",
  "Scenic Byway 12",
  "https://www.visitutah.com/articles/the-all-american-road-scenic-byway-12"),

 (340, 345, "Brian Head village",
  "annual", "closed",
  "Largely shut between summer and ski seasons",
  "October falls in the shoulder gap: most of the village is closed, and it reliably fails as "
  "a resupply. Already tiered 'minimal' in the resupply table — this is why.",
  "Visit Cedar City / Brian Head",
  "https://visitcedarcity.com/"),

 (830, 835, "Natural Bridges NM — potable water",
  "annual", "marginal",
  "Shut off after the first hard freeze",
  "The visitor-centre spigot is the only water in a long dry stretch, and it is turned off once "
  "freezing becomes routine — which the weather model puts at roughly 29% probability on the "
  "night you would arrive, rising fast after. Call before you rely on it: (435) 692-1234.",
  "NPS Natural Bridges",
  "https://www.nps.gov/nabr/planyourvisit/conditions.htm"),

 (1165, 1210, "Lizard Head Pass — Hwy 145",
  "annual", "open",
  "Plowed and open year-round",
  "The pavement over the pass is maintained all winter, so it is not a seasonal closure — but "
  "it is 10,222 ft on ~22 October with the highest freeze and precipitation odds on the route. "
  "It closes during storms, not for the season. CDOT COtrip is the live source.",
  "CDOT road conditions",
  "https://www.cotrip.org/"),

 (450, 600, "Grand Staircase clay roads",
  "annual", "marginal",
  "Not seasonal — condition-dependent year-round",
  "Included because riders keep reading 'open' as 'passable'. The bentonite clay through the "
  "Grand Staircase and again around Paradox turns to unrideable, unpushable glue within minutes "
  "of rain and stays that way for a day or more after. No gate will warn you. Precipitation "
  "odds here run 13–19% per day in October.",
  "BLM Grand Staircase-Escalante",
  "https://www.blm.gov/programs/national-conservation-lands/utah/grand-staircase-escalante"),
]


def build_season():
    order = {"verify": 0, "closed": 1, "marginal": 2, "open": 3}
    assert all(len(r) == 9 for r in SEASON), "SEASON rows must all have 9 fields"
    rows = [{
        "from": a, "to": b, "name": n, "type": t, "status": s,
        "window": w, "detail": d, "src": sl, "url": u,
    } for a, b, n, t, s, w, d, sl, u in SEASON]
    rows.sort(key=lambda r: (r["type"] != "current", order[r["status"]], r["from"]))
    return rows


def build_packing():
    out = {}
    for cat, item, spec, oz, pri, why in PACK:
        out.setdefault(cat, []).append(
            {"item": item, "spec": spec, "oz": oz, "pri": pri, "why": why})
    return out


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    rows, gaps = build_resupply()
    packing = build_packing()
    season = build_season()

    (here / "resupply.json").write_text(json.dumps({"stops": rows, "gaps": gaps}, indent=1))
    (here / "packing.json").write_text(json.dumps(packing, indent=1))
    (here / "seasonal.json").write_text(json.dumps(season, indent=1))

    print(f"{'Mi':>5}  {'Stop':<26}{'Off':>6}  {'Tier':<9}{'Days':>5}")
    print("-" * 60)
    for r in rows:
        off = f"{r['off']:.1f}" if r["off"] else "—"
        print(f"{r['mile']:>5}  {r['name']:<26}{off:>6}  {r['tier']:<9}{r['maxDays']:>5}")

    print("\nCARRY GAPS (between moderate-or-better stops)")
    print("-" * 60)
    for g in sorted(gaps, key=lambda g: -g["score"])[:8]:
        flag = {"critical": "!!", "watch": " !", "ok": "  "}[g["severity"]]
        sk = f"  skips: {', '.join(g['skipped'])}" if g["skipped"] else ""
        print(f"{flag} {g['from']:<21}→ {g['to']:<21}{g['miles']:>4} mi "
              f"{g['days']:>4}d  score {g['score']:>3}{sk}")

    # --- checks ---
    assert rows == sorted(rows, key=lambda r: r["mile"]), "stops out of order"
    tot = sum(i["oz"] for c in packing.values() for i in c
              if i["pri"] in ("critical", "recommended"))
    crit = sum(i["oz"] for c in packing.values() for i in c if i["pri"] == "critical")
    print(f"\nBase weight, critical only:          {crit/16:.1f} lb")
    print(f"Base weight, critical + recommended: {tot/16:.1f} lb")
    print("  (excludes worn items, food, water, and the bags themselves)")
    print("\nSEASONAL ACCESS (October status)")
    print("-" * 60)
    mark = {"verify": "??", "closed": "XX", "marginal": " ~", "open": " ."}
    for s in season:
        tag = "2026" if s["type"] == "current" else "    "
        print(f"{mark[s['status']]} {tag} mi {s['from']:>4}-{s['to']:<5}"
              f"{s['name'][:42]:<44}{s['window']}")

    assert all(s["url"].startswith("http") for s in season), "every entry needs a source"
    print(f"\n{len(rows)} stops, {len(gaps)} gaps, "
          f"{sum(len(v) for v in packing.values())} packing items, "
          f"{len(season)} access notes "
          f"({sum(1 for s in season if s['type']=='current')} year-specific)")

"""
Plateau Passage — October weather model, west to east.
Builds a day-by-day dataset from station climate normals + elevation lapse-rate
corrections + within-month seasonal drift.
"""
import json, math

# ---------------------------------------------------------------------------
# Base data: October climate normals at (or lapse-adjusted to) the elevation
# actually ridden/camped that day. Highs/lows are mid-October baselines.
#   camp_ft  = typical overnight elevation (drives the LOW temp)
#   high_ft  = highest point ridden that day (drives the "on the pass" numbers)
#   hi / lo  = mid-Oct normal high/low at camp elevation, degF
#   pday     = climatological chance of measurable precip on a given day (%)
# ---------------------------------------------------------------------------
DAYS = [
 # day, date,   landmark,                                 camp_ft, high_ft, hi, lo, pday, terrain,        note
 (1,  "Oct 1",  "Las Vegas, NV — depart",                   2000,  3200, 81, 61, 7,  "Mojave Desert",
  "Hot start. Ride early; 2+ gal water capacity out of town."),
 (2,  "Oct 2",  "Spring Mtns / Lovell Canyon, NV",          6000,  7500, 65, 40, 10, "Sky-island pinyon",
  "First 4,000 ft climb. 20°F colder than the Strip in one day."),
 (3,  "Oct 3",  "Mesquite / Beaver Dam Wash, NV–AZ",        1800,  4200, 82, 54, 8,  "Mojave Desert",
  "Lowest point of the route. Hottest day you'll have."),
 (4,  "Oct 4",  "St. George, UT",                           2760,  3600, 79, 52, 10, "Red-rock desert",
  "Resupply. Last reliably warm night for two weeks."),
 (5,  "Oct 5",  "Zion NP / Gooseberry Mesa",                3900,  5200, 78, 49, 13, "Slickrock mesa",
  "Slickrock. Nights start dipping into the 40s."),
 (6,  "Oct 6",  "Cedar City, UT",                           5850,  6200, 66, 34, 13, "Great Basin edge",
  "TRANSITION DAY. First frost-capable night. Resupply cold gear here."),
 (7,  "Oct 7",  "Cedar Breaks NM / Brian Head",            10300, 10600, 46, 24, 20, "Alpine / subalpine",
  "COLD SPIKE #1. Above 10,000 ft. Snow is entirely possible."),
 (8,  "Oct 8",  "Panguitch / Red Canyon, UT",               6600,  8000, 64, 26, 13, "High valley",
  "Panguitch is a cold-air sink — colder at night than the pass above it."),
 (9,  "Oct 9",  "Bryce Canyon NP",                          7900,  8300, 61, 27, 16, "High plateau",
  "Hard freeze most nights. Warm days, brutal mornings."),
 (10, "Oct 10", "Henrieville / Grand Staircase",            5900,  7200, 68, 33, 13, "Desert canyon",
  "Big diurnal swing — 35°F spread. Clay roads impassable when wet."),
 (11, "Oct 11", "Escalante, UT",                            5820,  7000, 68, 35, 13, "Desert canyon",
  "Resupply. Hole-in-the-Rock country."),
 (12, "Oct 12", "Boulder, UT",                              6700,  7400, 66, 37, 13, "Plateau foothills",
  "Last services before Boulder Mountain."),
 (13, "Oct 13", "Boulder Mtn → Capitol Reef NP",            5500,  9600, 71, 40, 13, "Alpine → desert",
  "9,600 ft pass then 4,000 ft descent. Ride the pass midday, not dawn."),
 (14, "Oct 14", "Hanksville / Hite — Lost Canyon Point",    4200,  6000, 72, 39, 10, "Slickrock desert",
  "Driest, most remote water carry of the route. Warm reprieve."),
 (15, "Oct 15", "Natural Bridges NM / Elk Ridge",           6500,  8500, 65, 36, 16, "Ponderosa mesa",
  "Bears Ears high country. Elk Ridge tops 8,500 ft."),
 (16, "Oct 16", "Monticello, UT (Abajo Mtns)",              7070,  8200, 62, 35, 16, "Mountain town",
  "Coldest town on the route until Colorado. Full resupply."),
 (17, "Oct 17", "Canyonlands rim / Lockhart Basin",         5000,  6200, 71, 42, 13, "Canyon country",
  "Descent back into warm desert. Enjoy it."),
 (18, "Oct 18", "Moab, UT",                                 4000,  5000, 73, 44, 13, "Red-rock desert",
  "Warmest nights since St. George. Best place for a rest day."),
 (19, "Oct 19", "La Sal Mtns / Paradox Valley",             7000,  8800, 63, 33, 16, "Montane forest",
  "Climb out of Moab into aspen. Nights turn hard again."),
 (20, "Oct 20", "Nucla / Naturita, CO",                     5400,  7000, 68, 37, 13, "High desert",
  "Last low-elevation night of the trip. Stage for the San Juans."),
 (21, "Oct 21", "Norwood, CO",                              7000,  7600, 62, 30, 16, "Wheat mesa",
  "Wind-exposed mesa. Weather now driven by Rockies, not desert."),
 (22, "Oct 22", "Telluride / Lizard Head Pass",             8750, 10222, 57, 25, 20, "Subalpine",
  "COLD SPIKE #2 — the trip's crux. Late Oct at 10,000+ ft."),
 (23, "Oct 23", "Rico → Durango, CO — finish",              6512,  9000, 66, 30, 16, "Montane → valley",
  "Long descent to the Animas. Durango is a notorious cold sink at dawn."),
]

# --- Model parameters -------------------------------------------------------
DRIFT_PER_DAY = 0.5     # degF/day cooling through October (Intermountain West)
MID_OCT = 16            # normals are centered on mid-month
LAPSE_HI = 3.5          # degF per 1000 ft, daytime
LAPSE_LO = 3.0          # degF per 1000 ft, overnight (damped by cold-air drainage)
SIGMA_LOW = 8.0         # stdev of daily min temp about the normal, degF
COLD_SNAP_Z = 1.28      # 10th percentile => design-cold planning number


def phi(z):
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


rows = []
for day, date, name, camp_ft, high_ft, hi, lo, pday, terrain, note in DAYS:
    drift = (MID_OCT - day) * DRIFT_PER_DAY          # + early in month, - late

    hi_adj = hi + drift
    lo_adj = lo + drift

    # Temperature at the day's high point (lapse-adjusted from camp elevation)
    d_kft = (high_ft - camp_ft) / 1000.0
    hi_pass = hi_adj - LAPSE_HI * d_kft
    lo_pass = lo_adj - LAPSE_LO * d_kft

    # Freeze probability overnight at camp
    p_freeze = phi((32.0 - lo_adj) / SIGMA_LOW) * 100.0

    # Design-cold night (~10th percentile) — what your sleep system must handle
    cold_snap = lo_adj - COLD_SNAP_Z * SIGMA_LOW

    # Precip chance nudged up with elevation and later dates
    p_precip = pday + max(0, (camp_ft - 5000) / 1000.0) * 1.2 - drift * 0.15

    rows.append({
        "day": day, "date": date, "mile": (day - 1) * 60, "name": name,
        "campFt": camp_ft, "highFt": high_ft, "terrain": terrain, "note": note,
        "hi": round(hi_adj), "lo": round(lo_adj),
        "hiPass": round(hi_pass), "loPass": round(lo_pass),
        "swing": round(hi_adj - lo_adj),
        "freeze": round(p_freeze), "precip": round(max(4, p_precip)),
        "coldSnap": round(cold_snap),
    })

with open("route_weather.json", "w") as f:
    json.dump(rows, f, indent=1)

# --- Sanity checks ----------------------------------------------------------
print(f"{'Day':<7}{'Landmark':<38}{'Camp':>7}{'Hi':>5}{'Lo':>5}{'Pass':>7}"
      f"{'Frz%':>6}{'Pcp%':>6}{'Cold':>6}")
print("-" * 87)
for r in rows:
    print(f"{r['date']:<7}{r['name'][:36]:<38}{r['campFt']:>7,}{r['hi']:>5}{r['lo']:>5}"
          f"{r['hiPass']:>4}/{r['loPass']:<2}{r['freeze']:>6}{r['precip']:>6}{r['coldSnap']:>6}")

print()
print("Coldest night at camp: ", min(rows, key=lambda r: r["lo"])["name"],
      min(r["lo"] for r in rows), "F")
print("Hottest day:           ", max(rows, key=lambda r: r["hi"])["name"],
      max(r["hi"] for r in rows), "F")
print("Biggest diurnal swing: ", max(rows, key=lambda r: r["swing"])["name"],
      max(r["swing"] for r in rows), "F")
print("Nights >50% freeze:    ", sum(1 for r in rows if r["freeze"] > 50), "of", len(rows))
print("Nights >80% freeze:    ", sum(1 for r in rows if r["freeze"] > 80))
print("Coldest design night:  ", min(r["coldSnap"] for r in rows), "F")
print("Total elevation range: ", min(r['campFt'] for r in rows), "-",
      max(r['highFt'] for r in rows), "ft")

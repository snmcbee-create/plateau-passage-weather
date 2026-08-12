# Plateau Passage — October Weather Profile

An interactive, offline-capable weather profile for the [Plateau Passage](https://bikepackingroots.org/project/the-plateau-passage/)
bikepacking route — 1,200 miles and ~123,000 ft of climbing from Las Vegas, NV to Durango, CO.

**→ [View the chart](https://snmcbee-create.github.io/plateau-passage-weather/)**

> ### ⚠ 2026 — Babylon Fire
> **107,189 acres burned across Bears Ears, Dark Canyon and the Monticello Ranger District
> in summer 2026** — Utah's first megafire in eight years, 95% contained in early August.
> The closure order covered the entire **Natural Bridges → Elk Ridge → Monticello** section
> of this route plus Canyonlands' Needles District, and was written to expire 31 Aug 2026.
> **Burn-area closures are routinely extended, and reopening is not the same as safe.**
> Confirm with the
> [Manti-La Sal National Forest](https://www.fs.usda.gov/r04/manti-lasal/alerts/babylon-wildfire-closure-order)
> before planning around this section.

Most route guides give you a single "October is nice" line. This models what you'll
actually meet, day by day, at the elevation you'll actually be sleeping at.

## What it shows

**Weather** — for each of 23 days from an Oct 1 Las Vegas start:

- Average high and low at **camp elevation**, and separately at the **day's high point**
- **Overnight freeze probability** — P(low ≤ 32°F)
- **Cold-snap low** — the 10th-percentile night, i.e. what your sleep system has to survive
- Chance of measurable precipitation, and elevation overlaid on the temperature curve

**Resupply & food** — 25 stops west to east, each tagged with what you can realistically
buy (not what a map pin claims exists), how far off route it sits, and how many days of
food it can actually support. Carry gaps are scored on what bites — dead stops inside the
gap, the detour you must ride, and dry country — rather than raw distance.

**Seasonal access** — 11 notes on parts of the route that aren't open all year, or aren't
open every year. Two year-specific entries (the Babylon Fire closure, and Utah's deer rifle
hunt on **17–25 Oct 2026**, which lands on the Monticello → Moab → La Sal stretch) alongside
nine recurring seasonal windows. Every entry links to the managing agency.

**Water** — 29 sources with an explicit confidence rating on every one, dry-stretch analysis,
and a worst-case toggle. See [How confident is this?](#how-confident-is-this) — the short
answer is *not very*, and the page says so loudly.

**Packing list** — 49 items specced against the weather model, with weights and a
critical / recommended / comfort split. Shelter and stove options are laid out against the
actual conditions with a recommendation, rather than assumed.

## The headline finding

October on this route is **not a gradient — it's a sawtooth.** You cross two cold
spikes at nearly identical elevation:

| | Date | Elevation | Avg low | Freeze risk |
|---|---|---|---|---|
| Cedar Breaks NM | ~Oct 7 | 10,300 ft | 28°F | 67% |
| Lizard Head Pass | ~Oct 22 | 10,222 ft | 22°F | 89% |

Same height, three weeks apart, and the second is far more serious — this region cools
about 0.5°F per day through October. Between the spikes you drop back into 70°F desert
three separate times, which is exactly the pattern that gets people under-packed.

### And on food: Hite is closed

**All services at Hite have been suspended since 2021, "until further notice"** — store,
fuel, ranger station, marina ([NPS](https://www.nps.gov/glca/planyourvisit/hite.htm)).
Plenty of older route notes and trip reports still list it as a resupply. They are wrong.

That turns **Hanksville → Blanding into 110 miles with nothing** — Natural Bridges sells no
food either — and it's the single carry that should size your food bags. Not the longest gap
on the route, but comfortably the most consequential once you score for dead stops, the
14-mile-each-way Blanding detour, and scarce water.

### And nobody mentions this: rural Utah closes on Sunday

**Every major grocery on the Utah half of this route is closed Sundays** — Panguitch,
Escalante (both stores), Blanding and Monticello. It's an LDS-community norm and it appears
in no route guide I could find. In Colorado the pattern inverts: Wild Gal's in Naturita
closes **Mondays** and doesn't open until 10am otherwise.

The site computes this against your actual start date. On an Oct 1 2026 departure it bites
once, and badly: **Oct 11 is a Sunday and lands on Escalante** — the last good grocery for
285 miles, with both stores shut and no alternative in town. Shifting the start by one day
moves it.

Two other things fall out of the weather data:

- **Oct 6 at Cedar City is the hinge.** In one day's ride you go from freezing being
  essentially impossible to being the default. Natural place to swap or mail cold gear.
- **60 mi/day breaks down at the end.** The highest, hardest days land when daylight is
  shortest. Plan 35–45 mi/day for the San Juans, and expect the trip to run past three weeks.

## Method

Town and park values are October climate normals from long-term NOAA/COOP stations:
Las Vegas, St. George, Zion NP, Cedar City, Panguitch, Bryce Canyon NP HQ, Escalante,
Boulder, Capitol Reef–Fruita, Hanksville, Natural Bridges NM, Blanding, Monticello, Moab,
Naturita, Norwood, Telluride, Durango.

Off-station points — Lovell Canyon, Cedar Breaks, Boulder Mountain, Elk Ridge, Lizard Head
Pass — are lapse-rate adjusted from the nearest station at **3.5°F/1,000 ft** daytime and
**3.0°F/1,000 ft** overnight (damped to account for cold-air drainage, which is why valley
floors like Panguitch and Durango run colder at night than the passes above them).

Monthly normals are centered on Oct 16, so each day is shifted by **0.5°F/day** of seasonal
cooling. Freeze probability is P(min ≤ 32°F) assuming daily minima are normally distributed
about the adjusted normal with **σ = 8°F**; the cold-snap column is the 10th percentile of
that same distribution.

A note on sources: the popular consumer weather sites (weather-atlas, climate-data.org and
similar) are reanalysis-grid products that compress the diurnal range — spot-checking them
against station data showed them running ~7°F low on highs and several degrees warm on lows.
Since overnight lows are the number that matters for this use, this model uses station
normals throughout.

### Resupply data — read this before trusting the mileages

**Resupply mileages are derived, not surveyed.** They come from the 23-day itinerary plus
known town locations, so treat them as **±10 miles** and cross-check against the official
[Bikepacking Roots route guide](https://bikepackingroots.org/project/the-plateau-passage/)
before you rely on them. Rows marked `est.` in the table are the softest.

Service tiers describe what you can realistically *buy* — a "moderate" stop is calories
without choice, and a "minimal" stop is a snack you should assume isn't there. Small-town
hours change constantly and seasonally. **Call ahead, and never let one store be your only
plan.**

### Seasonal access — this section goes stale fastest

The two year-specific entries are **dated snapshots**, not live data. The page shows the
month it was built for exactly this reason. Fire closures get extended, hunt dates move
annually, and forest gates close on judgement rather than a calendar.

The three that most often decide whether the route goes in October:

| | Window | October status |
|---|---|---|
| **Elk Ridge Rd (FR-088)** | Passable Apr–Nov, best Jun–Oct | End of window. First snow ends it, no plowing. Least certain link on the route. |
| **Cedar Breaks SR-148** | Closed mid-Nov → late May | Normally fine early Oct, but "sufficient snowpack" is a judgement, not a date. |
| **Natural Bridges water** | Off after first hard freeze | The only water in a long dry stretch. Call (435) 692-1234. |

**Check the agency, not this page.** Every entry links to the relevant Forest Service, NPS,
BLM or DOT source.

## How confident is this?

Every data point on the site carries one of these, and it's shown in the UI:

| | Meaning |
|---|---|
| **Verified** | Multiple independent sources agree, or confirmed by the managing agency |
| **Listed, unverified** | A single online listing. Plausible, not confirmed. |
| **Rider reported** | Submitted by someone who was physically there |
| **Inferred** | My reasoning from context — a hypothesis, not a fact |
| **Unknown** | Listed so you know it exists. Nothing more. |

### Water: not confident, and that matters most

Town taps and agency spigots are solid. **Everything else is inference, not observation.**
Nobody involved in building this has ridden the route, the official GPX was not obtainable,
and the sources that matter most — Poison Spring, Hog Springs, the Elk Ridge tanks — are
exactly the ones that can't be verified remotely. Bikepacking Roots' own guidance is *"do
not plan on every stock tank having water."*

**Treat every amber and red entry as absent until someone who was there says otherwise.**

One specific trap the site models explicitly: Natural Bridges' visitor-centre tap is the only
dependable water between Hanksville and Blanding, **and it's shut off after the first hard
freeze** (~29% on the night you'd arrive, rising through late October). With it working the
stretch looks routine. With it off it's 110 miles between reliable taps, two unverified
sources en route, in the most remote country on the route, inside a fresh burn scar. The
water chart has a toggle for exactly this.

### Business hours are the weakest data here

Names, addresses and phone numbers cross-check well. **Hours do not.** They come from online
aggregators, drift seasonally, and one listing pulled during research was internally
inconsistent. Every entry is stamped with the month it was checked and carries a phone
number for precisely that reason. Call, don't trust.

## Contributing — especially water reports

This is the part that actually fixes the confidence problem, and it needs riders and locals.

**[Report a water source →](../../issues/new?template=water-report.yml)** ·
**[Correct a business →](../../issues/new?template=business-update.yml)**

Negative reports are as valuable as positive ones and much rarer. "The tank was dry" is a
genuinely useful contribution.

**For maintainers** — reports flow in through the issue forms, then:

1. Sanity-check the issue. Does the mile match an existing point? Does the date make sense?
2. Append to the `reports` array in `reports.json`:
   ```json
   {"kind":"water", "mile":845, "date":"2026-10-15", "status":"none",
    "text":"Both tanks bone dry, ash in the basin.", "by":"@handle"}
   ```
3. Run `python3 merge_reports.py`. It validates strictly — wrong mile, bad date format or
   an invalid status is rejected with a specific reason and **nothing is rebuilt**.
4. Commit, push, close the issue with a link.

Reports **outrank** the built-in defaults. A reported point displays the reporter's status,
is retagged "Rider reported", and shows their note and date inline. Newest wins for status;
all reports are retained and displayed so readers can judge freshness themselves.

### Known limits

- Daily positions assume ~55 mi/day from an Oct 1 start, averaged over 23 days with slower
  mountain days. Shift the dates and the whole curve shifts, because late October cools fast.
- **Wind is not modeled.** On the Norwood and Grand Staircase mesas it is often the thing
  that decides your day.
- Off-station high points are estimates, not measurements. Treat them as ±5°F.
- Packing weights are typical retail weights, not best-in-class, and exclude worn items,
  bags, food and water.
- Normals run through 2020 and describe a typical October. No single October is typical.

## Not a forecast

These are climatological averages. One Great Basin cold front can put 12–18 inches on the
high plateaus and drop temperatures 30°F below anything on this chart — Cedar Breaks and
Lizard Head both close in some years before Halloween. Use this to choose a sleep system, a
resupply plan, and your bail-out points. Then check [NWS point forecasts](https://www.weather.gov)
within 72 hours of every high crossing.

## Fork it for your own trip

The model is the useful part, not the chart. To re-run it for different dates, a different
pace, or a different route, edit the `DAYS` table at the top of `build_data.py` — each row is
`(day, date, landmark, camp_ft, high_ft, oct_high, oct_low, precip_pct, terrain, note)` — then:

```bash
npm install chart.js@4.4.1
cp node_modules/chart.js/dist/chart.umd.js vendor/

python3 build_data.py    # weather model      → route_weather.json
python3 build_guide.py   # resupply + packing  → resupply.json, packing.json, seasonal.json
python3 build_supply.py  # businesses + water  → businesses.json, water.json
python3 build_site.py    # inlines everything + Chart.js → index.html
```

Model parameters (lapse rates, seasonal drift, σ) are named constants near the top of
`build_data.py`. Resupply stops live in the `R` table and packing items in the `PACK` table
in `build_guide.py`. Change `REPO` and `VERSION` in `build_site.py` to point at your own fork.

`build_data.py` and `build_guide.py` both print sanity-check tables and assert on ordering
and totals — read that output rather than trusting the page.

`index.html` has **zero external requests** — Chart.js is bundled — so readers can save it
with ⌘S and it still works in a canyon with no signal. That is deliberate; please keep it
that way if you fork.

## Files

| File | What it is |
|---|---|
| `index.html` | The built, self-contained page. This is what GitHub Pages serves. |
| `build_data.py` | The weather model. Edit this to change the route or dates. |
| `build_guide.py` | Resupply stops, gap scoring, seasonal access, and the packing list. |
| `build_supply.py` | Business directory and water sources, with confidence on every field. |
| `merge_reports.py` | Validates community reports and rebuilds. Run after editing `reports.json`. |
| `build_site.py` | Inlines all data + Chart.js into `index.html`. |
| `template.html` | Page markup and styling, with `__PLACEHOLDER__` tokens. |
| `route_weather.json` | Weather model output, if you just want the numbers. |
| `resupply.json` | Stops and scored carry gaps. |
| `seasonal.json` | Access windows and closures, each with a source URL. |
| `businesses.json` | Business directory output. |
| `water.json` | Water points, dry stretches, and closed-day analysis. |
| `reports.json` | **Community reports.** Edit this to add rider/local corrections. |
| `.github/ISSUE_TEMPLATE/` | Structured report forms for water and business updates. |
| `packing.json` | Packing list by category. |
| `vendor/chart.umd.js` | Chart.js 4.4.1, bundled for offline use (MIT). |

## Corrections

Please open an issue — especially if you've actually ridden this in October. Reports of what
the weather really did are more valuable than any refinement to the model.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Fork it, re-run it, publish it —
just credit back. Route created and stewarded by [Bikepacking Roots](https://bikepackingroots.org/project/the-plateau-passage/).
Chart.js is MIT, see `vendor/chart.js-LICENSE.md`.

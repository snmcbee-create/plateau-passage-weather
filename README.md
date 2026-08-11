# Plateau Passage — October Weather Profile

An interactive, offline-capable weather profile for the [Plateau Passage](https://bikepackingroots.org/project/the-plateau-passage/)
bikepacking route — 1,200 miles and ~123,000 ft of climbing from Las Vegas, NV to Durango, CO.

**→ [View the chart](https://YOUR-USERNAME.github.io/plateau-passage-weather/)**

Most route guides give you a single "October is nice" line. This models what you'll
actually meet, day by day, at the elevation you'll actually be sleeping at.

## What it shows

For each of 23 days from an Oct 1 Las Vegas start at 60 mi/day:

- Average high and low at **camp elevation**, and separately at the **day's high point**
- **Overnight freeze probability** — P(low ≤ 32°F)
- **Cold-snap low** — the 10th-percentile night, i.e. what your sleep system has to survive
- Chance of measurable precipitation
- Elevation profile overlaid on the temperature curve

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

Two other things fall out of the data:

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

### Known limits

- Daily positions assume a steady 60 mi/day from an Oct 1 start. Shift the dates and the
  whole curve shifts, because late October cools quickly.
- **Wind is not modeled.** On the Norwood and Grand Staircase mesas it is often the thing
  that decides your day.
- Off-station high points are estimates, not measurements. Treat them as ±5°F.
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

python3 build_data.py    # runs the model, prints a sanity-check table, writes route_weather.json
python3 build_site.py     # inlines data + Chart.js into index.html
```

Model parameters (lapse rates, seasonal drift, σ) are named constants near the top of
`build_data.py`. Change `REPO` and `VERSION` in `build_site.py` to point at your own fork.

`index.html` has **zero external requests** — Chart.js is bundled — so readers can save it
with ⌘S and it still works in a canyon with no signal. That is deliberate; please keep it
that way if you fork.

## Files

| File | What it is |
|---|---|
| `index.html` | The built, self-contained page. This is what GitHub Pages serves. |
| `build_data.py` | The weather model. Edit this to change the route or dates. |
| `build_site.py` | Inlines data + Chart.js into `index.html`. |
| `template.html` | Page markup and styling, with `__PLACEHOLDER__` tokens. |
| `route_weather.json` | Model output — the numbers, if you just want the data. |
| `vendor/chart.umd.js` | Chart.js 4.4.1, bundled for offline use (MIT). |

## Corrections

Please open an issue — especially if you've actually ridden this in October. Reports of what
the weather really did are more valuable than any refinement to the model.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Fork it, re-run it, publish it —
just credit back. Route created and stewarded by [Bikepacking Roots](https://bikepackingroots.org/project/the-plateau-passage/).
Chart.js is MIT, see `vendor/chart.js-LICENSE.md`.

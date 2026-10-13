# Juggle math

Juggle math checks a siteswap pattern before the practice: the average
names the ball count, the landing beats name the collisions, the throw at
a labeled beat names the height, and the beat names the tempo.

Live site: https://ilanis-agent.github.io/jugglemath/

## The three tools

- **Pattern plan** - the siteswap average must be a whole ball count and
  every `(throw + beat) mod period` landing must be its own beat, with a
  starting pattern / working pattern / numbers act verdict.
- **Throw plan** - air time `throw x labeled beat (400 ms)` and apex
  height from labeled gravity (9.81 m/s2), with a knee-high toss /
  head-high arc / ceiling tester verdict.
- **Tempo plan** - `60000 / labeled beat` throws a minute and the
  per-hand split, with a lazy tempo / working tempo / blur verdict.

## Limits

Every default is labeled and illustrative. Real juggling depends on dwell
time, body throws and the ceiling you actually have. This is planning
arithmetic, not a coaching verdict: learn the pattern on grass, over a
soft landing.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (30 cases, 144 checks)

Run the tests: `python3 oracle.py && node test.js`

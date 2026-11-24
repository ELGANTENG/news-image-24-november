# The World Today — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ELGANTENG/news-image-24-november/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ELGANTENG/news-image-24-november/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper-style front page summing up Tuesday 24 November 2026 in one
image: the masthead names the day, one large hero story, and six smaller
panel stories, each with a hand-drawn flat illustration, a short headline
and a one-line summary.

## The seven stories

1. **Jet scare sparks Korea alert (hero)** — Seoul briefly orders Ulleung
   islanders to take shelter after an aircraft enters South Korean airspace;
   the alert is lifted in minutes. First said to be Russian, later said to
   be possibly North Korean.
2. **Iran vows to fight US blockade** — Tehran says it will use "all its
   tools" against the US naval blockade; the Hormuz standoff goes on.
3. **NATO sends AWACS to Poland** — An early-warning aircraft goes to
   Poland after three Russian missiles landed there on Friday.
4. **US hits Iran's shadow banks** — Treasury sanctions dozens of exchange
   houses and front firms; $14.7bn in suspect flows identified.
5. **Three killed in Gaza strikes** — Israeli strikes kill three, including
   an UNRWA worker at a well in Jabalia camp.
6. **24 dead in factory fire in Indonesia** — A blaze at a candy factory in
   Banten; about 30 workers still missing as rescuers search.
7. **COP31 ends with no deal** — Climate talks collapse in Antalya;
   backlash in Australia, despair among Pacific nations.

## How it works

- `generate_image.py` draws the 1024×1024 front page with PIL and DejaVu
  fonts — fixed coordinates, no timestamps, no randomness, no network —
  and writes `entry.png` (under 1 MiB).
- `main.ts` (Node 22, standard library only) copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR` (or `out` if unset). Both runs write byte-identical
  output.

Sources: Reuters, AP, UNRWA, US Treasury.

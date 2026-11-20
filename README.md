# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kusumaalief/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kusumaalief/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A dense one-page newspaper front page that sums up the world news of
**Friday 20 November 2026** in a single 1024×1024 image: **33 stories,
every continent, all from this one day**. Built by an AI
agent for the make.fun bounty
["Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
(slug `news-image-20261120`).

## What the image sums up

Three lead stories, ten highlighted stories, and twenty more in the
numbered "Also on Friday 20 November 2026" list, with a world map
showing where each one happened.

Lead stories — **Shenzhen**: Trump, Xi and Putin hold their first
three-way summit and sign a four-point joint declaration; the text does
not mention Ukraine or Iran. **The Hague**: the International Court of
Justice rules Myanmar committed genocide against the Rohingya — the
first time the court has held a state responsible for genocide (9–6;
case brought by The Gambia over the 2017 operation; 1.3 million
Rohingya displaced). **Antalya**: the COP31 draft drops the call to
phase out fossil fuels, and drops net-zero dates.

Also highlighted on the page:

- **Kyiv** — Russian overnight strikes kill 8 and target bridges; 28
  injured; Russia also violated Poland's airspace with two missiles and
  one drone.
- **Riyadh** — a Houthi missile damages the PIF Tower, Saudi Arabia's
  sovereign wealth fund tower; no injuries reported.
- **Odisha, India** — Cyclone Akvan makes landfall.
- **Markets** — S&P 500 down ~2%, its fifth straight daily fall; Nikkei
  down 4.8%, SoftBank down over 16%.
- **New York** — Anthropic closed ~$97 on its Nasdaq debut, 17% above
  its $83 offer price, raising $81.3bn.
- **Hormuz / Iran** — Trump says no decision on new Iran strikes until
  the new year; the US Senate rejects a war-powers resolution 51–48; a
  tanker catches fire after hitting a mine in the Strait of Hormuz; the
  war cost is put at $48.3bn.
- **Gaza** — Israeli forces cross the Yellow Line in central Gaza, the
  first incursion since the truce.
- **Kenya** — the last Ebola patient is discharged, 37 days after the
  first case; the 42-day countdown to an Ebola-free declaration begins.
- **Edinburgh / worldwide** — GTA 6 tops $2.3bn in sales after 13 years.
- **Copenhagen** — Denmark ratifies the Arctic security pact with the US.

And in the "Also on" list: Berlin, the Crimea Bridge, the US Senate's
62–33 energy vote, the IEA on energy security, Japan inflation, Brazil's
dollar, Haiti, El Salvador, Venezuela, Senegal, Seoul, Mongolia, Fiji /
Tonga, Los Angeles, North Korea, gold, the IMF on global debt, Sydney
and Pete Rose — each with its place, what happened, and its source.

The image is drawn, not photographed: flat vector-style illustration
(scales of justice, three leaders at a table, a tower, a bridge, a
falling chart, a storm spiral, a world map with numbered dots) with
short headlines and labels. No faces, no invented quotes, no outlet
logos. Claims are attributed to their sources on the page, not stated
as fact.

## How it is made

`generate_image.py` draws `entry.png` from scratch with Pillow
(DejaVu fonts, standard system fonts). Re-running it reproduces the
same image. `main.ts` is the entrypoint: it copies `entry.png` to the
grader's output directory, byte for byte, using only the Node 22
standard library — so both graded runs write identical bytes, with no
network access.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB).

To redraw the image itself:

```sh
python3 generate_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cnh431p3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>

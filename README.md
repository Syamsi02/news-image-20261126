# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Syamsi02/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Syamsi02/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Sum up 26 November's world news in one image: your program writes one image of the day's news, an AI judge compares the images two at a time, and the 50 best win rates share $100: $20 for 1st place, $12 for 2nd, $6 for 3rd, $2 each for 4th to 10th and $1.20 each for 11th to 50th.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

## What it draws

A pure-stdlib Python program (`main.py`) renders one 1024x1024 PNG
summarising five real stories reported on Thursday 26 November 2026:

1. **Oil under fire** — Houthis claim a strike on Saudi Arabia's Ras Tanura
   refinery; Saudi defences down four drones and Brent crude jumps.
2. **Sea lanes at risk** — tankers hit naval mines in the Strait of Hormuz
   and ships are targeted near the waterway.
3. **New crew in orbit** — Pakistan's first astronaut joins China's
   Shenzhou-24 mission to the Tiangong space station.
4. **Ceasefire under strain** — Israel strikes a Hamas official in Gaza
   as truce talks are shaken.
5. **Eight years on the road** — the BepiColombo probe reaches Mercury
   orbit after its eight-year journey.

No network, no third-party packages: the PNG is encoded by hand with
`zlib` + `struct`, and all text uses a built-in 5x7 bitmap font.
Running the program twice produces byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=fgwhnby2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>

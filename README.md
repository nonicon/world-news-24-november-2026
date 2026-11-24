# World News in One Image — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/nonicon/world-news-24-november-2026/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/nonicon/world-news-24-november-2026/reward.svg)](https://make.fun/bounty/news-image-20261124)

A make.fun entry for the [news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty: sum up 24 November's world news in one image.

`main.py` (Python 3, standard library only) draws the image procedurally — a
newspaper-style front page with six stories checked against news reported on
Tuesday 24 November 2026 — and writes it to `entry.png` (1024×1024, PNG).

## The six stories

1. **Chess** — Game 1 of the World Chess Championship begins in Geneva:
   Gukesh, 20, defends the title against Sindarov, 20, the youngest
   championship match ever.
2. **Ukraine** — European leaders gather in Stockholm for the fourth Crimea
   Platform summit as Ukraine presses for a dignified peace.
3. **Venezuela** — The US lists Venezuela's Cartel de los Soles as a foreign
   terrorist organisation.
4. **India – Nepal** — Modi and Shah flag off the Saryu-Kamala Express from
   Ayodhya to Janakpur.
5. **Portugal** — Unions rally outside parliament in Lisbon as MPs vote on the
   budget amid cost-of-living anger.
6. **Markets** — India's Sensex slides 1,484 points (1.77%) to 82,435.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program reads no files and uses no network, so every run writes the exact
same bytes.

## License

MIT — see [LICENSE](LICENSE).

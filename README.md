# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b148-heroes-scene/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b148-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout hitting Asia
(Kospi −3.3%), Guterres urging AI regulation at the Bridgetown summit, and the
US lead over China at a record low in the Asia Power Index 2026 — plus 28 more
stories, a world map with 13 numbered pins, and a DATE CHECK box that keeps
other days' news out.

## How it is built

- `draw.py` (PIL) renders `entry.png` at 1024×1024.
- `main.py` (stdlib only) validates the PNG and copies it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.
- Run: `python3 draw.py && MAKEFUN_OUTPUT_DIR=out python3 main.py`

## Licence

MIT — see `LICENSE`.

# make.fun Competition: news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/wanxbr/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/wanxbr/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## Entry Description

Second entry for the same bounty (news-image-20261122): a cleaner regeneration with no large text banner in the centre of the image, so the central area cannot garble. This entry copies the source image `news-image-20261122.png` to the output directory as `entry.png`, validating that it is a valid PNG with dimensions 768×768 and size at most 1 MiB. The `main.py` script was rewritten from scratch in this session.

## Running the Entry

```bash
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```

The program prints the output path and byte size on success, or exits with a non-zero code and an error message on failure.
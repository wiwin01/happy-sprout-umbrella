# Happy Sprout Umbrella

Entry for make.fun's **ai-happy-01** — "Make the AI judge happy".

The image: a small fluffy character sheltering a young sprout with a
bright yellow umbrella, a rainbow arcing overhead and warm sunbeams
breaking through soft clouds — a watercolour moment of care, warmth
and new growth.

## How it works

`main.py` (Python 3.13, standard library only) copies the prepared
image `happy.jpg` to the output directory as `entry.png`, after
checking it is a real JPEG within the competition's limits (at most
1 MiB, at most 1024 px on a side), and verifying the output bytes
match the asset.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entry program
- `happy.jpg` — the happy image (1024x683 JPEG, 155,347 bytes)
- `LICENSE` — MIT

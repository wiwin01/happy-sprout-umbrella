"""Happy-image entry for make.fun ai-happy-01.

Copies the prepared happy image (a fluffy character sheltering a sprout
with a yellow umbrella, rainbow and sunbeams, watercolour style) to the
output directory as entry.png. The asset is JPEG bytes; the competition
names the output entry.png either way and tells PNG from JPEG by the
first bytes, so the name stays entry.png.

Runs with the standard library only:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

ASSET_NAME = "happy.jpg"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576  # 1 MiB, the competition's file cap
MAX_SIDE = 1024  # the competition's per-side pixel cap
JPEG_MAGIC = b"\xff\xd8\xff"


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Read width and height from a JPEG's first start-of-frame segment."""
    pos = 2  # skip the SOI marker
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("bad JPEG marker")
        marker = data[pos + 1]
        size = int.from_bytes(data[pos + 2:pos + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):  # baseline / progressive SOF
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + size
    raise ValueError("no JPEG start-of-frame segment found")


def main() -> int:
    here = Path(__file__).resolve().parent
    asset = here / ASSET_NAME
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target = out_dir / OUTPUT_NAME

    data = asset.read_bytes()
    if not data.startswith(JPEG_MAGIC):
        print(f"asset {ASSET_NAME} is not a JPEG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"asset {ASSET_NAME} is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    width, height = jpeg_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"asset is {width}x{height}, over the {MAX_SIDE}px cap",
              file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(asset, target)
    if target.read_bytes() != data:
        print("output differs from the asset", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

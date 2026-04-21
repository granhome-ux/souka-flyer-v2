"""
Remove checkerboard-pattern transparency preview burned into PNG images.

Strategy:
- Sample 50x50 blocks at each of the 4 corners (assumed to be background).
- Collect top-N most frequent colors (quantized to 8-unit buckets) as background-color candidates.
- For each pixel, if its RGB is within +/- 30 of ANY candidate color, set alpha = 0.
- Save an RGBA PNG (original-named) and a red-highlight validation PNG.

Usage: python _decheckerize.py
"""
import os
import sys
import time
import json
from PIL import Image
import numpy as np

BASE = r"C:\Users\kezoi\Desktop\souka-flyer"
IMAGES_DIR = os.path.join(BASE, "images")
PREVIEW_DIR = os.path.join(IMAGES_DIR, "_preview_transparent")
TARGETS = ["iyokan.png", "buntan.png", "ponkan.png", "sakuranbo.png"]

CORNER = 50          # corner sample box size
QUANT = 8            # quantization bucket (smaller = stricter)
TOP_N = 3            # number of dominant corner colors to use as background keys
THRESHOLD = 30       # RGB +/- range treated as background


def detect_background_colors(arr):
    h, w = arr.shape[:2]
    # Gather corner RGB pixels
    corners = [
        arr[0:CORNER, 0:CORNER, :3],
        arr[0:CORNER, max(0, w - CORNER):w, :3],
        arr[max(0, h - CORNER):h, 0:CORNER, :3],
        arr[max(0, h - CORNER):h, max(0, w - CORNER):w, :3],
    ]
    stacked = np.concatenate([c.reshape(-1, 3) for c in corners], axis=0)
    quantized = (stacked // QUANT) * QUANT
    unique, counts = np.unique(quantized, axis=0, return_counts=True)
    top = np.argsort(-counts)[:TOP_N]
    return unique[top], counts[top], stacked.shape[0]


def process(name):
    src = os.path.join(IMAGES_DIR, name)
    dst = src  # overwrite original
    preview = os.path.join(PREVIEW_DIR, name)
    t0 = time.time()

    with Image.open(src) as im:
        rgba = im.convert("RGBA")
    arr = np.array(rgba)
    h, w = arr.shape[:2]

    bg_colors, bg_counts, total_corner = detect_background_colors(arr)

    rgb = arr[:, :, :3].astype(np.int32)
    mask = np.zeros(arr.shape[:2], dtype=bool)
    for c in bg_colors:
        diff = np.abs(rgb - c.astype(np.int32))
        within = np.all(diff <= THRESHOLD, axis=-1)
        mask |= within

    out = arr.copy()
    out[mask, 3] = 0
    Image.fromarray(out, "RGBA").save(dst, "PNG")

    prev = arr.copy()
    prev[mask, 0] = 255
    prev[mask, 1] = 0
    prev[mask, 2] = 0
    prev[mask, 3] = 255
    Image.fromarray(prev, "RGBA").save(preview, "PNG")

    elapsed = time.time() - t0
    transparent_pct = float(mask.sum()) / mask.size * 100.0
    return {
        "file": name,
        "w": int(w),
        "h": int(h),
        "elapsed_sec": round(elapsed, 3),
        "transparent_pct": round(transparent_pct, 2),
        "bg_colors": [c.tolist() for c in bg_colors],
        "bg_counts": [int(x) for x in bg_counts],
        "out_size": os.path.getsize(dst),
        "preview_path": preview,
    }


def main():
    results = []
    for name in TARGETS:
        try:
            r = process(name)
            results.append(r)
            print(f"[OK] {name}: {r['transparent_pct']}% transparent, "
                  f"{r['elapsed_sec']}s, bg={r['bg_colors']}, "
                  f"out_size={r['out_size']} bytes")
        except Exception as e:
            print(f"[ERROR] {name}: {type(e).__name__}: {e}", file=sys.stderr)
            sys.exit(2)
    print("\n=== JSON SUMMARY ===")
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()

from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\kezoi\Desktop\souka-flyer\images\bg\bg.png").convert("RGB")
arr = np.array(img)
gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
dark = gray < 100

h, w = dark.shape

def longest_run(vec):
    max_run = 0
    cur = 0
    for v in vec:
        if v:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 0
    return max_run

vert_scores = np.array([longest_run(dark[:, x]) for x in range(w)])
horiz_scores = np.array([longest_run(dark[y, :]) for y in range(h)])

vline_mask = vert_scores > h * 0.55
hline_mask = horiz_scores > w * 0.25

def group_consecutive(positions, max_gap=5):
    if len(positions) == 0:
        return []
    groups = [[positions[0]]]
    for p in positions[1:]:
        if p - groups[-1][-1] <= max_gap:
            groups[-1].append(p)
        else:
            groups.append([p])
    return groups

vlines = np.where(vline_mask)[0].tolist()
hlines = np.where(hline_mask)[0].tolist()

vg = group_consecutive(vlines)
hg = group_consecutive(hlines)

print(f"bg.png size: {w} x {h}")
print(f"Detection thresholds: vertical run > {int(h*0.55)}px, horizontal run > {int(w*0.25)}px")

print("\nVertical lines (column groups):")
for g in vg:
    cx = round((g[0] + g[-1]) / 2)
    print(f"  x={g[0]:4d}-{g[-1]:4d}  center={cx:4d}  thickness={g[-1]-g[0]+1}px")

print("\nHorizontal lines (row groups):")
for g in hg:
    cy = round((g[0] + g[-1]) / 2)
    print(f"  y={g[0]:4d}-{g[-1]:4d}  center={cy:4d}  thickness={g[-1]-g[0]+1}px")

# Derive column boundaries
v_centers = [round((g[0] + g[-1]) / 2) for g in vg]
h_centers = [round((g[0] + g[-1]) / 2) for g in hg]

print("\n=== Column boundaries (vertical line centers) ===")
print(f"  {v_centers}")
print("=== Row boundaries (horizontal line centers) ===")
print(f"  {h_centers}")

# Compute block rects assuming 4 vertical lines: [outer-left, col-div-1, col-div-2, outer-right]
if len(v_centers) >= 4:
    col_left_x = (v_centers[0], v_centers[1])  # left column bounds
    col_mid_x  = (v_centers[1], v_centers[2])  # center band
    col_right_x = (v_centers[2], v_centers[3])  # right column bounds

    print("\n=== Inferred column regions ===")
    print(f"  Left column:   x={col_left_x[0]}-{col_left_x[1]} (width {col_left_x[1]-col_left_x[0]})")
    print(f"  Center band:   x={col_mid_x[0]}-{col_mid_x[1]} (width {col_mid_x[1]-col_mid_x[0]})")
    print(f"  Right column:  x={col_right_x[0]}-{col_right_x[1]} (width {col_right_x[1]-col_right_x[0]})")

# Separate horizontal lines per column (only those within left/right col ranges)
# For each column, find horizontal dividers by limiting run detection to that column range
def hlines_in_range(xs, xe, min_frac=0.75):
    region = dark[:, xs:xe]
    # For each row in region, count dark pixels
    row_runs = np.array([longest_run(region[y, :]) for y in range(h)])
    width = xe - xs
    mask = row_runs > width * min_frac
    idx = np.where(mask)[0].tolist()
    return group_consecutive(idx)

if len(v_centers) >= 4:
    print("\n=== Horizontal dividers inside LEFT column ===")
    for g in hlines_in_range(v_centers[0] + 5, v_centers[1] - 5, min_frac=0.5):
        cy = round((g[0] + g[-1]) / 2)
        print(f"  y={g[0]:4d}-{g[-1]:4d}  center={cy:4d}")

    print("\n=== Horizontal dividers inside RIGHT column ===")
    for g in hlines_in_range(v_centers[2] + 5, v_centers[3] - 5, min_frac=0.5):
        cy = round((g[0] + g[-1]) / 2)
        print(f"  y={g[0]:4d}-{g[-1]:4d}  center={cy:4d}")

    # Top/bottom of content area = first/last horizontal lines spanning entire width
    print("\n=== Outer-frame horizontal lines (top/bottom) ===")
    for g in hlines_in_range(0, w, min_frac=0.8):
        cy = round((g[0] + g[-1]) / 2)
        print(f"  y={g[0]:4d}-{g[-1]:4d}  center={cy:4d}")

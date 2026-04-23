from PIL import Image

SRC = "images/bg/1409443.jpg"
DST = "images/bg/bg_a4.png"
TARGET_W = 1754
TARGET_H = 1240

src = Image.open(SRC).convert("RGB")
print(f"Source: {src.size}")
print(f"Source aspect: {src.size[0] / src.size[1]:.4f}")
print(f"Target aspect: {TARGET_W / TARGET_H:.4f}")

# 縦横比を A4 横 (1.4145:1) に合わせる
# 元画像の縦横比を計算して、縦横比が違う場合はセンタークロップ
src_ratio = src.size[0] / src.size[1]
target_ratio = TARGET_W / TARGET_H

if abs(src_ratio - target_ratio) < 0.01:
    # 縦横比がほぼ一致 → そのままリサイズ
    resized = src.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    print("Aspect matches. Direct resize.")
else:
    # 縦横比が違う → センタークロップしてから目標サイズにリサイズ
    if src_ratio > target_ratio:
        # 元画像が横長すぎる → 左右をカット
        new_w = int(src.size[1] * target_ratio)
        left = (src.size[0] - new_w) // 2
        cropped = src.crop((left, 0, left + new_w, src.size[1]))
    else:
        # 元画像が縦長すぎる → 上下をカット
        new_h = int(src.size[0] / target_ratio)
        top = (src.size[1] - new_h) // 2
        cropped = src.crop((0, top, src.size[0], top + new_h))
    print(f"Center-cropped to: {cropped.size}")
    resized = cropped.resize((TARGET_W, TARGET_H), Image.LANCZOS)

resized.save(DST, optimize=True)
print(f"Saved: {DST} ({TARGET_W}x{TARGET_H})")

# 実測確認
out = Image.open(DST)
print(f"Verify output: {out.size}")

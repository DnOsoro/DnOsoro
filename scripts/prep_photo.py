"""Prep a photo for ASCII conversion (no model download needed for white/plain backgrounds).
Usage: python scripts/prep_photo.py source-photo.jpg [crop_bottom_fraction]
 - isolates the subject (flood-fill from the edges on a light background)
 - crops to head + neck, boosts local contrast (CLAHE) and lifts shadows
 - writes source-prepped.png (white background)"""
import sys
import cv2, numpy as np
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
crop_bottom = float(sys.argv[2]) if len(sys.argv) > 2 else 0.68   # drop the shirt

img = cv2.imread(src)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
gray = gray[: int(h * crop_bottom)]
img_h = gray.shape[0]

# subject mask: everything not connected to the light border
bg = (gray > 238).astype(np.uint8)
flood = bg.copy()
ff = np.zeros((img_h + 2, w + 2), np.uint8)
for seed in [(0, 0), (w - 1, 0)]:
    cv2.floodFill(flood, ff, seed, 2)
mask = (flood != 2).astype(np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(mask)
mask = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)

# contrast: lift shadows (gamma) then CLAHE
g = (255 * (gray / 255.0) ** 0.55).astype(np.uint8)
g = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(g)
out = np.where(mask > 0, g, 255).astype(np.uint8)

ys, xs = np.where(mask > 0)
pad = 12
out = out[max(ys.min() - pad, 0): ys.max() + pad, max(xs.min() - pad, 0): xs.max() + pad]
Image.fromarray(out).save("source-prepped.png")
print("wrote source-prepped.png", out.shape[::-1])

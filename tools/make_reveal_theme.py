"""Make a downloadable "reveal" scene for Medina Nights from one lit photo.

Turns the warm lights off for the night version, finds the places that
light up (warm bright spots, spread out), writes the theme folder and prints
the catalog entry to paste into catalog.json.

usage:
  python -I tools/make_reveal_theme.py <lit.jpg> <id> "<title>" "<line>" [--order near|bright|top]

Writes <id>/lit.jpg, <id>/night.jpg, <id>/card.jpg (1080 x 1920, 420 px card).
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter


def main():
    src, tid, title, line = sys.argv[1:5]
    order = sys.argv[sys.argv.index('--order') + 1] if '--order' in sys.argv else 'near'
    os.makedirs(tid, exist_ok=True)
    img = Image.open(src).convert('RGB').resize((1080, 1920))
    lit = np.asarray(img).astype(np.float32) / 255
    r, g, b = lit[..., 0], lit[..., 1], lit[..., 2]
    lum = lit @ np.array([0.2126, 0.7152, 0.0722], np.float32)

    # night: warm light off, cool and dim
    wk = np.clip((r - b) * 2.6, 0, 1) * np.clip((lum - 0.08) * 3, 0, 1)
    cool = (np.power(lum, 1.2) * 0.33)[..., None] * np.array([0.55, 0.68, 0.82], np.float32)
    night = lit * 0.6 * (1 - wk[..., None]) + cool * wk[..., None]

    img.save(f'{tid}/lit.jpg', quality=86)
    Image.fromarray(np.clip(night * 255, 0, 255).astype(np.uint8)).save(f'{tid}/night.jpg', quality=86)
    img.resize((420, 747)).save(f'{tid}/card.jpg', quality=82)

    # points: warm bright spots, spread out
    small = np.asarray(img.resize((270, 480))).astype(np.float32) / 255
    sr, sg, sb = small[..., 0], small[..., 1], small[..., 2]
    sl = 0.2126 * sr + 0.7152 * sg + 0.0722 * sb
    score = gaussian_filter(np.clip((sr - sb) * 2, 0, 1) * np.clip((sl - 0.3) * 2.5, 0, 1), 1.0)
    H, W = score.shape
    pts, s = [], score.copy()
    for _ in range(110):
        i = int(np.argmax(s))
        if s.flat[i] < 0.04:
            break
        y, x = divmod(i, W)
        pts.append((x / W, y / H, float(s.flat[i])))
        s[max(0, y - 6):y + 6, max(0, x - 6):x + 6] = 0
    rng = np.random.default_rng(5)
    if order == 'near':
        pts.sort(key=lambda p: -p[1] + rng.uniform(-0.03, 0.03))
    elif order == 'top':
        pts.sort(key=lambda p: p[1] + rng.uniform(-0.03, 0.03))
    else:  # bright first
        pts.sort(key=lambda p: -p[2] + rng.uniform(-0.05, 0.05))
    entry = {
        'id': tid, 'version': 1, 'title': title, 'line': line, 'pro': True, 'kind': 'reveal',
        'card': 'card.jpg', 'files': {'night': 'night.jpg', 'lit': 'lit.jpg'},
        'points': [[round(x, 4), round(y, 4), 0.05] for x, y, _ in pts],
    }
    print(json.dumps(entry, ensure_ascii=False))


if __name__ == '__main__':
    main()

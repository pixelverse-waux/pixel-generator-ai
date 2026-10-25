"""Pull the main colours from a reference photo and suggest Pokemon-style ramps.

    python3 -m pixelkit.palette "input/white_persian.avif" [--colors 8] [--crop 0.6]

Each colour gets four tones: outline (very dark, hue pushed toward blue/purple),
shade (darker, hue shifted cooler), base, light (brighter, hue shifted warmer,
less saturated). Background colours show up too: use the share column and your
own look at the photo to skip them.
"""
import argparse
import colorsys

from PIL import Image

from .pxl import rgb_to_hex

COOL, WARM = 250.0, 55.0  # hue targets in degrees: shadows lean blue/purple, lights lean yellow


def shift_hue(h, target, amount):
    """Move hue h (degrees) toward target by `amount` degrees along the short way round."""
    d = (target - h + 180) % 360 - 180
    step = max(-amount, min(amount, d))
    return (h + step) % 360


def tone(rgb, dv, ds, hue_target, hue_amount):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    h = shift_hue(h * 360, hue_target, hue_amount) / 360 if s > 0.08 else h
    s = min(1, max(0, s + ds))
    v = min(1, max(0, v + dv))
    return tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))


def ramp(rgb):
    outline = tone(rgb, -0.62, -0.05, COOL, 25)
    if max(outline) < 24:
        # never pure black: keep a hint of the colour's hue
        outline = tone(rgb, -(colorsys.rgb_to_hsv(*(c / 255 for c in rgb))[2] - 0.1), -0.05, COOL, 25)
    return {
        "outline": outline,
        "shade": tone(rgb, -0.16, +0.08, COOL, 10),
        "base": tuple(rgb),
        "light": tone(rgb, +0.12, -0.14, WARM, 8),
    }


def main_colours(path, n, crop):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    mx, my = int(w * (1 - crop) / 2), int(h * (1 - crop) / 2)
    img = img.crop((mx, my, w - mx, h - my))
    img.thumbnail((200, 200))
    q = img.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    return [(tuple(pal[i * 3:i * 3 + 3]), c / total) for c, i in counts]


def describe(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    return f"h{round(h * 360):3d} s{round(s * 100):3d} v{round(v * 100):3d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo")
    ap.add_argument("--colors", type=int, default=8)
    ap.add_argument("--crop", type=float, default=0.6, help="keep this middle fraction of the photo")
    a = ap.parse_args()

    cols = main_colours(a.photo, a.colors, a.crop)
    print("share  colour   hsv")
    for rgb, share in cols:
        print(f"{share * 100:4.0f}%  {rgb_to_hex(rgb)}  {describe(rgb)}")
    print("\n; suggested ramps (pick the subject's colours, drop background ones)")
    print("palette")
    for i, (rgb, share) in enumerate(cols):
        r = ramp(rgb)
        print(f"; colour {i + 1} ({share * 100:.0f}% of the middle of the photo)")
        for role in ("outline", "shade", "base", "light"):
            print(f"? {rgb_to_hex(r[role])} {role} of colour {i + 1}")


if __name__ == "__main__":
    main()

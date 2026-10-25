"""Render a .pxl sprite to a sheet PNG, a zoomed preview and a walk GIF.

Everything for one sprite goes in its own folder, out/<name>/. A sprite kept in a subfolder
of sprites/ (sprites/ginger_tabby/move.pxl) goes to that subfolder's folder instead (out/ginger_tabby/).
People live in sprites/characters/ but still get their own folder (out/<name>/):

    python3 -m pixelkit.render sprites/cat.pxl            -> out/<name>/<name>.png, _preview.png, _walk.gif
    python3 -m pixelkit.render sprites/cat.pxl --only down_0   -> out/<name>/<name>_down_0.png (12x zoom)
    python3 -m pixelkit.render sprites/cat.pxl --silhouette    -> out/<name>/<name>_silhouette.png
"""
import argparse
import os

from PIL import Image

from . import pxl

OUT = "out"


def group_of(path):
    """'ginger_tabby' for sprites/ginger_tabby/move.pxl, else None."""
    parent = os.path.dirname(os.path.abspath(path))
    if os.path.basename(os.path.dirname(parent)) == "sprites" and os.path.basename(parent) != "characters":
        return os.path.basename(parent)
    return None


def out_base(name, group=None):
    """out/<group or name>/<name>, creating the folder."""
    folder = os.path.join(OUT, group or name)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, name)


def frame_image(sp, name, scale=1):
    img = Image.new("RGBA", (sp.width, sp.height), (0, 0, 0, 0))
    pix = img.load()
    for y, row in enumerate(sp.grid(name)):
        for x, ch in enumerate(row):
            if ch != pxl.TRANSPARENT:
                pix[x, y] = sp.palette[ch] + (255,)
    if scale != 1:
        img = img.resize((sp.width * scale, sp.height * scale), Image.NEAREST)
    return img


def sheet_image(sp, scale=None):
    scale = scale or sp.scale
    layout = sp.sheet_layout()
    cols = max(len(r) for r in layout)
    img = Image.new("RGBA", (cols * sp.width * scale, len(layout) * sp.height * scale), (0, 0, 0, 0))
    for r, row in enumerate(layout):
        for c, name in enumerate(row):
            img.paste(frame_image(sp, name, scale), (c * sp.width * scale, r * sp.height * scale))
    return img


def checker(size, cell=8, a=(236, 236, 236), b=(250, 250, 250)):
    img = Image.new("RGBA", size, b + (255,))
    pix = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            if (x // cell + y // cell) % 2:
                pix[x, y] = a + (255,)
    return img


def on_checker(img, cell=8):
    bg = checker(img.size, cell)
    bg.alpha_composite(img)
    return bg


def walk_gif(sp, path, scale=4, ms=180):
    rows = [r for r in sp.sheet_layout() if r]
    w, h = sp.width * scale, sp.height * scale
    frames = []
    for i in range(max(len(r) for r in rows)):
        canvas = Image.new("RGB", (w * len(rows), h), (255, 255, 255))
        for d, row in enumerate(rows):
            f = frame_image(sp, row[i % len(row)], scale)
            canvas.paste(f, (d * w, 0), f)
        frames.append(canvas)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=ms, loop=0)


def render(path, only=None, silhouette=False):
    sp = pxl.load(path)
    base = out_base(sp.name, group_of(path))
    if silhouette:
        sp.palette = {k: (0, 0, 0) for k in sp.palette}
        out = base + "_silhouette.png"
        on_checker(sheet_image(sp, 4), 4).save(out)
        return [out]
    if only:
        out = f"{base}_{only}.png"
        on_checker(frame_image(sp, only, 12), 12).save(out)
        return [out]
    sheet_image(sp).save(base + ".png")
    on_checker(sheet_image(sp, 8)).save(base + "_preview.png")
    walk_gif(sp, base + "_walk.gif")
    return [base + ".png", base + "_preview.png", base + "_walk.gif"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--only", help="render a single frame at 12x")
    ap.add_argument("--silhouette", action="store_true", help="render the sheet in solid black at 4x")
    args = ap.parse_args()
    try:
        for p in render(args.file, args.only, args.silhouette):
            print("wrote", p)
    except pxl.PxlError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    main()

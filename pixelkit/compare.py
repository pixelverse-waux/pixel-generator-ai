"""Put the reference photo, a drawn frame and the palette side by side.

    python3 -m pixelkit.compare "input/white_persian.avif" sprites/white_persian.pxl [--frame down_0]  -> out/<name>/<name>_compare.png
"""
import argparse

from PIL import Image, ImageDraw

from . import pxl
from .render import frame_image, group_of, on_checker, out_base

H = 480


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo")
    ap.add_argument("file")
    ap.add_argument("--frame", default="down_0")
    a = ap.parse_args()

    sp = pxl.load(a.file)
    photo = Image.open(a.photo).convert("RGBA")
    photo = photo.resize((max(1, photo.width * H // photo.height), H), Image.LANCZOS)
    zoom = max(1, H // sp.height)
    art = on_checker(frame_image(sp, a.frame, zoom), zoom)

    sw = 150
    swatches = Image.new("RGBA", (sw, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(swatches)
    row = max(14, min(28, H // max(1, len(sp.palette))))
    for i, (k, c) in enumerate(sp.palette.items()):
        y = i * row
        d.rectangle((6, y + 2, 6 + row - 4, y + row - 2), fill=c + (255,), outline=(0, 0, 0, 255))
        d.text((row + 8, y + row // 2 - 6), f"{k} {pxl.rgb_to_hex(c)}", fill=(0, 0, 0, 255))

    gap = 12
    out = Image.new("RGBA", (photo.width + art.width + sw + gap * 2, H), (255, 255, 255, 255))
    out.paste(photo, (0, 0))
    out.paste(art, (photo.width + gap, (H - art.height) // 2))
    out.paste(swatches, (photo.width + art.width + gap * 2, 0))
    path = out_base(sp.name, group_of(a.file)) + "_compare.png"
    out.save(path)
    print("wrote", path)


if __name__ == "__main__":
    main()

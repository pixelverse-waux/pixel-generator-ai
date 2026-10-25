"""Build every cat_ref action (walk, idle, sit, lie, meow, groom, ...) for one cat.

    python3 -m pixelkit.actions sprites/ginger_tabby/coat.json [--render] [--only move,sit]

The poses come from refs/local/cat_ref/*.pxl. The coat file says how this cat differs:
colours for the reference's letter roles, markings painted on every frame, and a few body
changes that work in any pose. Output: sprites/<cat>/<action>.pxl (+ renders in out/<cat>/).

Coat file (JSON):
{
  "name": "ginger_tabby",
  "photo": "input/cat.jpeg",                 optional, for notes only
  "palette": {"K": "#1e1410", "A": "#b8642b", "B": "#e8963f", "C": "#f6c27e",
              "D": "#ec9a96", "E": "#f2b0a0", "F": "#e8a0b0", "G": "#f4f1ec"},
  "extra":   {"W": ["#fbf6ee", "white"], "s": ["#a34e1d", "tabby stripe"]},
  "shape":   {"ears": 0, "fluff": 0},
  "markings": {"white_muzzle": "W", "white_chest": "W", "white_legs": true,
               "forehead_m": "s", "back_bars": "s", "mask": null, "eyes": null,
               "wrinkles": null}
}

Reference letter roles (refs/local/cat_ref/INDEX.md): K outline/eyes, A fur shade, B fur,
C back light, D nose, E inner ear, F open mouth, G eye glint.

shape.ears N    stretch the ears N rows taller wherever the inner ear (E) shows
shape.fluff N   long fur: push every Nth outline pixel on the lower and side edges out by 1
markings        each value is the letter to paint with (null = off):
  white_muzzle  around the nose       white_chest   bib below the chin (+ white_legs: down to the feet)
  forehead_m    tabby M (front) / stripe (side)  back_bars  bars across the light back stripe
  mask          face mask around the nose        eyes       eye colour (lower eye pixel)
  wrinkles      hairless wrinkle dashes on forehead and chest
"""
import argparse
import glob
import json
import os

from PIL import Image, ImageDraw

from . import pxl

REF_DIR = "refs/local/cat_ref"
FUR = "ABC"
ROLE_NOTES = {"K": "outline, eyes", "A": "fur shade", "B": "fur", "C": "fur light (back)",
              "D": "nose", "E": "inner ear", "F": "open mouth", "G": "eye glint"}


class Frame:
    def __init__(self, rows):
        self.g = [list(r) for r in rows]
        self.h, self.w = len(self.g), len(self.g[0])

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def set(self, x, y, ch, only=FUR):
        if 0 <= x < self.w and 0 <= y < self.h and (only is None or self.g[y][x] in only):
            self.g[y][x] = ch

    def rows(self):
        return ["".join(r) for r in self.g]

    def find(self, ch):
        return [(x, y) for y in range(self.h) for x in range(self.w) if self.g[y][x] == ch]

    def face(self):
        """(nose_x, nose_y, facing) or None when the face isn't visible."""
        noses = self.find("D")
        filled = [(x, y) for y in range(self.h) for x in range(self.w) if self.g[y][x] != "."]
        if not noses or not filled:
            return None
        xs = [p[0] for p in filled]
        cx = (min(xs) + max(xs)) / 2
        nx, ny = noses[0]
        facing = "left" if nx < cx - 2 else "right" if nx > cx + 2 else "front"
        return nx, ny, facing


# ---- body shape ---------------------------------------------------------------

def close_outline(f, x0, y0, x1, y1):
    """Inside the box, give every fill pixel that touches transparent an outline pixel there."""
    for y in range(max(0, y0), min(f.h, y1 + 1)):
        for x in range(max(0, x0), min(f.w, x1 + 1)):
            if f.g[y][x] in ".K":
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if f.get(x + dx, y + dy) == "." and 0 <= x + dx < f.w and 0 <= y + dy < f.h:
                    f.g[y + dy][x + dx] = "K"


def grow_ears(f, n):
    """Stretch each ear (a cluster of inner-ear E pixels plus its outline) n rows up."""
    if n <= 0:
        return
    seen, clusters = set(), []
    for p in f.find("E"):
        if p in seen:
            continue
        stack, cl = [p], []
        while stack:
            x, y = stack.pop()
            if (x, y) in seen or f.get(x, y) != "E":
                continue
            seen.add((x, y))
            cl.append((x, y))
            stack += [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        clusters.append(cl)
    for cl in clusters:
        etop = min(y for _, y in cl)
        ebot = max(y for _, y in cl)
        xs = [x for x, _ in cl]
        for x in range(min(xs) - 1, max(xs) + 2):
            top = next((y for y in range(f.h) if f.get(x, y) != "."), None)
            if top is None or top > etop + 1 or top - n < 0:
                continue
            col = [f.get(x, y) for y in range(top, ebot + 1)]
            if len(col) < 2:
                continue
            new = [col[0]] + [col[1]] * n + col[1:]
            for i, ch in enumerate(new):
                f.g[top - n + i][x] = ch
        close_outline(f, min(xs) - 3, etop - n - 2, max(xs) + 3, ebot)


def fluff(f, every):
    """Long fur: every Nth outline pixel on a straight lower or side edge moves 1 px outward.
    Corners are skipped so the outline stays closed."""
    if every <= 0:
        return
    k = 0
    for y in range(f.h):
        for x in range(f.w):
            if f.g[y][x] != "K":
                continue
            for dx, dy in ((0, 1), (-1, 0), (1, 0)):
                ox, oy, ix, iy = x + dx, y + dy, x - dx, y - dy
                # the edge must run on both sides (straight), and the tuft lands on empty space
                side = [(x + dy, y + dx), (x - dy, y - dx)]
                if any(f.get(sx, sy) == "." for sx, sy in side):
                    continue
                if any(f.get(sx + dx, sy + dy) not in ".K" for sx, sy in side):
                    continue
                if f.get(ox, oy) == "." and f.get(ix, iy) in FUR and 0 <= ox < f.w and 0 <= oy < f.h:
                    k += 1
                    if k % every == 0:
                        f.g[oy][ox] = "K"
                        f.g[y][x] = f.get(ix, iy)
                    break


# ---- markings -------------------------------------------------------------------

def paint(f, m):
    face = f.face()
    if face:
        nx, ny, facing = face
        d = 1 if facing == "left" else -1
        if m.get("mask"):
            for dx in range(-2, 3):
                for dy in range(-2, 2):
                    if abs(dx) + abs(dy) <= 2:
                        f.set(nx + dx, ny + dy, m["mask"])
        if m.get("white_muzzle"):
            for dx, dy in ((-1, 0), (1, 0), (0, 1), (-1, 1), (1, 1)):
                f.set(nx + dx, ny + dy, m["white_muzzle"])
        if facing == "front":
            if m.get("white_chest"):
                bottom = f.h if m.get("white_legs") else ny + 8
                for y in range(ny + 2, bottom):
                    for x in range(nx - 2, nx + 3):
                        f.set(x, y, m["white_chest"])
            if m.get("forehead_m"):
                for x in (nx - 2, nx, nx + 2):
                    f.set(x, ny - 4, m["forehead_m"], "B")
                f.set(nx - 1, ny - 3, m["forehead_m"], "B")
                f.set(nx + 1, ny - 3, m["forehead_m"], "B")
            if m.get("wrinkles"):
                for x in range(nx - 3, nx + 4, 2):
                    f.set(x, ny - 5, m["wrinkles"], "B")
                for x in range(nx - 2, nx + 3, 2):
                    f.set(x, ny + 4, m["wrinkles"], "B")
            if m.get("eyes"):
                for ex in (nx - 2, nx + 2):
                    f.set(ex, ny - 1, m["eyes"], "K")
        else:
            if m.get("white_chest"):
                for y in range(ny + 1, ny + 5):
                    for k in range(0, 4):
                        f.set(nx + d * k, y, m["white_chest"])
            if m.get("forehead_m"):
                f.set(nx + d * 3, ny - 4, m["forehead_m"], "B")
                f.set(nx + d * 4, ny - 4, m["forehead_m"], "B")
            if m.get("wrinkles"):
                for k in (3, 5):
                    f.set(nx + d * k, ny - 4, m["wrinkles"], "B")
                for k in (6, 8, 10):
                    f.set(nx + d * k, ny + 2, m["wrinkles"], "B")
            if m.get("eyes"):
                f.set(nx + d * 2, ny - 1, m["eyes"], "K")
    if m.get("back_bars"):
        for y in range(f.h):
            run = [x for x in range(f.w) if f.g[y][x] == "C"]
            for i, x in enumerate(run):
                if i % 3 == 1:
                    f.g[y][x] = m["back_bars"]
                    f.set(x, y + 1, m["back_bars"], "B")


# ---- build ----------------------------------------------------------------------

def build(coat_path, only=None):
    coat = json.load(open(coat_path))
    name = coat["name"]
    out_dir = os.path.dirname(os.path.abspath(coat_path))
    shape = coat.get("shape", {})
    marks = coat.get("markings", {})
    written = []
    for path in sorted(glob.glob(os.path.join(REF_DIR, "*.pxl"))):
        action = os.path.splitext(os.path.basename(path))[0]
        if only and action not in only:
            continue
        ref = pxl.load(path)
        sp = pxl.Sprite()
        sp.name = f"{name}_{action}"
        sp.width, sp.height, sp.scale = ref.width, ref.height, 2
        sp.outline = ["K"]
        sp.layout = ref.sheet_layout()
        for k, hexc in coat["palette"].items():
            sp.palette[k] = pxl.hex_to_rgb(hexc)
            sp.notes[k] = ROLE_NOTES.get(k, "")
        for k, (hexc, note) in coat.get("extra", {}).items():
            sp.palette[k] = pxl.hex_to_rgb(hexc)
            sp.notes[k] = note
        for fname in ref.frame_names():
            f = Frame(ref.grid(fname))
            grow_ears(f, shape.get("ears", 0))
            fluff(f, shape.get("fluff", 0))
            paint(f, marks)
            sp.frames[fname] = f.rows()
        out = os.path.join(out_dir, f"{action}.pxl")
        pxl.dump(sp, out)
        with open(out) as fh:
            body = fh.read()
        with open(out, "w") as fh:
            fh.write(f"; {name}, action '{action}'. Built by pixelkit.actions from {os.path.basename(coat_path)};\n"
                     f"; poses from {path}. Edit the coat file and rebuild rather than this file.\n" + body)
        written.append(out)
    return name, written


def overview(name, files):
    """out/<cat>/<cat>_all_actions.png: every action's sheet stacked with a label."""
    from .render import out_base, sheet_image
    parts = []
    for path in files:
        sp = pxl.load(path)
        im = sheet_image(sp)
        lab = Image.new("RGBA", (im.width, 14), (255, 255, 255, 255))
        ImageDraw.Draw(lab).text((2, 1), sp.name, fill=(0, 0, 0, 255))
        parts += [lab, im]
    w = max(p.width for p in parts)
    out = Image.new("RGBA", (w, sum(p.height for p in parts)), (225, 225, 225, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    path = out_base(f"{name}_all_actions", name) + ".png"
    out.save(path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("coat")
    ap.add_argument("--render", action="store_true", help="also render every action and an overview")
    ap.add_argument("--only", help="comma list of actions, e.g. move,sit")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    name, files = build(a.coat, only)
    for f in files:
        print("wrote", f)
    if a.render:
        from .render import render
        for f in files:
            render(f)
        print("wrote", overview(name, files))


if __name__ == "__main__":
    main()

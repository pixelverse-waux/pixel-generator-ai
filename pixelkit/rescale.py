"""Shrink a .pxl sprite to a smaller canvas while keeping pixel art clean (1-px outlines).

    python3 -m pixelkit.rescale sprites/golden_retriever.pxl -o sprites/x.pxl --to 48
    python3 -m pixelkit.rescale sprites/golden_retriever/sit.pxl --to 48 --phase 3,3

Scaling pixel art by a fraction in the browser makes outlines uneven (some 1 px, some 2 px).
This keeps every kept pixel exactly as drawn: it drops whole rows and columns (for 64 -> 48,
one in every four), so outlines stay 1 px. The dropped row/column phase is picked per file to
lose as few outline pixels as possible (or forced with --phase, so every action of one animal
shrinks the same way), then any fill pixel left touching the transparent background is turned
into the outline colour next to it, so the silhouette stays closed. Frames that are copies or
mirrors stay copies or mirrors. Check the result with pixelkit.lint and fix by hand.
"""
import argparse
from collections import Counter
from fractions import Fraction

from . import pxl


def kept(n_src, n_dst, phase):
    """Source indexes to keep: drop one per group, at offset `phase` inside the group."""
    ratio = Fraction(n_src, n_dst)
    group = ratio.numerator                      # e.g. 64/48 = 4/3 -> groups of 4, keep 3
    drop = group - ratio.denominator
    keep = [i for i in range(n_src) if (i % group) not in range(phase, phase + drop)]
    return keep[:n_dst]


def shrink(grid, cols, rows):
    return ["".join(grid[y][x] for x in cols) for y in rows]


def edge_fill(grid, outline):
    return [(x, y) for y, row in enumerate(grid) for x, ch in enumerate(row)
            if ch != "." and ch not in outline and any(
                not (0 <= x + dx < len(row) and 0 <= y + dy < len(grid)) or grid[y + dy][x + dx] == "."
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]


def close_outline(grid, outline):
    """Fill pixels touching the background become the outline letter most used around them."""
    g = [list(r) for r in grid]
    for x, y in edge_fill(grid, outline):
        near = Counter(grid[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                       if 0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[0])
                       and grid[y + dy][x + dx] in outline)
        g[y][x] = near.most_common(1)[0][0] if near else sorted(outline)[0]
    return ["".join(r) for r in g]


def score(sp, phase, size):
    cols, rows = kept(sp.width, size[0], phase[0]), kept(sp.height, size[1], phase[1])
    outline = set(sp.outline_letters())
    return sum(len(edge_fill(shrink(rows_, cols, rows), outline)) for rows_ in sp.frames.values())


def rescale(sp, size, phase=None):
    outline = set(sp.outline_letters())
    group_x = Fraction(sp.width, size[0]).numerator
    group_y = Fraction(sp.height, size[1]).numerator
    if phase is None:
        phase = min(((px, py) for px in range(group_x) for py in range(group_y)),
                    key=lambda p: score(sp, p, size))
    cols, rows = kept(sp.width, size[0], phase[0]), kept(sp.height, size[1], phase[1])
    sp.frames = {n: close_outline(shrink(g, cols, rows), outline) for n, g in sp.frames.items()}
    sp.width, sp.height = size
    if getattr(sp, "footprint", None):
        sp.footprint = max(1, round(sp.footprint * size[1] / len(rows)))
    return phase


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out", help="default: overwrite the file")
    ap.add_argument("--to", required=True, help="new size, e.g. 48 or 48x48")
    ap.add_argument("--phase", help="x,y: which row/column of each group to drop (default: best)")
    a = ap.parse_args()
    w, _, h = a.to.lower().partition("x")
    size = (int(w), int(h or w))
    sp = pxl.load(a.file)
    sp.defaulted = []          # write every derived frame back out explicitly
    phase = tuple(int(v) for v in a.phase.split(",")) if a.phase else None
    phase = rescale(sp, size, phase)
    pxl.dump(sp, a.out or a.file)
    print(f"wrote {a.out or a.file}: {size[0]}x{size[1]}, dropped phase {phase[0]},{phase[1]}")


if __name__ == "__main__":
    main()

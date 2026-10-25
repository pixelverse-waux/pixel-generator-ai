"""Check a .pxl sprite for common pixel-art mistakes.

    python3 -m pixelkit.lint sprites/cat.pxl [--strict]

ERROR  file can't be used (too many colours)
WARN   visible mistakes: outline gaps, stray pixels, pinholes, doubled outline,
       uneven curve steps (jaggies)
INFO   things worth a look: frames filled in by defaults, unused colours, feet rows,
       step frames that change a lot above the legs
Exit code 1 on ERROR (or on WARN with --strict).
"""
import argparse
from collections import defaultdict

from . import pxl

MAX_SHOWN = 6
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


class Report:
    def __init__(self):
        self.items = defaultdict(list)  # (level, frame, check) -> [(x, y, detail)]

    def add(self, level, frame, check, x=None, y=None, detail=""):
        self.items[(level, frame, check)].append((x, y, detail))

    def count(self, level):
        return sum(1 for k in self.items if k[0] == level)

    def print(self):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for (level, frame, check), hits in sorted(self.items.items(), key=lambda kv: (order[kv[0][0]], kv[0][1], kv[0][2])):
            where = ", ".join(
                (f"({x},{y})" if x is not None else "") + (f" {d}" if d else "")
                for x, y, d in hits[:MAX_SHOWN]
            ).strip(", ")
            more = f" (+{len(hits) - MAX_SHOWN} more)" if len(hits) > MAX_SHOWN else ""
            print(f"{level:5} {frame:10} {check}: {where}{more}")
        print(f"\n{self.count('ERROR')} error(s), {self.count('WARN')} warning(s), {self.count('INFO')} note(s)")


def at(g, x, y):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        return g[y][x]
    return pxl.TRANSPARENT


def bbox(g):
    pts = [(x, y) for y, row in enumerate(g) for x, ch in enumerate(row) if ch != pxl.TRANSPARENT]
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def check_pixels(name, g, outline, rep):
    h, w = len(g), len(g[0])
    for y in range(h):
        for x in range(w):
            ch = g[y][x]
            if ch == pxl.TRANSPARENT:
                if all(at(g, x + dx, y + dy) != pxl.TRANSPARENT for dx, dy in N4) and 0 < x < w - 1 and 0 < y < h - 1:
                    rep.add("WARN", name, "pinhole (transparent pixel inside the sprite)", x, y)
                continue
            if ch not in outline and any(at(g, x + dx, y + dy) == pxl.TRANSPARENT for dx, dy in N4):
                rep.add("WARN", name, "outline gap (fill touches transparent)", x, y, repr(ch))
            if all(at(g, x + dx, y + dy) == pxl.TRANSPARENT for dx, dy in N8):
                rep.add("WARN", name, "stray pixel", x, y, repr(ch))
            if (ch in outline and at(g, x + 1, y) in outline and at(g, x, y + 1) in outline
                    and at(g, x + 1, y + 1) in outline):
                # a 2x2 block of outline next to transparent = doubled outline
                block = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                if any(at(g, bx + dx, by + dy) == pxl.TRANSPARENT for bx, by in block for dx, dy in N4):
                    rep.add("WARN", name, "doubled outline (2x2 outline block)", x, y)


def runs(profile):
    """Group a list of (index, value) into runs of equal value -> [(start_index, value, length)]."""
    out = []
    for i, v in profile:
        if out and out[-1][1] == v and out[-1][0] + out[-1][2] == i:
            out[-1] = (out[-1][0], v, out[-1][2] + 1)
        else:
            out.append((i, v, 1))
    return out


def check_jaggies(name, g, rep):
    """Silhouette edges should step in an even rhythm: flag a run that is shorter or longer
    than both neighbours while the edge keeps moving the same way (e.g. 3,1,3 or 1,3,1)."""
    h, w = len(g), len(g[0])
    edges = {}
    rows = [y for y in range(h) if g[y].strip(pxl.TRANSPARENT)]
    cols = [x for x in range(w) if any(g[y][x] != pxl.TRANSPARENT for y in range(h))]
    edges["left"] = [(y, len(g[y]) - len(g[y].lstrip(pxl.TRANSPARENT))) for y in rows]
    edges["right"] = [(y, len(g[y].rstrip(pxl.TRANSPARENT)) - 1) for y in rows]
    col = lambda x: "".join(g[y][x] for y in range(h))
    edges["top"] = [(x, len(col(x)) - len(col(x).lstrip(pxl.TRANSPARENT))) for x in cols]
    for side, profile in edges.items():
        r = runs(profile)
        for i in range(1, len(r) - 1):
            a, b, c = r[i - 1], r[i], r[i + 1]
            if abs(b[1] - a[1]) != 1 or abs(c[1] - b[1]) != 1:
                continue  # only judge smooth 1px steps
            if (b[1] - a[1]) != (c[1] - b[1]):
                continue  # edge turns here, that's a corner not a jaggy
            # a long straight run (>= 4, e.g. a leg) between short steps is intentional
            if (b[2] < a[2] and b[2] < c[2] and min(a[2], c[2]) - b[2] >= 2) or \
               (b[2] > a[2] and b[2] > c[2] and b[2] - max(a[2], c[2]) >= 2 and b[2] < 4):
                idx = b[0]
                x, y = (b[1], idx) if side in ("left", "right") else (idx, b[1])
                rep.add("WARN", name, f"uneven curve step on {side} edge", x, y,
                        f"runs {a[2]},{b[2]},{c[2]}")


def changed_above_legs(g0, g1):
    """Pixels changed between a stand and a step frame above the leg zone, allowing a 0/1px bob."""
    b = bbox(g0)
    if not b:
        return 0, 0
    top, bottom = b[1], b[3]
    leg_top = bottom - max(3, (bottom - top + 1) * 3 // 10)
    best = None
    for bob in (0, 1, -1):
        diff = 0
        for y in range(top, leg_top):
            for x in range(len(g0[0])):
                if at(g0, x, y) != at(g1, x, y - bob):
                    diff += 1
        best = diff if best is None else min(best, diff)
    area = (leg_top - top) * (b[2] - b[0] + 1)
    return best, area


def lint(path, rep=None):
    rep = rep or Report()
    try:
        sp = pxl.load(path)
    except pxl.PxlError as e:
        rep.add("ERROR", "-", str(e))
        return rep, None

    if len(sp.palette) > 15:
        rep.add("ERROR", "-", f"{len(sp.palette)} colours; keep to 15 + transparent (GBA limit)")
    outline = sp.outline_letters()
    if sp.outline:
        for k in sp.outline:
            if k not in sp.palette:
                rep.add("ERROR", "-", f"outline letter '{k}' is not in the palette")
    for n in sp.defaulted:
        kind, src, _ = sp.derived[n]
        rep.add("INFO", n, f"filled in by default ({kind} {src})")
    for n in sp.missing:
        rep.add("INFO", n, "not drawn yet (renders blank)")

    used = set()
    names = []
    for n in sp.frame_names():
        if n in sp.frames:
            names.append(n)
    for n in names:
        g = sp.grid(n)
        used.update(ch for row in g for ch in row)
        if not bbox(g):
            rep.add("WARN", n, "frame is empty")
            continue
        check_pixels(n, g, outline, rep)
        check_jaggies(n, g, rep)
    unused = set(sp.palette) - used
    if unused:
        rep.add("INFO", "-", "unused colours: " + " ".join(sorted(unused)))

    # frames of one direction usually stand on the same row; a leap or a stepping foot
    # may move it, so this is only a note (refs/local/cat_ref lifts 3 rows mid-run)
    groups = defaultdict(dict)
    for n in sp.frame_names():
        b = bbox(sp.grid(n))
        if b:
            groups[n.rsplit("_", 1)[0]][n] = b[3]
    for base in groups.values():
        common = max(set(base.values()), key=list(base.values()).count)
        for n, y in base.items():
            if n in sp.frames and abs(y - common) > 1:
                rep.add("INFO", n, f"feet on row {y}, the rest of this direction stands on row {common}")

    # step frames should only move legs/arms and bob
    for d in pxl.DIRECTIONS:
        s0, s1 = f"{d}_0", f"{d}_1"
        if s0 in sp.frames and s1 in sp.frames:
            diff, area = changed_above_legs(sp.grid(s0), sp.grid(s1))
            if area and diff > area * 0.12:
                rep.add("INFO", s1, f"{diff} pixels differ from {s0} above the legs; "
                                    "step frames should mostly move legs/arms and bob 1px")
    return rep, sp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    a = ap.parse_args()
    rep, _ = lint(a.file)
    rep.print()
    if rep.count("ERROR") or (a.strict and rep.count("WARN")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

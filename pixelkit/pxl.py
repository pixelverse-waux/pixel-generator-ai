"""Read and write .pxl sprite files.

Format (one directive per line, ';' starts a comment line):

    name white_persian             optional, defaults to the file name
    size 32 32                 logical cell size
    scale 2                    output pixel scale (default 2)
    outline K k                letters that count as outline (default: darkest colour)
    footprint 4                objects only: bottom rows that block walkers (default: all)
    layout                     optional; rows of frame names, default is the 4x4 walk sheet
    down_0 down_1 down_2 down_3
    ...
    palette
    K #3a2418 outline          letter, hex colour, free-text note
    frame down_0
    ................           exactly <width> chars per row, '.' = transparent
    frame down_2 = copy down_0
    frame right_1 = mirror left_1
    frame up_2 = mirror up_0 shift -1   shift moves the result N columns (+ right, - left)

Frames left out of the file are filled in by walk-sheet defaults:
    X_2 = copy X_0, down_3 / up_3 = mirror of X_1, left_3 = copy left_1,
    right_N = mirror left_N.
"""
import os

TRANSPARENT = "."
DIRECTIONS = ["down", "left", "right", "up"]
DEFAULT_LAYOUT = [[f"{d}_{i}" for i in range(4)] for d in DIRECTIONS]


class PxlError(Exception):
    pass


class Sprite:
    def __init__(self):
        self.name = None
        self.width = 32
        self.height = 32
        self.scale = 2
        self.outline = None        # set of letters, None = darkest colour
        self.footprint = None      # rows at the bottom that block walkers, None = whole sprite
        self.layout = None
        self.palette = {}          # letter -> (r, g, b)
        self.notes = {}            # letter -> note
        self.frames = {}           # name -> list of row strings
        self.frame_notes = {}      # name -> comment written above the frame (e.g. source rect)
        self.derived = {}          # name -> ("copy" | "mirror", source, shift)
        self.defaulted = []        # frames filled in by walk-sheet defaults
        self.missing = []          # layout frames not drawn yet (rendered blank)

    # ---- frames -------------------------------------------------------
    def grid(self, name):
        """Rows of the frame, resolving copy/mirror references."""
        seen = set()
        steps = []
        while name in self.derived:
            if name in seen:
                raise PxlError(f"frame '{name}' refers to itself")
            seen.add(name)
            kind, src, shift = self.derived[name]
            steps.append((kind, shift))
            name = src
        if name not in self.frames:
            if name in self.missing:
                return [TRANSPARENT * self.width] * self.height
            raise PxlError(f"frame '{name}' is not defined")
        rows = self.frames[name]
        for kind, shift in reversed(steps):
            if kind == "mirror":
                rows = [r[::-1] for r in rows]
            if shift:
                pad = TRANSPARENT * abs(shift)
                rows = [(pad + r)[:self.width] if shift > 0 else (r + pad)[-self.width:] for r in rows]
        return rows

    def frame_names(self):
        return [n for row in self.sheet_layout() for n in row]

    def sheet_layout(self):
        return self.layout or DEFAULT_LAYOUT

    def outline_letters(self):
        if self.outline:
            return set(self.outline)
        if not self.palette:
            return set()
        return {min(self.palette, key=lambda k: sum(self.palette[k]))}

    def apply_defaults(self):
        if self.layout:
            return
        def have(n):
            return n in self.frames or n in self.derived
        rules = []
        for d in DIRECTIONS:
            rules.append((f"{d}_2", "copy", f"{d}_0"))
        rules += [("down_3", "mirror", "down_1"), ("up_3", "mirror", "up_1"),
                  ("left_3", "copy", "left_1")]
        rules += [(f"right_{i}", "mirror", f"left_{i}") for i in range(4)]
        for target, kind, src in rules:
            if not have(target) and have(src):
                self.derived[target] = (kind, src, 0)
                self.defaulted.append(target)


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) != 6:
        raise ValueError(h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(c):
    return "#%02x%02x%02x" % tuple(c[:3])


def load(path):
    sp = Sprite()
    sp.name = os.path.splitext(os.path.basename(path))[0]
    with open(path) as f:
        lines = f.read().splitlines()

    mode = None
    current = None
    for no, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        word = line.split()[0]

        def fail(msg):
            raise PxlError(f"{path}:{no}: {msg}")

        if word == "name":
            sp.name = line.split(None, 1)[1].strip()
            mode = None
        elif word == "size":
            parts = line.split()
            if len(parts) != 3:
                fail("size needs width and height")
            sp.width, sp.height = int(parts[1]), int(parts[2])
            mode = None
        elif word == "scale":
            sp.scale = int(line.split()[1])
            mode = None
        elif word == "outline":
            sp.outline = line.split()[1:]
            mode = None
        elif word == "footprint":
            sp.footprint = int(line.split()[1])
            mode = None
        elif word == "layout":
            sp.layout = []
            mode = "layout"
        elif word == "palette":
            mode = "palette"
        elif word == "frame":
            parts = line.split()
            if len(parts) == 2:
                current = parts[1]
                if current in sp.frames or current in sp.derived:
                    fail(f"frame '{current}' defined twice")
                sp.frames[current] = []
                mode = "frame"
            elif len(parts) in (5, 7) and parts[2] == "=" and parts[3] in ("copy", "mirror"):
                shift = 0
                if len(parts) == 7:
                    if parts[5] != "shift":
                        fail("expected 'frame NAME = copy|mirror SOURCE [shift N]'")
                    shift = int(parts[6])
                sp.derived[parts[1]] = (parts[3], parts[4], shift)
                mode = None
            else:
                fail("expected 'frame NAME' or 'frame NAME = copy|mirror SOURCE [shift N]'")
        elif mode == "layout":
            sp.layout.append(line.split())
        elif mode == "palette":
            parts = line.split(None, 2)
            if len(parts) < 2 or len(parts[0]) != 1 or parts[0] == TRANSPARENT:
                fail("palette lines look like 'K #3a2418 note' (one letter, not '.')")
            try:
                sp.palette[parts[0]] = hex_to_rgb(parts[1])
            except ValueError:
                fail(f"bad colour '{parts[1]}'")
            sp.notes[parts[0]] = parts[2] if len(parts) > 2 else ""
        elif mode == "frame":
            rows = sp.frames[current]
            if len(line) != sp.width:
                fail(f"frame '{current}' row {len(rows)} is {len(line)} wide, expected {sp.width}")
            for ch in line:
                if ch != TRANSPARENT and ch not in sp.palette:
                    fail(f"frame '{current}' row {len(rows)} uses '{ch}', not in palette")
            rows.append(line)
        else:
            fail(f"unexpected line: {line[:40]}")

    for name, rows in sp.frames.items():
        if len(rows) != sp.height:
            raise PxlError(f"{path}: frame '{name}' has {len(rows)} rows, expected {sp.height}")
    sp.apply_defaults()
    for name in sp.frame_names():
        try:
            sp.grid(name)
        except PxlError:
            # unfinished file: the frame (or the frame it copies) isn't drawn yet
            sp.missing.append(name)
    return sp


def dump(sp, path):
    out = [f"name {sp.name}", f"size {sp.width} {sp.height}", f"scale {sp.scale}"]
    if sp.outline:
        out.append("outline " + " ".join(sp.outline))
    if sp.footprint:
        out.append(f"footprint {sp.footprint}")
    if sp.layout:
        out.append("layout")
        out += [" ".join(r) for r in sp.layout]
    out.append("palette")
    for k, c in sp.palette.items():
        note = sp.notes.get(k, "")
        out.append(f"{k} {rgb_to_hex(c)} {note}".rstrip())
    for name, rows in sp.frames.items():
        out.append("")
        if sp.frame_notes.get(name):
            out.append(f"; {sp.frame_notes[name]}")
        out.append(f"frame {name}")
        out += rows
    for name, (kind, src, shift) in sp.derived.items():
        if name not in sp.defaulted:
            out.append(f"frame {name} = {kind} {src}" + (f" shift {shift}" if shift else ""))
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")

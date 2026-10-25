"""Convert a sprite image into .pxl text so it can be read pixel by pixel.

    python3 -m pixelkit.img2pxl character_sprite.jpg -o refs/local/trainer.pxl --cell 64x64 --scale 2
    python3 -m pixelkit.img2pxl refs/local/cat_ref.png -o refs/local/cat_ref/move.pxl --cell 32x32 --bg-all --rows 4,7,6,5 --names down,left,right,up

Sheet mode cuts the image into cells and names them with the walk-sheet layout
(down/left/right/up x 0..3) when the grid is 4x4, else r<row>_c<col>.
With --rows, only those sheet rows are kept, named by --names (e.g. --rows 20,22,23,21
--names down,left,right,up gives down_0.. left_0..); empty cells are dropped.
Crop mode turns one region into a single frame. Colours are reduced to at most
15 plus transparent; the darkest colour is marked as outline.

Tile sheets with a gap between cells: --gutter 1 (cells start at gutter + i*(cell+gutter)).

Object mode cuts every separate object (8-connected opaque pixels) out of a loose sheet,
in reading order, each padded bottom-centred into one shared cell. --crop limits it to a
region, --names names the objects in order, --gap merges objects closer than N px, --bg
sets the background colour when it isn't transparent or a corner colour:

    python3 -m pixelkit.img2pxl refs/local/interior_ref.png -o refs/local/interior_ref/beds.pxl --objects --crop 276,16,150,170
"""
import argparse
import os

from PIL import Image

from . import pxl

LETTERS = "KABCDEFGHIJLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
# symbols for big reference sheets (house art can use ~90 colours); never '.' or ';'
LETTERS += "!$%&*+-/:<=>?@^_~|{}[]()',`#"


def detect_bg(img):
    px = img.load()
    w, h = img.size
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    return max(set(corners), key=corners.count)


def close(a, b, tol):
    return sum((int(x) - int(y)) ** 2 for x, y in zip(a[:3], b[:3])) <= tol * tol


def downsample(img, scale):
    """Take the middle pixel of every scale x scale block (robust to JPEG edges)."""
    if scale == 1:
        return img
    w, h = img.size[0] // scale, img.size[1] // scale
    src = img.load()
    out = Image.new("RGBA", (w, h))
    dst = out.load()
    o = scale // 2
    for y in range(h):
        for x in range(w):
            dst[x, y] = src[x * scale + o, y * scale + o]
    return out


def pixels(img):
    return list(img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata())


def background_mask(cell, bg, tol, flood=True):
    """Background = transparent pixels plus bg-coloured pixels connected to the cell edge,
    so white eyes or highlights inside the sprite are kept. flood=False: every
    bg-coloured pixel is background (for clean PNGs with enclosed gaps)."""
    w, h = cell.size
    px = cell.load()

    def bgish(x, y):
        p = px[x, y]
        return p[3] < 128 or (bg[3] >= 128 and close(p, bg, tol))

    # transparent pixels are always background; opaque bg-coloured ones only if reachable from the edge
    if not flood:
        return [[bgish(x, y) for x in range(w)] for y in range(h)]
    mask = [[px[x, y][3] < 128 for x in range(w)] for y in range(h)]
    seen = [[False] * w for _ in range(h)]
    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while stack:
        x, y = stack.pop()
        if seen[y][x] or not bgish(x, y):
            continue
        seen[y][x] = True
        mask[y][x] = True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx]:
                stack.append((nx, ny))
    return mask


def to_letters(cells, bg, tol, max_colors, flood=True, colour_source=None):
    """cells: list of RGBA images. Returns palette dict and list of row-string grids.
    colour_source: optional image whose colours fix the letter assignment, so files
    cut from the same sheet share one palette."""
    masks = [background_mask(c, bg, tol, flood) for c in cells]

    colours = set()
    if colour_source is not None:
        m = background_mask(colour_source, bg, tol, flood=False)
        w = colour_source.size[0]
        for i, p in enumerate(pixels(colour_source)):
            if not m[i // w][i % w]:
                colours.add(p[:3])
    for c, m in zip(cells, masks):
        w = c.size[0]
        for i, p in enumerate(pixels(c)):
            if not m[i // w][i % w]:
                colours.add(p[:3])
    if not colours:
        return {}, [["." * c.size[0]] * c.size[1] for c in cells]

    max_colors = min(max_colors, len(LETTERS))
    if len(colours) <= max_colors:
        mapping = {c: c for c in colours}
    else:
        strip = Image.new("RGB", (len(colours), 1))
        strip.putdata(sorted(colours))
        q = strip.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
        pal = q.getpalette()
        idx = pixels(q)
        mapping = {c: tuple(pal[i * 3:i * 3 + 3]) for c, i in zip(sorted(colours), idx)}

    used = sorted(set(mapping.values()), key=lambda c: sum(c))
    letter = {c: LETTERS[i] for i, c in enumerate(used)}
    palette = {letter[c]: c for c in used}

    grids = []
    for cell, m in zip(cells, masks):
        px = cell.load()
        rows = []
        for y in range(cell.size[1]):
            rows.append("".join("." if m[y][x] else letter[mapping[px[x, y][:3]]]
                                for x in range(cell.size[0])))
        grids.append(rows)
    return palette, grids


def find_objects(img, bg, tol, gap=0, min_px=4):
    """Connected blobs of non-background pixels. Returns (bbox, pixel set) in reading order:
    objects are grouped into lines by their top edge, then sorted left to right."""
    w, h = img.size
    px = img.load()
    solid = [[not (px[x, y][3] < 128 or (bg[3] >= 128 and close(px[x, y], bg, tol)))
              for x in range(w)] for y in range(h)]
    seen = [[False] * w for _ in range(h)]
    r = gap + 1
    found = []
    for y in range(h):
        for x in range(w):
            if not solid[y][x] or seen[y][x]:
                continue
            seen[y][x] = True
            stack, pts = [(x, y)], []
            while stack:
                cx, cy = stack.pop()
                pts.append((cx, cy))
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and solid[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
            if len(pts) < min_px:
                continue
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            found.append(((min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1), set(pts)))
    found.sort(key=lambda o: o[0][1])
    lines = []
    for o in found:
        top, hh = o[0][1], o[0][3]
        if lines and top < lines[-1][0] + lines[-1][1] // 2:
            lines[-1][2].append(o)
        else:
            lines.append((top, hh, [o]))
    return [sorted(objs, key=lambda o: o[0][0]) for _, _, objs in lines]


def merge_objects(objs):
    """Join several (bbox, pixels) objects into one, e.g. a tap drawn apart from its bath."""
    pts = set().union(*(p for _, p in objs))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1), pts


def objects_sprite(img, rows, names, name, max_colors=15, origin=(0, 0)):
    """Build a Sprite from rows of (bbox, pixels) objects: one frame per object, padded
    bottom-centred into the largest object's size, its source rect kept as a comment."""
    objs = [o for row in rows for o in row]
    if not objs:
        raise SystemExit("no objects found")
    names = list(names or [])
    if len(names) > len(objs):
        raise SystemExit(f"{len(names)} names for {len(objs)} objects")
    names += [f"o{i}" for i in range(len(names), len(objs))]
    cw = max(b[2] for b, _ in objs)
    ch = max(b[3] for b, _ in objs)
    src = img.load()
    cells = []
    for (x, y, w, h), pts in objs:
        cell = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        dst = cell.load()
        ox, oy = (cw - w) // 2, ch - h
        for px_, py_ in pts:
            dst[px_ - x + ox, py_ - y + oy] = src[px_, py_]
        cells.append(cell)

    sp = pxl.Sprite()
    sp.name = name
    sp.scale = 1
    sp.width, sp.height = cw, ch
    sp.layout, i = [], 0
    for row in rows:
        sp.layout.append(names[i:i + len(row)])
        i += len(row)
    sp.frame_notes = {n: "src %d,%d %dx%d" % (b[0] + origin[0], b[1] + origin[1], b[2], b[3])
                      for n, (b, _) in zip(names, objs)}
    sp.palette, grids = to_letters(cells, (0, 0, 0, 0), 0, max_colors)
    sp.notes = {k: "" for k in sp.palette}
    if sp.palette:
        sp.notes["K"] = "outline (darkest)"
    sp.frames = dict(zip(names, grids))
    return sp


def convert(path, out, cell=None, scale=1, crop=None, tol=40, max_colors=15, name=None, flood=True,
            rows=None, row_names=None, gutter=0, objects=False, gap=0, min_px=4, bg=None,
            names=None):
    img = Image.open(path).convert("RGBA")
    if bg is None:
        bg = detect_bg(img)
    origin = (crop[0], crop[1]) if crop else (0, 0)
    if crop:
        x, y, w, h = crop
        img = img.crop((x, y, x + w, y + h))
    img = downsample(img, scale)

    sp = pxl.Sprite()
    sp.name = name or os.path.splitext(os.path.basename(out))[0]
    sp.scale = scale

    if objects:
        rows = find_objects(img, bg, tol, gap, min_px)
        sp = objects_sprite(img, rows, names, sp.name, max_colors, origin)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        pxl.dump(sp, out)
        return sp
    if crop or not cell:
        cells = [img]
        names = ["frame_0"]
        sp.layout = [names]
    else:
        cw, ch = cell[0] // scale, cell[1] // scale
        g = gutter
        ncols, nrows = (img.size[0] - g) // (cw + g), (img.size[1] - g) // (ch + g)
        cells, names = [], []
        sheet = nrows == 4 and ncols == 4 and not rows
        picked = rows if rows else list(range(nrows))
        sp.layout = []
        for i, r in enumerate(picked):
            row = []
            for c in range(ncols):
                x0, y0 = g + c * (cw + g), g + r * (ch + g)
                cell_img = img.crop((x0, y0, x0 + cw, y0 + ch))
                if rows and not cell_img.getbbox():
                    continue  # skip empty cells at the end of a picked row
                if sheet:
                    n = f"{pxl.DIRECTIONS[r]}_{c}"
                elif rows:
                    n = f"{row_names[i] if row_names else 'r%d' % r}_{c}"
                else:
                    n = f"r{r}_c{c}"
                cells.append(cell_img)
                names.append(n)
                row.append(n)
            sp.layout.append(row)
        if sheet:
            sp.layout = None  # default walk-sheet layout

    sp.width, sp.height = cells[0].size
    sp.palette, grids = to_letters(cells, bg, tol, max_colors, flood, img if rows else None)
    for k in sp.palette:
        sp.notes[k] = ""
    if sp.palette:
        sp.notes["K"] = "outline (darkest)"
    sp.frames = dict(zip(names, grids))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    pxl.dump(sp, out)
    return sp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--cell", help="cell size in source pixels, e.g. 64x64")
    ap.add_argument("--scale", type=int, default=1, help="source pixels per art pixel")
    ap.add_argument("--crop", help="x,y,w,h region in source pixels (single frame)")
    ap.add_argument("--tol", type=int, default=40, help="background colour tolerance")
    ap.add_argument("--colors", type=int, default=15,
                    help=f"max colours (up to {len(LETTERS)}; past 15 only for study refs)")
    ap.add_argument("--name")
    ap.add_argument("--rows", help="comma list of sheet rows to keep (needs --cell)")
    ap.add_argument("--names", help="comma list of frame-name prefixes, one per --rows entry")
    ap.add_argument("--bg-all", action="store_true",
                    help="treat every background-coloured pixel as transparent, even enclosed ones")
    ap.add_argument("--gutter", type=int, default=0, help="px between cells (and before the first)")
    ap.add_argument("--objects", action="store_true", help="cut each separate object into a frame")
    ap.add_argument("--gap", type=int, default=0, help="--objects: merge objects closer than N px")
    ap.add_argument("--min-px", type=int, default=4, help="--objects: drop specks smaller than this")
    ap.add_argument("--bg", help="background colour as #rrggbb (default: corner colour)")
    a = ap.parse_args()
    cell = tuple(int(v) for v in a.cell.lower().split("x")) if a.cell else None
    crop = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    rows = [int(v) for v in a.rows.split(",")] if a.rows else None
    row_names = a.names.split(",") if a.names else None
    if rows and row_names and len(rows) != len(row_names):
        raise SystemExit("--names needs one name per --rows entry")
    if a.objects and (cell or rows):
        raise SystemExit("--objects works on the whole image or a --crop, not with --cell/--rows")
    bg = pxl.hex_to_rgb(a.bg) + (255,) if a.bg else None
    sp = convert(a.image, a.out, cell, a.scale, crop, a.tol, a.colors, a.name, not a.bg_all,
                 None if a.objects else rows, None if a.objects else row_names, a.gutter,
                 a.objects, a.gap, a.min_px, bg, row_names if a.objects else None)
    print(f"wrote {a.out}: {len(sp.frames)} frame(s) {sp.width}x{sp.height}, {len(sp.palette)} colours")


if __name__ == "__main__":
    main()

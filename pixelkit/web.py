"""Export cats, dogs, characters, buildings and ground tiles for a website: one packed sprite atlas + one JSON each.

    python3 -m pixelkit.web                 everything -> web/cats/, web/dogs/, web/characters/, web/buildings/, web/tiles/
    python3 -m pixelkit.web ginger_tabby yellow_bomber   only these

Per animal it collects every action in sprites/<name>/*.pxl, plus the hand-drawn showcase walk
sprites/<name>.pxl (exported as action "walk") when it exists. Animals drawn bigger than 32x32
(dogs: 48x48) are dogs, the rest are cats. A character is one hand-drawn walk,
sprites/characters/<name>.pxl, exported as action "walk". A building is one file,
sprites/objects/<name>.pxl, with no animations: each of its frames (top_down, winter, ...)
becomes a pose of the same name; `footprint N` in the file (trees) exports as "footprint".
Ground tiles (sprites/tiles/<name>.pxl, 16x16) export the same way to web/tiles/, and the
inside of the house (sprites/interior/: room tiles, furniture, decor) to web/interior/.
Frames are kept at 1x (32x32 for
cats and people, 48x48 for dogs) and identical frames are stored once. The atlas is an indexed PNG with one transparent colour:
let the browser scale it with `image-rendering: pixelated`. index.json in each folder lists
the names.

JSON:
{
  "name": "ginger_tabby", "image": "ginger_tabby.png", "frameWidth": 32, "frameHeight": 32,
  "frames": [[x, y], ...],                          top-left of each frame in the atlas
  "animations": {"move/left": {"frames": [3, 4, ...], "fps": 10, "loop": true}, ...},
  "poses": {"sit": [12, 13, ...], ...}              single-frame stills (directions / poses)
}
"""
import argparse
import glob
import json
import os

from PIL import Image

from . import pxl

OUT = {"cats": os.path.join("web", "cats"), "dogs": os.path.join("web", "dogs"),
       "characters": os.path.join("web", "characters"), "buildings": os.path.join("web", "buildings"),
       "tiles": os.path.join("web", "tiles"), "interior": os.path.join("web", "interior")}
CHARACTERS = os.path.join("sprites", "characters")
OBJECTS = os.path.join("sprites", "objects")
TILES = os.path.join("sprites", "tiles")
INTERIOR = os.path.join("sprites", "interior")
COLUMNS = 16
CAT_SIZE = 32   # cat_ref frames are 32x32; dogs are bigger (48x48 since 2026-10-25, 64x64 dog_ref)

# how each cat_ref / dog_ref action plays; actions not listed are animations at 8 fps, looping
PLAY = {
    "walk": (8, True), "move": (10, True), "move_diag": (10, True),
    "idle_tail": (6, True), "idle_tail_diag": (6, True),
    "turn": (8, False), "turn_diag": (8, False),
    "blink": (8, False), "meow": (8, False), "groom": (8, True),
    "look": (6, True), "hiss": (4, True),
    "pant": (6, True), "sleep": (2, True),
}
POSES = {"idle", "sit", "lie"}   # rows of separate stills, not animations


def frame_pixels(sp, name):
    return tuple(tuple(sp.palette[ch] + (255,) if ch != pxl.TRANSPARENT else (0, 0, 0, 0)
                       for ch in row) for row in sp.grid(name))


def row_prefix(names, action):
    """The shared name of a sheet row ("down" for down_0 down_1 ...). A row of differently
    named stills (dog sit: down up left right tilt) is named after the action."""
    prefix = names[0].rsplit("_", 1)[0] if "_" in names[0] else names[0]
    if len(names) > 1 and not all(n.startswith(prefix + "_") for n in names):
        return action
    return prefix


def collect(cat, kind="cats"):
    """[(action, sprite)] for one cat or character."""
    if kind == "characters":
        return [("walk", pxl.load(os.path.join(CHARACTERS, f"{cat}.pxl")))]
    if kind == "buildings":
        return [("building", pxl.load(os.path.join(OBJECTS, f"{cat}.pxl")))]
    if kind == "tiles":
        return [("tiles", pxl.load(os.path.join(TILES, f"{cat}.pxl")))]
    if kind == "interior":
        return [("interior", pxl.load(os.path.join(INTERIOR, f"{cat}.pxl")))]
    out = []
    hero = os.path.join("sprites", f"{cat}.pxl")
    if os.path.exists(hero):
        out.append(("walk", pxl.load(hero)))
    for path in sorted(glob.glob(os.path.join("sprites", cat, "*.pxl"))):
        out.append((os.path.splitext(os.path.basename(path))[0], pxl.load(path)))
    return out


def export(cat, kind="cats"):
    sprites = collect(cat, kind)
    if not sprites:
        raise SystemExit(f"no sprites for '{cat}' (looked for sprites/{cat}.pxl and sprites/{cat}/*.pxl)")
    fw, fh = sprites[0][1].width, sprites[0][1].height
    unique, index = [], {}
    animations, poses = {}, {}

    def add(pixels):
        if pixels not in index:
            index[pixels] = len(unique)
            unique.append(pixels)
        return index[pixels]

    for action, sp in sprites:
        if (sp.width, sp.height) != (fw, fh):
            raise SystemExit(f"{cat}/{action}: frame size differs from the rest")
        for row in sp.sheet_layout():
            ids = [add(frame_pixels(sp, n)) for n in row]
            if kind in ("buildings", "tiles", "interior"):
                poses.update({n: [i] for n, i in zip(row, ids)})
                continue
            key = f"{action}/{row_prefix(row, action)}"
            if action in POSES:
                poses[key] = ids
            else:
                fps, loop = PLAY.get(action, (8, True))
                animations[key] = {"frames": ids, "fps": fps, "loop": loop}

    cols = min(COLUMNS, len(unique))
    rows = (len(unique) + cols - 1) // cols
    colours = sorted({p for fr in unique for row in fr for p in row if p[3]})
    if len(colours) > 255:
        raise SystemExit(f"{cat}: {len(colours)} colours, an indexed PNG holds 255 + transparent")
    lookup = {c: i + 1 for i, c in enumerate(colours)}
    atlas = Image.new("P", (cols * fw, rows * fh), 0)
    pal = [0, 0, 0] + [v for c in colours for v in c[:3]]
    atlas.putpalette(pal + [0] * (768 - len(pal)))
    px = atlas.load()
    frames = []
    for i, fr in enumerate(unique):
        ox, oy = (i % cols) * fw, (i // cols) * fh
        frames.append([ox, oy])
        for y, row in enumerate(fr):
            for x, p in enumerate(row):
                if p[3]:
                    px[ox + x, oy + y] = lookup[p]

    out = OUT[kind]
    os.makedirs(out, exist_ok=True)
    png = os.path.join(out, f"{cat}.png")
    atlas.save(png, optimize=True, transparency=0)
    meta = {"name": cat, "image": f"{cat}.png", "frameWidth": fw, "frameHeight": fh,
            "frames": frames, "animations": animations, "poses": poses}
    if kind == "buildings" and sprites[0][1].footprint:
        meta["footprint"] = sprites[0][1].footprint   # only these bottom rows block a walker
    with open(os.path.join(out, f"{cat}.json"), "w") as f:
        json.dump(meta, f, separators=(",", ":"))
    total = sum(len(sp.frame_names()) for _, sp in sprites)
    return {"name": cat, "frames": total, "unique": len(unique),
            "png_bytes": os.path.getsize(png), "animations": len(animations), "poses": len(poses)}


def all_animals():
    names = {os.path.basename(os.path.dirname(p)) for p in glob.glob("sprites/*/*.pxl")}
    names |= {os.path.splitext(os.path.basename(p))[0] for p in glob.glob("sprites/*.pxl")}
    names.discard("characters")
    names.discard("objects")   # buildings and trees: exported separately to web/buildings/
    names.discard("tiles")     # ground tiles: exported to web/tiles/
    names.discard("interior")  # room tiles, furniture, decor: exported to web/interior/
    return sorted(names)


def is_dog(name):
    sprites = collect(name)
    return bool(sprites) and sprites[0][1].width > CAT_SIZE


def all_characters():
    return sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(CHARACTERS, "*.pxl")))


def all_buildings():
    return sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(OBJECTS, "*.pxl")))


def all_tiles():
    return sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(TILES, "*.pxl")))


def all_interior():
    return sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(INTERIOR, "*.pxl")))


def write_index(kind, names, partial):
    idx = os.path.join(OUT[kind], "index.json")
    existing = []
    if os.path.exists(idx) and partial:
        existing = [n for n in json.load(open(idx)) if n not in names]
    os.makedirs(OUT[kind], exist_ok=True)
    with open(idx, "w") as f:
        json.dump(sorted(existing + names), f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="cats, dogs, characters and/or buildings (default: all)")
    a = ap.parse_args()
    characters = set(all_characters())
    buildings = set(all_buildings())
    tiles = set(all_tiles())
    interior = set(all_interior())
    picked = a.names or all_animals() + sorted(characters) + sorted(buildings) + sorted(tiles) + sorted(interior)
    animals = [n for n in picked if n not in characters | buildings | tiles | interior]
    dogs = {n for n in animals if is_dog(n)}
    groups = {"cats": [n for n in animals if n not in dogs],
              "dogs": [n for n in animals if n in dogs],
              "characters": [n for n in picked if n in characters],
              "buildings": [n for n in picked if n in buildings],
              "tiles": [n for n in picked if n in tiles],
              "interior": [n for n in picked if n in interior]}
    for kind, names in groups.items():
        if not names:
            continue
        stats = [export(n, kind) for n in names]
        write_index(kind, names, bool(a.names))
        for s in stats:
            print(f"{kind.rstrip('s'):<9} {s['name']:<14} {s['frames']:>4} frames -> {s['unique']:>4} unique, "
                  f"{s['animations']} animations, {s['poses']} pose sets, {s['png_bytes'] / 1024:.1f} KB png")


if __name__ == "__main__":
    main()

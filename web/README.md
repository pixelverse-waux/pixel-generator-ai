# Cat, dog and character sprites for the web

Copy this folder's `catsprite.js` plus `cats/`, `dogs/` and/or `characters/` into your site.
The demo site has six pages: `/` (overview), `/cats/`, `/dogs/`, `/characters/`, `/buildings/` and `/town/` (a walkable demo ground). The galleries use
`viewer.js` and `site.css`: pick a sprite, play any animation, see all four walk directions,
and walk it around a field with the arrow keys / WASD (touch buttons on phones). The URL hash
remembers the pick (`/characters/#yellow_bomber`).

| File | What |
|---|---|
| `cats/<cat>.png` | Sprite atlas: every frame at 1× (32×32), identical frames stored once, indexed PNG (~11–15 KB) |
| `cats/<cat>.json` | Frame positions, animations (fps, loop) and still poses (~5 KB) |
| `cats/index.json` | List of cat names |
| `dogs/<dog>.png`, `.json`, `index.json` | Same format for dogs, with 48×48 frames: `walk/*`, `pant/sit`, `pant/stand`, `sleep/*`; poses `sit/sit`, `lie/left`, `lie/right` |
| `characters/<name>.png`, `.json`, `index.json` | Same format for people: one `walk/*` set (down, left, right, up) |
| `buildings/<name>.png`, `.json`, `index.json` | Same format for top-down buildings (`sprites/objects/*.pxl`): no animations, one pose per frame (`top_down`, …). The page draws the building on grass and lets the first character walk around it; opaque building pixels block the character's feet. A tree's `footprint` (bottom rows, from `footprint N` in its `.pxl`) is all that blocks, and the character is drawn behind it when standing above its base |
| `tiles/<name>.png`, `.json`, `index.json` | 16×16 ground tiles from `sprites/tiles/*.pxl`, one pose per tile: `ground` (grass, dirt, cobble, grass-edge overlays, pebble and leaf decals), `fence` (horizontal, vertical, post) and `flowers` (red and yellow tulips, daisies, lavender, tall grass). `/town/` lays them out from a character map in its page script and draws houses, trees, bushes, fences, every exported cat and dog (wandering: walk, stand, sit, tail sway / pant) and the walker sorted by where they touch the ground |
| `interior/<name>.png`, `.json`, `index.json` | The inside of the White House, from `sprites/interior/*.pxl`: `room` (16×16 plank floors, wallpaper wall with trim / skirting, wall tops, door mat), `furniture` (bed, desk, table, chairs in 4 facings, bookshelf, sofa, lamp, plant; bottom-centred on 48×48 cells, placed by centre x + floor row) and `decor` (rug, window, painting; flat). `/town/` switches to this room when you walk up into the front door, and back when you step on the door mat |
| `catsprite.js` | Tiny player, no dependencies (~3 KB) |

## Use

```html
<canvas id="cat"></canvas>
<script src="catsprite.js"></script>
<script>
  CatSprite.load("cats/sphynx.json").then((cat) => {
    const player = cat.attach(document.getElementById("cat"), { scale: 4 });
    player.play("walk/left");                                   // loops
    // player.play("meow/sit", () => player.play("idle_tail/down")); // once, then idle
    // player.pose("sit/sit", 0);                               // a still
    // player.still("walk/left", 0);                            // hold one frame of an animation
  });
</script>
```

`Object.keys(cat.animations)` and `Object.keys(cat.poses)` list everything a cat has:

- `walk/*`: the cat's own hand-drawn walk (down, left, right, up). Not every cat has one.
- `move/*`, `move_diag/*`: the walk cycle in 4 and 4 diagonal directions.
- `idle_tail/*`, `turn/*`: standing idle with tail sway, turning around.
- `blink/*`, `meow/*`, `groom/*`, `look/*`, `hiss/*`: behaviours.
- Poses: `idle/idle` (8 directions), `sit/*`, `lie/lie`, `lie/sleep`.

Scale by whole numbers (2, 3, 4…) so pixels stay sharp. The player sets
`image-rendering: pixelated` for you. Use the atlas directly with CSS or a game engine by
reading `frames[i]` (top-left x, y) and `frameWidth`/`frameHeight` from the JSON.

Attaching a new cat to a canvas stops whatever was playing on it, so switching cats never mixes
two animations on one canvas.

## Preview

```bash
python3 -m http.server 8765 -d web
```

Then open http://localhost:8765 (or /cats/, /characters/). Browsers block `fetch` from `file://` pages, so the demo needs a server.

## Rebuild after changing a cat or character

```bash
python3 -m pixelkit.web
```

Cats and dogs come from `sprites/<name>.pxl` + `sprites/<name>/*.pxl` (a set drawn bigger than 32×32,
the 48×48 dogs, goes to `dogs/`); characters from
`sprites/characters/<name>.pxl`.

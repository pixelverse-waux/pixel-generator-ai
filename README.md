# Pixel generator

Hand-drawn, Pokémon-style top-down pixel art: cats, dogs, people, buildings, trees, plants,
ground tiles and furniture. Every sprite is a plain-text `.pxl` file drawn pixel by pixel.
A small Python toolkit (`pixelkit`) renders, checks and exports the sprites, and a static
demo site (`web/`) plays them, including a walkable town with a house you can go into.

## Quick start

Requirements: Python 3 and [Pillow](https://pypi.org/project/Pillow/) (`pip install pillow`).
Nothing else.

```bash
python3 -m pixelkit.web                    # export every sprite to web/
python3 -m http.server 8765 -d web         # then open http://localhost:8765
```

The demo has to be served over HTTP, because browsers block `fetch` from `file://` pages.

| Page | What it shows |
|---|---|
| `/` | overview |
| `/cats/`, `/dogs/`, `/characters/` | pick a sprite, play every animation, walk it around a field |
| `/buildings/` | buildings and trees; walk around them (trees only block at the trunk) |
| `/town/` | a walkable demo map: grass, roads, fences, flowers, the White House, trees, wandering cats and dogs. Walk up into the front door to go inside; the door mat takes you back out |

Controls: arrow keys or WASD (touch buttons on phones).

## How sprites are made

Sprites are drawn by hand in `.pxl` text, normally by Claude through the `/pixel-sprite` skill
(`.claude/skills/pixel-sprite/SKILL.md`):

1. Study the reference for the subject (`refs/local/*/INDEX.md`) and `style/STYLE_GUIDE.md`.
   References beat rules.
2. Write an identity card for the subject (build, coat, ears, hair, clothes, ...).
3. Draw the first frame, render it, lint it, then draw the rest of the frames.
4. Export to the web.

The tools never draw for you: they render, check, compare and export.

### The `.pxl` format

```text
name tulip
size 16 16                 canvas size (frames are all this size)
scale 2                    output scale for renders
outline K                  letters that count as outline
footprint 4                objects only: bottom rows that block a walker (trees)
layout                     optional: rows of frame names
red yellow
palette
K #1f3a24 stem outline     one letter per colour, with a note
R #c8364a petal
frame red
....KRK.....               one character per pixel, '.' = transparent
...
frame yellow = copy red    or: mirror SOURCE [shift N]
```

The full description is at the top of [`pixelkit/pxl.py`](pixelkit/pxl.py).

## Tools

All are run from the repo root as `python3 -m pixelkit.<tool>`.

| Tool | What it does | Example |
|---|---|---|
| `render` | sheet PNG, zoomed preview, walk GIF into `out/<name>/` | `python3 -m pixelkit.render sprites/sphynx.pxl` |
| `lint` | outline gaps, stray pixels, pinholes, doubled outlines, jaggies, too many colours | `python3 -m pixelkit.lint sprites/sphynx.pxl` |
| `compare` | reference photo, drawn frame and palette side by side (animals only, not people) | `python3 -m pixelkit.compare input/sphynx.webp sprites/sphynx.pxl` |
| `palette` | main colours of a photo, with suggested ramps | `python3 -m pixelkit.palette input/sphynx.webp` |
| `actions` | builds every cat_ref action for one cat from a coat file | `python3 -m pixelkit.actions sprites/siberian/coat.json --render` |
| `img2pxl` | turns a sprite sheet into `.pxl` text for study (grid, gutter or loose objects) | `python3 -m pixelkit.img2pxl sheet.png -o out.pxl --objects` |
| `rescale` | shrinks a sprite by dropping whole rows/columns, keeping 1-px outlines | `python3 -m pixelkit.rescale dog.pxl --to 48` |
| `web` | packs each sprite into a 1× indexed-PNG atlas + JSON for `web/` | `python3 -m pixelkit.web` |

## Folders

| Folder | Contents |
|---|---|
| `sprites/` | the drawings. `<cat>.pxl` (hand-drawn walk) + `<cat>/` (every action); `characters/` (people); `objects/` (buildings, trees, bushes); `tiles/` (16×16 ground, fences, flowers); `interior/` (room tiles, furniture, decor) |
| `input/` | reference photos for the sprites, named after the sprite |
| `refs/local/` | the user's private reference sheets, split into `.pxl` files with an `INDEX.md` each. See [Reference material](#reference-material) |
| `refs/cc0/` | CC0 reference sheets, each with a `SOURCE.txt` |
| `style/STYLE_GUIDE.md` | the drawing rules, summarised from the references |
| `pixelkit/` | the Python toolkit |
| `web/` | the demo site and the exported atlases (see `web/README.md` for embedding `catsprite.js` in your own site) |
| `out/` | renders (generated) |

## Sizes and conventions

Everything sits on one pixel grid at 1×. The 16×32 trainers are the yardstick.

| Kind | Canvas |
|---|---|
| People | 32×32 frame (body about 14×21) |
| Cats | 32×32, 4 directions, cat_ref timing |
| Dogs | **48×48** (3/4 of the 64×64 dog_ref), 6-frame walk |
| Ground tiles, flowers | 16×16 |
| Trees | 28–64 wide, 44–53 tall, with `footprint` so walkers pass behind the crown |
| Furniture | bottom-centred on 48×48 cells |

- Outlines are 1 px and use a dark shade of the material, not black, except on people.
- Colour and season variants are palette swaps of one drawing.
- Keep to 15 colours per sprite file. The study copies in `refs/local/` are the exception.
- **Never scale pixel art by a fraction** (for example 0.75× in a browser): it makes 1-px
  outlines uneven. Draw at the target size, or use `pixelkit.rescale` and fix the result by hand.

## Reference material

`refs/local/` holds the user's private study sheets: cats, dogs, trainers, walls and floors,
furniture, houses, trees, plants, ground and fences. `refs/local/SOURCE.txt` lists them.

- They are **study only**. No pixels are copied from them into new sprites, and they are never
  exported to `web/` or published.
- Some are commercial assets whose licences forbid redistribution. One example is the
  Flower & Plant Pack in `refs/local/plant_ref/`; its `LICENSE.txt` is kept alongside it.
- New references go in as CC0 material with a `SOURCE.txt` (`refs/cc0/`), or in `refs/local/`
  when the user supplies them.

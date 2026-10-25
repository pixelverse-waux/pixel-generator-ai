---
name: pixel-sprite
description: Draw a Pokémon-style top-down 4-direction walk sprite sheet by hand from a reference image (photo or drawing of an animal or person). Use when the user gives an image and asks for a sprite, pixel character, overworld sprite, or walk cycle, or runs /pixel-sprite <image> [name].
---

# /pixel-sprite <image> [name]

You draw every pixel yourself as text in a `.pxl` file. The tools in `pixelkit/` only render,
check and compare; they never draw for you.

Reference photos live in `input/` (e.g. `input/siberian.webp`). Save a new photo the user gives
into `input/` before starting, and use that path in every command below.

## 1. Study (every run)
1. Read `style/STYLE_GUIDE.md` in full. Section 0 matters most: **the references beat the rules**.
2. Look at the reference image and write an **identity card** in your message. For animals, cover
   every row of the identity table in the style guide: build, leg length, body length, coat, head,
   ears, eyes, tail, pattern. For people: build, height, hair, clothes, signature item. Next to each
   trait, say what it changes in the drawing compared with the reference skeleton. The motion comes
   from the reference; the shape must come from this subject.
3. Open the reference grids for the subject and read them as text:
   - cat: `refs/local/cat_ref/INDEX.md`, then `move.pxl` (every frame
     of the cycle you will draw) and `idle_tail.pxl`. These decide body shape, leg positions per
     frame, tail and behaviour. Follow them over the style guide.
   - dog: `refs/local/dog_ref/INDEX.md`, then `48/move.pxl` (6 frames per direction) and
     `48/idle.pxl`. Dog frames are `size 48 48` (3/4 of dog_ref, the user's dog size), so every
     row is 48 chars. Never scale a finished sprite by a fraction; use `pixelkit.rescale` (style
     guide 2b). Other four-legged animals: whichever
     of cat_ref / dog_ref is closer in build.
   - person: `refs/local/character_male_ref/INDEX.md` or `character_female_ref/INDEX.md` (whichever
     fits the subject), then `walk.pxl` (every frame) and `run.pxl`. `refs/cc0/julia/julia.pxl` as a
     second opinion.
   - tile, furniture, prop, building or tree: `refs/local/wall_floor_ref/`, `interior_ref/`,
     `house_ref/`, `tree_ref/`, `tree3_ref/` (seasons), `tree2_ref/` (designs, dead), `ground_ref/` + `ground_details_ref/`
     (fences, outdoor ground, scatter decals) or `plant_ref/`
     (flowers, grass, plants, bushes; commercial pack, never copy or export) (read its `INDEX.md`, then the closest file: e.g. `beds_dark.pxl` for a bed,
     `cabin_blue_summer.pxl` + `_winter.pxl` for a house). These are single frames, not walk
     cycles: match size on the 1× grid, view, outline colour and ramps (style guide 3b), keep to
     15 colours, and draw colour variants as extra frames of the same shape. Put them in
     `sprites/objects/<name>.pxl` with a `layout` block; give trees `footprint N` (bottom rows that
     block a walker, usually the trunk base) so the web page lets people walk behind the crown.
   Match proportions, poses and motion frame by frame; recolour and re-mark for the subject.
   Never paste reference rows unchanged.
4. `python3 -m pixelkit.palette <image>`: pick the subject's colours from its ramps and drop
   background ones. 15 colours max.

## 2. Draw `sprites/<name>.pxl`
People go in `sprites/characters/<name>.pxl` instead (so the web export lists them under
/characters); use that path in every command below.
Start the file like this (the format is described at the top of `pixelkit/pxl.py`):
```
name <name>
size 32 32
scale 2
outline K
palette
K #1c1218 outline
...
frame down_0
<32 rows of 32 chars, '.' = transparent>
```
Order of work, render and lint after each step:
1. **down_0** first. Block the silhouette at the reference's size and baseline, then colours
   and shading in the reference's roles, then the face. Run:
   `python3 -m pixelkit.render sprites/<name>.pxl --only down_0`, look at the PNG,
   `python3 -m pixelkit.lint sprites/<name>.pxl`, and (animals only)
   `python3 -m pixelkit.compare <image> sprites/<name>.pxl`. For people, don't make the
   photo / sprite / palette side-by-side image: the user doesn't want those for human characters.
   Check the colours against the photo by eye instead.
   Fix and repeat, at most 3 rounds, until it reads as the subject and lint has no WARN on down_0
   that the reference doesn't also have.
2. **left_0** and **up_0**, keeping the same head width, eye row, colours and baseline.
3. The motion frames. Animals: as many frames per direction as the reference cycle (cat move:
   4 down / 8 left / 4 up), with legs, body height and tail matching each reference frame;
   add a `layout` block. People: down_1, left_1, up_1 (and left_3) per the trainer walk.
4. Right-facing frames: `frame right_N = mirror left_N`. Leave other defaults or write explicit
   `frame X = copy|mirror Y` lines.

Edit the `.pxl` with the Edit tool, one frame at a time. Count columns carefully: every row must be
exactly 32 chars, and the parser tells you the line number when one isn't.

## 3. Finish
1. `python3 -m pixelkit.lint sprites/<name>.pxl`: 0 errors. Fix the warnings, or list the ones
   left on purpose because the reference does the same (whiskers, gaps between legs).
2. `python3 -m pixelkit.render sprites/<name>.pxl` and `--silhouette`; view the preview and the
   silhouette next to the reference's silhouette (`python3 -m pixelkit.render refs/local/cat_ref/move.pxl --silhouette`).
   The subject's identity (build, coat, ears, tail) must show in the silhouette alone.
3. Send `out/<name>/<name>.png` and `out/<name>/<name>_walk.gif` to the user (every sprite gets its own folder in `out/`). Say what you kept from the
   reference, what you simplified, and any warnings you left.

## Every animation for a cat (sit, lie, meow, groom, ...)
The hand-drawn sheet above is the cat's showcase walk. For all 14 cat_ref actions (about 300
frames), describe the cat in `sprites/<cat>/coat.json` and build:
```
python3 -m pixelkit.actions sprites/<cat>/coat.json --render
```
- `palette` recolours the reference letter roles (K A B C D E F G); `extra` adds marking colours.
- `markings` paints white muzzle/chest/legs, forehead M, back bars, face mask, eye colour and
  wrinkles on every frame, anchored to the nose and the back highlight.
- `shape` changes the body in every pose: `ears` (taller, where the inner ear shows) and `fluff`
  (long-fur tufts on the outline).
- Output: `sprites/<cat>/<action>.pxl` and `out/<cat>/` (+ `<cat>_all_actions.png`).
Check the overview and lint (outline gaps must be 0). Fix a whole cat by editing its coat file and
rebuilding, not by editing the generated `.pxl` files. Examples: `sprites/ginger_tabby/coat.json`
(bicolour tabby), `sprites/sphynx/coat.json` (ears, mask, wrinkles), `sprites/siberian/coat.json`
(heavy fluff). Body changes it can't express (chunky body, bushy tail) are only in the hand-drawn
sheet.

## Export for a website
```
python3 -m pixelkit.web            # cats -> web/cats/, dogs (48x48) -> web/dogs/, people -> web/characters/, sprites/objects -> web/buildings/, sprites/tiles -> web/tiles/ and sprites/interior -> web/interior/ (both used by /town/)
```
One packed 1× indexed-PNG atlas plus JSON (frames, animations with fps/loop, poses) per cat.
The hand-drawn sheet becomes `walk/*`. `web/catsprite.js` plays them, `web/index.html` is the demo,
and `web/README.md` explains how to embed. Re-run the export after changing any cat.

## Rules
- Never write a script that generates the hand-drawn sheet. Its `.pxl` text is the drawing.
  `pixelkit.actions` is the one exception, for the full action set, and it only recolours and
  marks cat_ref's poses.
- The tools in `pixelkit/` may be improved, but stay within Python + Pillow.
- Files in `refs/local/` are the user's private references: study only, never copy pixels.

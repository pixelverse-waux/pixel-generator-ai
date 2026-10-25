# Top-down sprite guide

## 0. References beat rules
The reference sheets are the authority. This guide only summarises them and fills gaps.
When the guide and a reference disagree, **do what the reference does**.
- **Cats:** `refs/local/cat_ref/` (index in `INDEX.md`) decides proportions, the walk/run
  cycle, idles and behaviours.
- **Dogs:** `refs/local/dog_ref/` (index in `INDEX.md`) does the same for dogs (drawn on a 48×48 frame from its `48/` copy),
  6-frame walk, jump, leap, play bow, sniff, scratch, pant, bark, sleep. Section 2b.
- **Other four-legged animals:** whichever of the two is closer in build.
- **People:** `refs/local/character_male_ref/` and `refs/local/character_female_ref/` (Pokémon
  Ruby/Sapphire Brendan and May, index in each `INDEX.md`) decide proportions and the walk/run
  cycle. `refs/cc0/julia/julia.pxl` is a second opinion.
- **Walls and floors:** `refs/local/wall_floor_ref/` (32×32 tiles). **Furniture and props:**
  `refs/local/interior_ref/`. **Building exteriors** (summer + winter): `refs/local/house_ref/`.
  **Trees:** `refs/local/tree_ref/` (big), `tree3_ref/` (15 species × 4 seasons, character
  scale) and `tree2_ref/` (3 designs per species, dead, dead in winter). **Flowers, grass, small
  plants and bushes:** `refs/local/plant_ref/` (16-px tile grid, 4 seasons, 7 colours, sway).
  **Outdoor ground and fences:** `refs/local/ground_ref/` (fence + ground only) and
  `refs/local/ground_details_ref/` (pebble / leaf decals).
  Each has an `INDEX.md`; section 3b summarises them.

`pixelkit.lint` is advisory. The cat reference itself gets about 36 warnings (whisker pixels,
gaps between legs), so a warning that matches what the reference does is fine.

## 1. Canvas
- One frame = **32×32** logical pixels, output at 2× (`scale 2`), transparent background.
- Sheet rows: **down, left, right, up**. Frame counts follow the reference for the action
  (cat move cycle: 4 down / 8 left / 8 right / 4 up). Write an explicit `layout` block when it
  isn't the default 4×4. Right-facing frames can be `mirror` of left-facing ones.
- Keep one baseline per direction, except where the reference moves it (the run leap lifts the
  feet 3 rows).
- A cat with several actions gets a folder: `sprites/<cat>/<action>.pxl`, named after the
  cat_ref file it follows (`move`, `idle_tail`, `sit`, ...). Renders go to `out/<cat>/`.
  `python3 -m pixelkit.actions sprites/<cat>/coat.json --render` builds all 14 from the cat's
  coat file (colours, markings, ears, fluff). See `sprites/ginger_tabby/coat.json`.

## 2. Cats (from `refs/local/cat_ref/`)
Realistic, slim cat, **not chibi**. Measured from `move.pxl` and `idle_tail.pxl`:

| View | Size | Notes |
|---|---|---|
| Side | ~22 wide × 18 tall (cols 5–26, rows 7–24 standing) | head ~8×7 at the front, body ~14 long, tail rises from the rump 6–8 rows |
| Front (down) | ~13 wide × 25 tall (cols 9–21, rows 2–27) | tail stands up behind the head (2 px wide, rows 2–9), head ~11 wide, body narrow |
| Back (up) | same width as front | tail curls up over the back |

- **Head:** small and angular, not round. Ears are 2–3 px triangles with 1 px inner ear (E).
  Front face: two 1 px dark eyes 4 px apart on the same row, 1 px nose (D) under the middle,
  no mouth while idle. Side face: one eye pixel, nose (D) on the front edge.
- **Whiskers:** front view: an extra outline pixel sticking out on each side of the cheeks
  for 2–3 rows (it looks like a doubled outline). Side view: a lone dark pixel just below or
  in front of the muzzle. Both are meant to be there, even though lint flags them.
- **Legs:** thin, 1–2 px of fur inside a 1 px outline, 5–6 rows long. Far legs are drawn
  entirely in the shade colour (A), near legs in base (B), so depth reads without extra lines.
  Paws are just the leg end; there are no white paws unless the cat has them.
- **Tail:** 2 px wide, long, an S-curve or straight up, shaded on the underside.
- **Fur shading (3 tones):** base B everywhere, light C as a single stripe along the top of
  the back, shade A on the belly, rump, far legs and under the tail. Light comes from above.
- **Outline:** one near-black colour (#120e14-like) everywhere, outer and inner; inner lines
  separate the near legs from the body. No selective or coloured outlines.
- **Palette:** ~8 colours total (outline, 3 fur tones, nose, inner ear, plus mouth/eye glint
  for meow/blink). Swap the fur tones for the subject's colours. Keep the outline, and keep
  the same three roles (base / back light / underside shade).
- **Markings** (white chest, stripes, patches): add them as extra colours on top of the 3
  tones, following the same light/shade logic.

### Every cat is its own shape (identity)
cat_ref gives the **motion** (which frame has which leg where, bob, tail sway). It does not give
the **body**: a Persian, a Sphynx and a chubby tabby must not share one silhouette. Before drawing,
write an identity card from the photo, then change the cat_ref body to fit it in every frame.
Keep the leg timing.

| Trait | Look for | What to change vs cat_ref |
|---|---|---|
| Build | thin / normal / chunky / fat | thin: belly 1 row higher (legs look longer), neck visible, front view 1–2 px narrower. Chunky/fat: body 2–3 rows deeper with a round hanging belly, front view 2–4 px wider, legs 1–2 rows shorter |
| Leg length | long / normal / short (cobby, munchkin) | add or remove rows from every leg; keep the feet on one baseline |
| Body length | compact / normal / long (oriental) | side body ±2–3 px; move the hind legs with it |
| Coat | hairless / short / long / very fluffy | hairless: smooth outline, 1 px wrinkle dashes in the shade colour, no whiskers. Short: as cat_ref. Long: 1 px fur tufts notched into the outline every 3–4 px, chest ruff, fluffy cheeks, britches on the hind legs |
| Head | round / wedge / flat face / big cheeks | flat face: muzzle 1 px shorter in side view; wedge: head 1 px longer, narrower jaw |
| Ears | small / normal / huge / folded / tufted | huge (Sphynx): 2–3 rows taller and wider, flared out. Folded (Scottish fold): flat caps. Tufted: a pale tip pixel |
| Eyes | colour, size | big eyes: 2 px wide; keep the eye on the same row in every view |
| Tail | thin whip / normal / bushy / short / curled | thin: 1 px fill. Bushy: 3–4 px with tufts. Bob: 3–4 rows only |
| Pattern | solid, tabby, points, bicolour, calico | tabby: M forehead, back bands, leg bars, tail rings. Points: darker face, ears, paws, tail |

After drawing, run `render --silhouette` next to `out/cat_move/cat_move_silhouette.png`. If you could swap
the two silhouettes, you haven't shown the cat's identity yet.

### How a cat moves (`move.pxl`)
- **Side, 8 frames:** a full gait cycle. The legs pass, reach, stretch fully (frame 2:
  front legs forward, hind legs back, body lowered and long), gather (frame 6: legs bunched
  under the body), then repeat. The head stays level and the tail sways gently. Copy the leg
  positions frame by frame and change only the colours and markings.
- **Front/back, 4 frames:** the legs alternate long/short. On frames 1 and 3 the whole body
  sits **1 px lower**; the tail stays up.
- **Diagonals:** `move_diag.pxl`, 6 frames.

### How a cat behaves
Use the matching file in `refs/local/cat_ref/` (see `INDEX.md`): standing idle with tail
sway (`idle_tail`), sit, lie/loaf/sleep, blink, meow, groom, look around, hiss, turn.
While idle the legs stay locked; only the head, tail and eyes move.

## 2b. Dogs (from `refs/local/dog_ref/`)
Realistic short-coated dog, **not chibi**, bigger than a cat but smaller than a person. `refs/local/dog_ref/INDEX.md`
has the measurements and the per-frame notes; the main points:
- **Canvas: `size 48 48`** (the user's chosen dog size, 2026-10-25): 3/4 of dog_ref's 64×64. Follow
  `refs/local/dog_ref/48/` frame by frame (dog_ref shrunk to 48 with 1-px outlines kept). Standing
  side 32×26 with feet on row 35; front 16×29, feet on row 38; sit front 18×25; lying 32×19.
- **Never scale a sprite by a fraction** (in the browser or anywhere): 0.75× makes 1-px outlines
  uneven (some 1 px, some 2 px). Draw at the target size, or shrink an existing drawing with
  `python3 -m pixelkit.rescale <file> --to 48 --phase X,Y` (drops whole rows/columns, keeps
  outlines 1 px, closes gaps), use the same phase for every action of one animal, then lint and
  fix the face (eyes merge into the ear line most often) and any 2×2 outline blocks by hand.
- **Head:** floppy ears hanging out to the sides of the skull, pale blaze down the forehead into
  the muzzle, nose 2 px (B), eyes K with a 1 px glint (H). Mouth only shows when panting/barking (D).
- **Legs:** 3 px wide at 48 (4 in dog_ref at 64), 2-row sock at the foot (G over F). Near legs outlined in K. In motion, far
  legs, tail and rump are outlined in a second dark (A, navy-black) and filled base/shade, so they
  sit behind. This is a selective outline and it is meant to be there.
- **Fur (3 tones + light marking):** base E, shade C inside legs and under the tail, light F on
  brows and paw tips, marking G on blaze, chest, socks and tail tip.
- **Walk:** 6 frames per direction; trot with diagonal pairs; back bobs 1 px; tail sways, hangs low.
  Right = mirror of left in every action.
- **Identity:** as with cats, dog_ref gives the motion, not the breed. Change ears (prick / floppy
  / folded), muzzle length, leg length, coat (feathering, curls, wire), tail (curled, docked, plume)
  and size to fit the subject, keeping the leg timing.

## 3. People (from `refs/local/character_male_ref/` and `character_female_ref/`)
- The references are 16×32 cells: body 14 wide × 20–21 tall, head + hat/hair ≈ 55% of the
  height, feet on the bottom row of the stand frame (row 30). In a 32×32 frame, centre that
  body horizontally and keep the feet on row 30.
- Walk: stand → step A → stand → step B. Step frames drop the **whole sprite 1 px** (the stand
  frame is the high point), one foot reaches the row below, and the arm swings opposite the leg.
- Run: same 4 beats, body leans forward 1 px and the stride is wider (up to 16 wide).
- Right = mirror of left in the girl sheet; anything asymmetric (hair tails, bag strap) flips.
- Outline: black `#000000`, 1 px, all round; interior lines use the darkest shade of the material.
- 3–4 tones per material (skin 3, hair 3, clothes 3 + highlight), light from the top-left.
  14–15 colours per character.

## 3b. Tiles, furniture and buildings (from `wall_floor_ref/`, `interior_ref/`, `house_ref/`)
Everything is 1×, on the same pixel grid as the 16×32 trainers: a door is ~23–26×35, a chair
16×25, a bed 30 or 38 × 50, a log cabin 158×165.
- **Walls** are 32×32 tiles, 3 high: `top` (wood trim + 1 px shadow), `mid` (repeatable), then
  `skirting` or `wainscot`. Wallpaper is one flat colour with a few 1 px specks; stripes and
  planks are 1 px darker lines. The trim is the same wood on every wall.
- **Floors** are 32×32 tiles that wrap: checker (15 px squares, 1 px grout, 1 px bevel), bricks
  16×8 offset by half, parquet 8×8 basket weave, plain carpet = base + sparse 1 px dots.
- **Furniture** is top-down 3/4: a lighter top slab seen from above, a darker front face,
  2–3 px leg stubs. Light comes from above. Chairs need 4 facings (`_s _n _w _e`), sofas front,
  back and side.
- **Buildings** are front-on with the roof as the biggest mass (3/4 of a cabin's height), roof
  edges stepping 3 across per 2 down, left slope one step lighter than the right (light from the
  left). Logs, plaster infill, framed blue windows with one glint streak, plank door, steps and
  a flagstone foundation. **Winter** = the same silhouette with snow painted on: white wedges on
  shingles, white ridge, icicles under the eaves, caps on sills, beams and steps.
- **Outlines are coloured**: 1 px, a dark shade of each material (wood `#61381b`, roof
  `#2a4d66`), never black; only metal/electronics go near-black.
- **Colour variants are palette swaps**: one drawing, recoloured (6 bed colours, 3 sofa
  colours, dark/light wood sets, 3 roof colours). Draw the shape once, then add palettes.
- **Trees** (`tree_ref/`): 46–48 wide, 75–90 tall at 1×; crown ~2/3 of the height, trunk 6–8
  wide flaring to 8–12 at the roots. Leafy crowns are overlapping 8–12 px clumps, each lit on
  top and dark underneath, with a ragged edge and a darkest band at the bottom; pines are 6–7
  drooping tiers under a 1-px tip. Outline = darkest leaf / bark shade, 4–5 greens.
  Beside 16×32 people use the `tree3_ref` scale (18–42 wide, 26–57 tall, trunk splitting into
  3–5 roots). **Seasons repaint one silhouette**: spring adds blossom dots, autumn swaps the
  leaf ramp to orange/gold, winter turns each clump's upper half to snow; dead trees replace
  the crown with Y-forking branches (winter: 1 px snow on top of each branch).
- **Flowers, grass, plants, bushes** (`plant_ref/`): canvases are whole 16×16 tiles (32×32,
  32×48, 48×48) with the art bottom-aligned on the last row and centred; outline = the two
  darkest leaf steps (petals: their own dark step); colour / season variants are palette swaps
  of one drawing; a small version is redrawn at half size, not downscaled. Wind sway = 12-frame
  sine loop, bottom third still, top ±2 px.
- **Fences** (`ground_ref/fence_*`): 16×16 tiles, two 5-px posts per tile 8 px apart, a 3-row
  steel-blue rail at rows 6–8, and a separate 35 % shadow ring at each post's foot.
- **Outdoor ground** (`ground_ref/`): grass, dirt, cobble and sand patches are flat in the middle
  and detailed only at the edge (grass: lit tufts + dark-green outline; dirt: dark rim; cobble:
  3 colours, ragged stone edge, no outline). Break up flat ground with `ground_details_ref`
  decals: 1-colour pebble clusters and 2–3-green leaf sprigs, no outline, scattered loosely.
- **Short ramps**: 3–4 values per material plus its outline. The reference files hold up to
  ~90 colours because of near-duplicate noise; don't copy that. Merge it into the ramp and stay
  within 15 colours per sprite file.

## 4. General pixel craft
- 1 px outlines, never doubled (except where the reference does it between overlapping legs).
- Curves step evenly (1,1,2,3 not 3,1,3); no unintended stray pixels or pinholes.
- No anti-aliasing against the background.
- Keep the subject's real colours and markings from the photo; push contrast a little.

## 5. Before calling a sprite done
1. `python3 -m pixelkit.lint <file>`: no ERROR. Fix warnings unless the reference does the same.
2. `python3 -m pixelkit.render <file>` and `--silhouette`: check the preview, silhouette and GIF.
3. Put your frame next to the matching reference frame (same action, same direction) and
   compare size, leg positions and tail. They should line up.
4. Animals: `python3 -m pixelkit.compare <photo> <file>`: colours and markings match the photo.
   People: no compare image (the user doesn't want photo / sprite side-by-sides for humans).

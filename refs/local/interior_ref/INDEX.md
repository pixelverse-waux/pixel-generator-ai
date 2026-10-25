# interior_ref.png: what each file is

Source: `refs/local/interior_ref.png`, 448×853, **1×**, transparent background, objects laid out
loosely (no fixed grid). 297 separate objects, all of them used below.
The user's private reference: study only, don't copy pixels.
This is **the authority on furniture and indoor props**. Every `.pxl` here pastes back onto the
sheet with 0 pixels different. Each frame is the object cut out alone and padded
**bottom-centred** into the file's cell; the `; src x,y wxh` comment above it is the object's
rect on the sheet. Palettes are per file and keep every source colour (the sheet has 629, with
many near-duplicates), so they break the 15-colour lint rule on purpose.

The sheet has two wood sets with the same layout: the top block (y 16–235) is **dark wood**, the
block below it (y 240–460) is **light wood**. `*_dark` / `*_light` files hold the same frame
names; the light set is the same drawing recoloured (identical silhouettes frame for frame;
the wood ramp changes, and in a few frames a shade is split into two).

| File | Frames (size w×h) |
|---|---|
| `kitchen_dark/_light.pxl` | `sink_0..3` (20–21×29, counter with tap), `cupboard_0..3` (20–21×25), `drawers_0..3`; modules sit side by side into a kitchen run |
| `storage_dark/_light.pxl` | `drawers_small cupboard_narrow nightstand cupboard_small shelf_top shelf_bottom` (15–21×13–24), `sideboard_0..3` (31–32×25), `dresser` 42×48, `cabinet_side` 17×52, `hutch` 33×48, `bookshelf` 25×52, `bookshelf_wide` 42×52 |
| `doors_dark/_light.pxl` | `door_glass door_panel` 23×37 |
| `tables_dark/_light.pxl` | `desk_corner_0/1` 29×37, `desk` 34×26, `vanity` 34×43 (oval mirror), `computer_desk` 34×32, `table_long_l/m/r` 16×11–13 (a long table built from end + middle + end pieces), `table` 46×27, `table_tall` 22×46, `table_small` 34×24, `table_big` 46×26, `bench` 33×18, `side_table` 15×24, `chess_table` 17×21 |
| `seating_dark/_light.pxl` | `stool` 17×18, `chair_w chair_s chair_n chair_e` 16×25 (4 facings), `barstool_*` 11×19 in green, taupe, olive, grey, red, blue |
| `beds_dark/_light.pxl` | `<colour>_single` 30×50 and `<colour>_double` 38×50 for green, red, pink, orange, coral, blue |
| `lamps_dark/_light.pxl` | `lamp_yellow lamp_cream` 16×50 floor lamps |
| `misc_dark.pxl` | `fireplace` 31×46, `box_big` 25×17, `box_small` 16×17, `chest_low` 25×17, `clock` 17×17 (dark set only) |
| `appliances.pxl` | `tv_crt` 19×32, `tv_small` 19×30, `stove` 21×27, `fridge` 24×45 (light set only) |
| `sofas.pxl` | rows olive / orange / grey: `sofa` 53×33–36, `chair_e chair_w` 27×33–36, `chair` 29–32×33–36, `sofa_back` 57×36, `chair_back` 33×36, `sofa_side` 28×59 |
| `windows.pxl` | `window_4pane` 23×26, `window_double` 30×25, `window_tall` 25×30, `window_small` 24×18, `picture_0..2` 11×15, `mirror` 20×20 |
| `bathroom.pxl` | `bathtub_top` 27×51 (tap merged in), `bathtub_side` 40×24, `toilet_side` 22×24, `toilet_front` 11×24, `vent` 16×14, `basin_pedestal` 17×24, `basin` 17×17, `cabinet_white` 19×23, `wardrobe_white` 22×40, `shelf_white` 21×25 |
| `rugs.pxl` | `mat_<colour>` 32×16, `oval_s_<colour>` 21×13, `oval_l_<colour>` 35×21, `oval_red oval_orange` 35×21, `rug_checker` 26×16, `rug_stripe` 32×16 |
| `rugs_large.pxl` | `olive purple sage taupe` 74×51, fringed both ends |
| `curtain_panels.pxl` | `<colour>_l/_r` 16×34 and `<colour>_short_l/_r` 12×26 for blue, sage, red, yellow, green, peach; `_r` is the exact mirror of `_l` |
| `curtain_pairs.pxl` | `<colour>_wide` 45×34 and `<colour>_narrow` 32–33×26: two tied-back panels on a rod with knob ends |
| `items_jars.pxl` | `jar_0..6` 6×9, `flask_0..4` 7×11, `label_jar_0..4` 8×14 |
| `items_potions.pxl` | `vial_0..7` 4×9, `potion_0..7` 6×9 |
| `items_pots.pxl` | `pot_0..4` 8×13, `bottle_small` 4×7, `box_tiny` 7×8 |
| `chests_plants_keys.pxl` | `chest_blue/green/red/gold` 17×12, `flower_pot` 7×17, `cactus` 11×24, `blue_flower` 9×18, `key_0..3` 4×9 |

## How furniture is drawn
- **View**: top-down 3/4, the same camera as the people. Every piece shows its **top surface**
  (a slab seen from above, often 1 px wider than the body on each side, 8–12 rows deep) and its
  **front face** below it; legs are short 2–3 px stubs at the bottom corners.
- **Outline**: 1 px, **a dark shade of the object's own colour**, never black. Dark wood
  `#61381b`, light wood `#866847`, olive sofa `#6c5819`, grey sofa `#4e4639`, red rug `#8e484b`.
  Only metal / electronics use a near-black (`#2c2c2c` on the fridge).
- **Light from above**: tops are the lightest values, fronts a step darker, the band under a
  top or a cushion a 1 px shadow line. Wood has faint 1-px grain streaks, not dithering.
- **Ramps are short**: a material is 3–4 values plus the outline (dark wood `#61381b`,
  `#ac5f1b`, `#b46e31`, light wood `#866847`, `#cc9e6c`, `#f2bb80`). Rugs and curtains use
  only 3 colours. The many near-duplicate colours in the files are source noise; when drawing,
  merge them into the ramp.
- **Facings**: chairs come in 4 facings (`_s` seat towards the viewer, back above it; `_n` back
  in front with spindles over the seat; `_w`/`_e` side view with the back on the far side).
  Armchairs come front, back and both sides; sofas front, back and one side view.
- **Variants are palette swaps**: beds, sofas, barstools, rugs and curtains repeat one drawing
  in several colours; dark/light wood repeat the whole furniture set. Draw one shape, then
  recolour.
- **Beds**: headboard with two round-topped posts at the top, grey-blue pillow with its own dark
  outline, blanket covering the lower 2/3 with a lighter rim round a flat middle, footboard and legs at the
  bottom. Single 30 wide, double 38, both 50 tall.
- **Modules**: kitchen pieces (`sink_*`, `cupboard_*`, `drawers_*`) and `table_long_l/m/r` are
  built to butt together edge to edge into longer runs.

## Scale
1×, the same pixel size as the 16×32 trainers and the 32×32 tiles in `../wall_floor_ref/`.
A door is 23×37 (a 21-px trainer fits with room), a chair 16×25, a bed 50 tall (~1.5 tiles),
a sofa 53 wide.

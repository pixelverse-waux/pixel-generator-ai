# wall_floor_ref.png: what each file is

Source: `refs/local/wall_floor_ref.png`, 397×232, **32×32 tiles at 1×** on a 1 px transparent
gutter (tile *c*, row *r* starts at `1 + 33c, 1 + 33r`), 12 columns × 7 rows (the last row has 4).
The user's private reference: study only, don't copy pixels.
This is **the authority on interior walls and floors**. Every `.pxl` here pastes back onto the
sheet with 0 pixels different; each frame has a `; src x,y wxh` comment with its source rect.
Palettes are per file and keep every source colour (up to 33), so they break the 15-colour lint
rule on purpose: these are study copies, not sprites.

## Files

| File | Frames | What it is |
|---|---|---|
| `wall_00_wood_boards.pxl` … `wall_11_cream_stripe.pxl` | `top mid skirting wainscot` (stacked, 1 per layout row) | one wall style per sheet column: 00 wood boards (short staggered planks), 01 wood planks (vertical), 02 pink, 03 blue, 04 starry (navy + yellow dots), 05 red stripe, 06 peach, 07 orange, 08 lavender, 09 green, 10 purple, 11 cream stripe |
| `floor_wood.pxl` | `parquet planks_dark planks brick_peach brick_dark brick_orange` | sheet row 4, cols 0–2 and 9–11 |
| `floor_checker.pxl` | `blue_teal teal_mint black_white greens peach_cream lavender_cream` | sheet row 4, cols 3–8 |
| `floor_plain.pxl` | `green pink blue navy red peach orange lavender salmon purple tan cream` | sheet row 5: carpet colours |
| `floor_large.pxl` | `cream_peach brown_gold orange_yellow purple_speckle` | sheet row 6: big 2×2 tiles and a speckled carpet |

## How a wall is built (all 12 styles share it)
A wall is **3 tiles tall**: `top`, `mid` (repeat for taller rooms), then `skirting` **or**
`wainscot` as the bottom tile. Columns tile seamlessly left to right.
- `top`: rows 0–1 light wood trim, row 2 dark wood line, row 3 a 1 px shadow in the wallpaper's
  dark shade, then wallpaper.
- `mid`: wallpaper only.
- `skirting` (bottom of a plain wall): wallpaper down to row 25, then row 26 wallpaper shadow,
  row 27 dark line, rows 28–29 a light board with a 1 px dark divider every 8 px, row 30 dark
  line, row 31 the darkest outline where the wall meets the floor.
- `wainscot` (bottom of a panelled wall): 9 rows of wallpaper, then a dark line, a light line,
  and 4 recessed panels 8 px apart (7 px frame, flat light inside, noisy 1 px grain down the
  right edge of each frame), closed by light / dark / darkest rows.
- Wallpaper is **one flat colour** with a few 1 px lighter specks (~2 per tile) so a big wall
  isn't dead flat; stripes and planks are 1 px darker lines of the same hue. The wood trim
  is identical on every style (light `#d58c4f`, highlight `#d8945c`, line `#995947`, floor
  edge `#65352f`); only the wallpaper and its 1 px shadow shade change.

## How a floor is built
- **Checker** (`floor_checker`): 2×2 squares of 15 px with a 1 px dark grout line on the right
  and bottom of each square; the last row of each square is a 1 px lighter bevel.
- **Bricks** (`brick_*`): bricks 16×8 with 1 px dark mortar, every other row offset by 8 px;
  each brick has a small lighter L of grain in its bottom-left corner.
- **Parquet**: 8×8 basket-weave blocks alternating horizontal / vertical boards, 1 px joints.
- **Planks**: long boards running one way, 1 px dark joints, staggered ends.
- **Plain carpet** (`floor_plain`): 3 colours: base, plus a sparse grid of 1 px darker dots.

## Scale
Tiles are 32×32 at 1×, the same pixel size as the people (16×32 trainer cell, 21 px tall body)
and the furniture in `../interior_ref/`. A standing trainer is ~2/3 of one wall tile tall.

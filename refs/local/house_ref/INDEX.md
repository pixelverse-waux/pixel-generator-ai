# house_ref.png: what each file is

Source: `refs/local/house_ref.png`, 2070×416, **1×**, buildings on a flat `#cae2ea` sky-blue
background inside an 11 px orange frame (the frame is not part of any house).
The user's private reference: study only, don't copy pixels.
This is **the authority on building exteriors**. Every `.pxl` here pastes back onto the sheet
with 0 pixels different (only the frame and two stray 1-px specks are left out). One file per
building and season, one frame each, with a `; src x,y wxh` comment. A whole house uses up to 88
colours (lots of near-duplicate noise), so palettes run past `Z` into `a–z`, `0–9` and symbols.
Study copies only; they break the 15-colour lint rule on purpose.

| File | Size | What it is |
|---|---|---|
| `cabin_blue_summer/_winter.pxl` | 158×165 | log cabin, blue shingle roof, gable faces the viewer, gold plaster infill, grey stone foundation |
| `cabin_green_summer/_winter.pxl` | 158×165 | same cabin, green roof, sandstone foundation |
| `cabin_salmon_summer/_winter.pxl` | 158×165 | same cabin, salmon roof |
| `long_blue_summer/_winter.pxl` | 274×176 | cabin with a long side wing on the left (roof seen along its slope, 2 windows) |
| `long_green_summer/_winter.pxl` | 276×176 | same, green |
| `long_salmon_summer/_winter.pxl` | 274×176 | same, salmon |
| `shop_wide_summer/_winter.pxl` | 222×153 | wide building, flat-on roof with a small gabled porch in front, lanterns either side of the door, sign board, raised on short stone-footed posts |
| `shop_small_straw/_summer/_winter.pxl` | 169×153 / 167×153 | smaller shop, porch gable on the left and one window wing on the right; `straw` has a yellow thatch roof (summer only), `summer`/`winter` a green shingle one |

The three cabins are one drawing (identical silhouette; salmon differs by ~200 px at the
foundation) with roof, infill and foundation recoloured, like the furniture colour variants in
`../interior_ref/`. Every winter frame has exactly the summer silhouette: snow and icicles are
painted over existing pixels, never added outside them.

## How a house is drawn
- **View**: front-on with a top-down tilt; the roof is the biggest mass. On the cabin the roof
  takes rows 0–125 of 165 and the gable wall shows between its two slopes. Roof edges step
  **3 px across per 2 px down**. The ridge is a 1-shingle-wide wood beam (or the chimney) running
  straight down the middle.
- **Light from the left**: the left roof slope is a step lighter than the right (blue
  `#4b8ab7` vs `#427ca5`). Each shingle is a staggered brick-like course ~9 px tall with a 1 px
  dark line (`#2a4d66` on blue) and a 1 px light glint (`#7dabcb`) along its top/left edge.
- **Outline**: 1 px, a dark shade of each material, never black: roof `#2a4d66`, logs
  `#774520` / `#6f401e`, stone `#615242`.
- **Logs**: horizontal and vertical beams in a 3-value orange ramp (`#ff9345`, `#d97d3b`,
  `#774520`) with faint 1 px grain; vertical posts frame the door and corners, round log ends
  cap the horizontal beams.
- **Infill** between the beams is flat plaster (gold `#d5b95b` on the blue cabin, peach on the
  shops) with a 1 px shadow under each beam.
- **Door** ~26×35 incl. frame: dark brown planks (`#6f401e`, `#512f16`), 2 plank lines, a
  1-px-dark knob and a short handle. **Steps** ~36 wide, 3 boards of 6 rows, in front of the door
  and below the foundation line.
- **Windows** ~26×17 (2 panes) or 4 panes: orange wood frame, blue glass (`#58a0d3`,
  `#67bbf7`) with one diagonal light streak per pane, a 2-row sill under the frame.
- **Foundation**: a ~10-row strip of irregular flagstones (`#8e846f` with `#615242` joints)
  along the bottom of the walls; shops stand on posts with grey stone feet instead.

## Winter (`*_winter`)
Same drawing, snow painted on (12–14 % of the pixels change colour):
- white wedges (`#ddffff`, shaded `#c6e4e4`) on the upper-left of scattered shingles;
- the ridge beam / chimney turn white;
- icicles 1–2 px wide and 3–8 px long hang from the eaves and the porch gable;
- a 1–2 row snow cap on every sill, beam top, log end and step;
- the stone foundation gets white joints.

## Scale
1×, the same pixel size as the 16×32 trainers, the furniture and the 32×32 floor tiles: a
door (35 tall) fits a 21-px trainer with room; a cabin is ~5 tiles wide.

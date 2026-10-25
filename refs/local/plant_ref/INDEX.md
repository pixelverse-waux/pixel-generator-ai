# plant_ref: Flower & Plant Pack (flowers, grass, plants, bushes)

Source: the user's `Flower_Plant_Pack/` (v1.0, Deniz Samed Öztaş, made with PixelLab AI then
cleaned up and recoloured). **Commercial licence (`LICENSE.txt`)**: may be used in games, may
**not be redistributed** as assets. Private study material: never copy its pixels into new
sprites and never export it to `web/`.
Copied here: `README.txt`, `LICENSE.txt`, `palette.gpl` (the shared 85-colour palette),
`overview.png`, plus every static sprite converted to `.pxl` (the source PNGs are clean, so the
conversion is exact: one letter per source colour, checked). Letter notes give each colour's
palette role (`leaf summer 3`, `petal red 1`, ...).

| File | Frames | What it is |
|---|---|---|
| `<type>.pxl` | one layout row per design (`d01 d02 ...`), one frame per variant: `d01_red`, `d02_summer` | the normal size (32×32; sunflower and cattail 32×48; large bush 48×48) |
| `<type>_small.pxl` | same names | the small size (16×16; 16×32; 32×32): the same design redrawn at half size, not a downscale |
| `sway/<type>.pxl` | `sway_0` … `sway_11` | the 12-frame wind-sway loop of design 01 (red / summer), 120 ms per frame |

32 types: flowers (tulip, daisy, rose, sunflower, lavender, poppy, bluebell, dandelion,
wildflowers, waterlily), grass (tuft, tall, flowering, cattail, wheat, clover), plants (leafy,
longleaf, fern, thistle, vine, sprout, lilypad, cactus, succulent, mushroom), bushes (round,
large, flowering, berry, hedge, wild). Variants: flowers, flowering grass, flowering and berry
bushes come in 7 colours (`red pink yellow orange white blue purple`); grass, plants and bushes
in 4 seasons (`spring summer autumn winter`); cactus, succulent, mushroom, wildflowers have one.

## How these plants are drawn
- **Grid**: made for 16×16 tiles. Canvases are whole tiles (32×32 = 2×2), and every sprite is
  **bottom-aligned on the last row and centred**: the art fills about 12–28 × 19–28 of a 32×32
  canvas (tulip 12×26, round bush 25×22, sunflower 21×43 on 32×48, large bush 41×35 on 48×48).
  Next to a 16×32 trainer, a normal flower is knee-to-waist high, a sunflower head-high.
- **Outline**: 1 px, the **darkest two steps of the leaf ramp** (`leaf * 0` / `1`); petals are
  outlined in their own dark step (`petal red 1`), never black.
- **Light from the top left**: lit leaf tips use steps 4–6, bodies 2–3, shadow 1.
- **Shared palette**: each leaf ramp is 7 steps (`leaf spring/summer/autumn/autumn_red/winter
  0–6`), each petal ramp 6, plus yellow/brown flower centres. One sprite uses only 5–18
  colours. Seasons and colours are **palette swaps of one drawing**: a colour variant changes
  only the petals or berries; a season variant swaps the leaf ramp (spring fresh green with
  tiny blossoms, summer full green, autumn gold / orange-red, winter frosted with snow).
- **Small size**: half the size with the outline redrawn, so 1-px features (stems) stay 1 px.
- **Sway**: a 12-frame sine loop. The **bottom third never moves**; the top drifts about ±2 px
  sideways (cactus and other rigid plants only ±1 px at the very top). Plays at ~8 fps, the
  same timing as the matching seasonal tree pack.

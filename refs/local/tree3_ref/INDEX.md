# tree3_ref.png (and tree4_ref.png): 15 trees × 4 seasons

Source: `refs/local/tree3_ref.png`, 2962×1218: a screenshot of a **4× pixel-art sheet** (the
re-grid found a 4.000 px period), rows on flat coloured bands (spring green, summer dark green,
autumn brown, winter slate) with a text label on the left. The screenshot is softened (about
13 % of each 4×4 block is off-colour), so the 1× art was **reconstructed** by sampling the middle
of every 4×4 cell, then each band's background was removed. Files are exact copies of that 1×
reconstruction (one colour per source colour, no merging), not of the PNG's blurred pixels.
`tree4_ref.png` (3358×1422) is the **same sheet captured again at ~4.9×** and blurrier; its
trees match these to within resampling noise (oak and palm 1–3 px narrower). It was not split:
use these files.
The user's private reference: study only, don't copy pixels.

Layout: `<season>/<species>.pxl`, one frame named after the season, `; src` = rect on the 1×
re-grid. Seasons: `spring summer autumn winter`.

| Species (my names) | Summer size | Notes |
|---|---|---|
| `oak` | 28×41 | dark round crown of big clumps, red-brown trunk, wide root flare |
| `apple` | 30×40 | light crown dotted with 3×3 red apples (kept in every season, even winter) |
| `pear` | 32×42 | pale yellow-green, slightly pointed crown |
| `cherry` | 29×41 | the spring one is **all pink blossom**; other seasons a normal crown |
| `birch` | 24×41 | narrow, white trunk with dark flecks |
| `gnarled` | 31×46 | twisted two-tone (purple-brown + tan) trunk, crown off to one side |
| `sapling` | 21×26 | small bush-tree |
| `wide_oak` | 42×42 | broadest crown, two trunk forks |
| `orange` | 30×34 | dark crown full of orange-red blossom / fruit |
| `fir` | 22×37 | small cone of tiers |
| `spruce` | 21×56 | tall, narrow, dark blue-green tiers |
| `cypress` | 18×57 | tall column |
| `palm` | 31×43 | curved ringed trunk, fan of fronds |
| `bamboo` | 30×44 | cluster of jointed green canes |
| `willow` | 29×43 | crown with hanging strands |

## How these trees are drawn
- **Scale**: smaller than `../tree_ref/`: 18–42 wide, 26–57 tall. A 41-px oak is ~2 trainers
  tall (21 px), ~1.3 tiles. Use this scale for trees beside 16×32 people; `tree_ref` is the
  "big tree" scale.
- **Shape**: crown ~2/3 of the height on a short trunk 4–6 px wide that **splits into 3–5 roots**
  spreading 12–16 px at the ground row. A 1–3 px ground speck (petal / leaf) sits beside the roots.
- **Crown**: overlapping clumps 6–10 px, each with a light top-left, mid body and dark
  underside; the darkest green rims the bottom and right of the crown (light from top-left).
  Edge is 1-px ragged, outline = darkest crown shade, never black.
- **Bark**: 3–4 values, light on the left, dark on the right, darkest outline; roots lit on top.
- **Ramps** are short (leaves 4–5, bark 3–4); each file holds 9–45 colours only because the
  reconstruction keeps faint tone variants: merge them when drawing.

## Seasons = same tree, repainted
Silhouettes match across seasons (0–45 px different on most species; the willow strands and the
summer fir/gnarled/orange vary a little). Only the colours change:
- **spring**: summer crown plus 1–2 px white/pink blossom dots; cherry turns fully pink;
- **summer**: plain greens (the base design);
- **autumn**: the leaf ramp swapped to orange / gold / red-brown, same clumps; bamboo and palm go
  gold too; trunks unchanged;
- **winter**: leaves stay dark green underneath, every clump's **upper half turns to snow**
  (white + pale blue-grey shade); fruit stays visible; the ground speck becomes a snow fleck.

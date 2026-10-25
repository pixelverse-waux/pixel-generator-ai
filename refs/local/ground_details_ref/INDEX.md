# ground_details_ref.png: pebbles and leaves to scatter on the ground

Source: `refs/local/ground_details_ref.png`, 336×288, 1×, transparent, **only 4 colours**. Small
decals laid loosely: pebble clusters in the top part (y 0–129), fallen-leaf / clover sprigs in
the bottom part (y 130–287). The user's private reference: study only, don't copy pixels.
Each decal = pixels within 3 px of each other, cut out alone and padded bottom-centred; the
`; src` comment is its rect on the sheet. Exact copies.

| File | Frames | Cell | What it is |
|---|---|---|---|
| `pebbles.pxl` | `pebble_00` … `pebble_77` | 29×26 | flat pebble clusters: one colour `#a08c61` |
| `leaves.pxl` | `leaf_00` … `leaf_56` | 32×29 | leaf sprigs: `#5b9252` shade, `#96c55f` leaf, `#bad362` tip |

## How details are drawn
- **No outline and very few colours**: a pebble is a flat 1-colour blob (1–2 px grit up to
  ~8×6 stones); a leaf is a 2–3 px diagonal lozenge in 2 greens with a lighter tip. They sit on
  the ground colour and read by contrast alone.
- **Clusters, not singles**: one decal is 1 big + 2–4 small pebbles, or 3–7 leaves fanning from
  a point, inside a 16–32 px area. Sizes vary a lot across the set so a field never repeats.
- The colours are the ground's own: pebbles use the dirt/sand family, leaves the grass ramp
  (`#5b9252 #96c55f #bad362` are the same greens as `../ground_ref/grass.pxl`).
- Use them to break up flat ground tiles: scatter a few per screen, never in a grid.

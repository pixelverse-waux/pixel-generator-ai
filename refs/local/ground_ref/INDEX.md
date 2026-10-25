# ground_ref.png: fence and ground only

Source: `refs/local/ground_ref.png`, 240×800, **1× on a 16×16 tile grid**, transparent. The
sheet also has a house, rocks, trees, bushes, stumps, mushrooms and a scarecrow: **not used**
(the user asked for the ground and the fence only). The user's private reference: study only,
don't copy pixels. Every frame is an exact copy of its source rect (`; src` comment), checked
colour for colour.

| File | Frames | What it is |
|---|---|---|
| `fence_tiles.pxl` | `t<col>_<row>`, 16 tiles of 16×16 | the fence block cut on the tile grid: horizontal runs, end posts, corners and sides of two pens |
| `fence_block.pxl` | `block` 80×64 | the same block whole, to see how the tiles join |
| `cobble.pxl` | `patch autotile strip` | pale cobblestone: a loose patch, an 8×3-tile path piece with a hole, corners and a corridor, a 1-tile vertical strip |
| `grass.pxl` | `patch_a hole_a edges_a` / `patch_b hole_b edges_b` | grass: a round patch, a 2×2 tile with a hole, loose edge pieces; two versions |
| `dirt.pxl` | `patch hole path` | dirt: a round patch, a 2×2 tile with a hole, a winding path |
| `sand.pxl` | `border tile bit` | packed sand: a 2×2 border frame, a 2×2 paving tile, a small bit |

## Fence (`fence_tiles`, `fence_block`)
- **Posts**: 5 px wide (outline, 3 px body, outline), 15 px tall with a rounded 3-px top lit
  orange-tan (`#c48e5e #ab7757`), body `#865441` / `#714438`, shade `#5d3731`, outline `#482a2a`.
  **Two posts per tile, 8 px apart.**
- **Rail**: 3 rows across the whole tile at rows 6–8: outline `#404155`, light steel blue
  `#7294b8`, outline. On a vertical run the rail runs down the outer side of the posts
  (`#5b6485 #687ca1`).
- **Shadow** (`#36362c`, a 35 % transparent black in the source, kept as its own letter): a
  1-px ring round the bottom 3 rows of each post plus one row under it (`.KAEDDAK` /
  `.KKAAAKK` / `..KKKKK`). Draw it over the ground, not as part of the post colour.
- 12 colours, no black. Pens are built from the same tiles: straight runs, end posts, corners.

## Ground
- **Grass** (`#7aad55` base): the middle is **flat**, the edge is a ring of overlapping 3–5 px
  tufts lit on top (`#96c55f`, tips `#bad362`), shaded below (`#5b9252 #4b7a4c`), outlined in
  dark green `#264532`. A "hole" tile is a square of grass with a tufted hole cut in it, so the
  ground under it shows through.
- **Dirt** (`#967e5d`): flat, with a 1–2 px dark rim `#46332a` and a lighter lip on top
  (`#ae976c #c2ad74`); the winding path keeps a 6–10 px width and bulges at the ends.
- **Cobble**: only 3 colours: cream stones `#e7dcc4`, joints `#c7a896`, deep joints `#9a7b71`.
  Stones are irregular 4–8 px blobs; the path edge is ragged because whole stones stick out.
  No outline.
- **Sand**: 4 colours (`#b4997d` base, `#ceb38f` light, `#a1846d #957e66` grout); 8×8 slabs.
- Ground patches are **flat in the middle and detailed only at the edge**, so they tile and
  don't fight the sprites standing on them.

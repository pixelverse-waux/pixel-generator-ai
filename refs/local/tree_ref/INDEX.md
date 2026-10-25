# tree_ref.png: what each file is

Source: `refs/local/tree_ref.png`, 1232×1232, which is **176×176 art upscaled 7×** on a baked-in
grey checkerboard (`#807b7a` / `#b3b0af`, 16 px squares at 1×). The checkerboard is not part of
the art: it was flood-filled away from the edges (none of it sits inside a tree).
The user's private reference: study only, don't copy pixels.
This is **the authority on trees**. Every `.pxl` here is the tree at 1×; pasted back and scaled
7× it matches the PNG with 0 pixels different. The `; src` comment is the rect on the 1× sheet.

| File | Size (1×) | Colours | What it is |
|---|---|---|---|
| `birch.pxl` | 48×75 | 21 | round leafy crown, white-blue bark with dark marks, a Y-fork of branches showing through a gap in the leaves |
| `oak.pxl` | 47×75 | 31 | round, denser and darker crown, brown trunk with a short side stub |
| `pine.pxl` | 46×90 | 14 | conifer: pointed tip, stacked drooping tiers widening downward, dark brown trunk with root flare |

## How a tree is drawn
- **View**: same top-down 3/4 as the houses and people: a tall shape standing on its trunk base.
  The **crown is ~2/3 of the height** (leafy trees: rows 0–52 of 75; pine: rows 0–58 of 90),
  the trunk the rest. Trunk is 6–8 px wide and **flares at the base** (roots 8–12 px), with the
  bottom row as the ground line.
- **Leafy crown** = many overlapping **clumps of ~8–12 px**. Each clump is lit on top (light
  green) and falls to mid then dark green underneath, so the crown reads as bumps, not a flat
  disc. The silhouette is ragged: 1–2 px notches and tufts all round, never a smooth circle.
  The bottom rows of the crown are the darkest band (shadow over the trunk).
- **Pine** = 6–7 tiers stacked down from a 1-px tip, each tier a drooping bough row a bit wider
  than the one above, with single tip pixels poking out sideways; lit top edge of each tier,
  dark under it.
- **Outline**: no black. The edge is the darkest shade of the crown (birch `#0f4a34`/`#043523`,
  oak `#073d23`/`#032c18`, pine `#033310`) and of the bark (birch `#434965`, oak `#61341e`, pine
  `#372719`).
- **Ramps**: leaves 4–5 greens (birch blue-green `#043523 #0f4a34 #23674e #388d5e #44af66`;
  oak `#032c18 #073d23 #0d5b2a #1a7e3b #249c4c`; pine darker `#033310 #073f15 #0a4c1b #106727
  #167c2f`). Bark 3–4 values plus outline; birch bark is pale blue-grey (`#8b93af #b3b9d1
  #cdd2e6`) with dark brown flecks. The oak's 31 colours are trunk noise; merge to the ramp.
- **Bark texture**: vertical 1-px streaks of the shade colour, a few short dark marks; light on
  the left edge, shade on the right.

## Scale
1×, the same pixel size as the 16×32 trainers (21 px tall): a tree is 75–90 px tall, about
3.5–4 trainers, and ~1.5 32×32 tiles wide. The house_ref cabin (158×165) is about twice a tree's
height.

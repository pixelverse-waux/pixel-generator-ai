# dog_ref.png: what each row is

Source: `refs/local/dog_ref.png`, 384×2608, **64×64 cells at 1×** (6 columns × 40 rows, the last
48 px are empty), transparent background, 9 colours. A grey short-coated dog with a pale blaze,
chest and socks. The user's private reference: study only, don't copy pixels.
This is **the authority on how dogs look, move and behave**. Where `style/STYLE_GUIDE.md`
disagrees, copy this. Every `.pxl` here converts back to the sheet with 0 pixels different.

Every `.pxl` here uses the same letters:

| Letter | Colour | Role |
|---|---|---|
| K | #120e14 | outline, eyes, inner lines (near side) |
| A | #0d0e1e | **far-side outline**: legs, tail and rump on the side away from the viewer in motion (walk, jump, leap, bow, scratch). Standing and sitting use K only |
| B | #312b30 | nose |
| C | #414752 | fur shade: inside of legs, far legs, under the tail |
| D | #7d3564 | tongue / open mouth |
| E | #626773 | fur base |
| F | #868d9b | fur light: brows, paw tips, sock shade |
| G | #b6b8c7 | blaze, muzzle, chest, socks, tail tip |
| H | #e1dee7 | eye glint |

| File | Sheet rows | Frames | What it is |
|---|---|---|---|
| `move.pxl` | 4 down, 6 left, 7 right, 5 up | 6 each | **walk cycle** |
| `idle.pxl` | 1 | 4 (`down up left right`) | standing still |
| `sit.pxl` | 0 | 5 (`down up left right tilt`) | sitting; `tilt` = head tilted, curious |
| `lie.pxl` | 2 left, 3 right | 6 each | 0 lying head up (front-ish), 1–2 curled asleep, 3 lying head up (side), 4–5 asleep stretched |
| `sleep.pxl` | 24 down_left, 26 left, 27 right, 25 down_right | 2 each | sleep breathing loop |
| `jump.pxl` | 8 down, 10 left, 11 right, 9 up | 4 each | hop: crouch, take off, stretched in the air, land |
| `leap.pxl` | 36 down, 38 left, 39 right, 37 up | 4 each | bigger jump: side frame 1 rears up steeper than `jump`, front crouch is lower, back view tucks the tail. Both lift the feet 7 rows at the top |
| `bow.pxl` | 12 down, 14 left, 15 right, 13 up | 4 each | play bow: chest drops to the ground, rump and tail go up |
| `scratch.pxl` | 16 left, 17 right | 6 each | sitting, scratching the ear with a hind leg |
| `groom.pxl` | 18 | 5 (`sit_*`) | sitting front, licking a paw |
| `pant.pxl` | 19 sit, 20 stand | 3 each | panting, tongue out (front) |
| `bark.pxl` | 22 sit, 23 stand | 3 each | barking, mouth wide (front) |
| `smile.pxl` | 21 | 2 (`sit stand`) | happy open mouth, single frame per pose |
| `sniff.pxl` | 32 down, 34 left, 35 right, 33 up | 6 each | standing, nose lowers to the ground and back up |
| `sniff_sit.pxl` | 28 down, 30 left, 31 right, 29 up | 6 each | same while sitting |

## Body (measured)

| View | Size (w×h) | Feet row | Notes |
|---|---|---|---|
| stand front / down | 22×38 | 51 | head 18 wide with ears flopped out to the sides, chest blaze in G, legs 4 wide with a 4 px gap |
| stand back / up | 22×43 | 56 | G stripe down the back of the head, tail hangs between the hind legs |
| stand side | 43×34 | 47 | long level back, deep chest, feathered tail hanging low |
| sit front | 24×34 | 48 | tail curls round the right paw |
| sit side | 34×37 | 51 | |
| lying / asleep | 43–46×25 | 51 | |

**Draw dogs on a 48×48 frame** (`size 48 48`): the user chose the 3/4 size on 2026-10-25 (at 64 a
dog towered over the 16×32 people). `48/` holds every file here shrunk to 48×48 with
`pixelkit.rescale --to 48 --phase 1,0` (one row/column in four dropped, outlines kept 1 px): read
those when drawing. Sizes at 48: standing side 32×26 (feet row 35), front 16×29 (feet row 38), sit
front 18×25, side 26×28, lying 32×19.

## How a dog walks (`move.pxl`)
- **6 frames per direction**. Right is an exact mirror of left in every action, so right frames
  can be `mirror` of left ones.
- Side: diagonal pairs move together (trot). Near legs are outlined in K; far legs are outlined
  in **A** and filled E/C so they read as behind. Each foot ends in 2 rows of G/F sock. The back
  bobs 1 px (top row 13 on frames 0 and 3, 14 on the rest). Feet stay on row 47.
- Front/back: legs alternate long/short, the feet line moves between rows 52 and 53, and the
  head stays level.
- The tail sways a pixel or two each frame; it never curls over the back while walking.

## How a dog behaves
Idle: stand (`idle`), sit, head tilt, pant, smile, bark, sniff the ground, scratch, lick a paw,
lie, sleep. Active: hop (`jump`), big jump (`leap`), play bow (`bow`).
While standing or sitting, the legs stay locked; only the head, mouth and tail move.

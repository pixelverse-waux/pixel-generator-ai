# character_female_ref.png: what each file is

Source: `refs/local/character_female_ref.png`, 366×513, Pokémon Ruby/Sapphire May sheet
(arranged by voliol), **1×**, cells framed on a mint `#73c5a4` background.
The user's private reference: study only, don't copy pixels.
This is **the authority on how a girl trainer looks and walks**, together with
`../character_male_ref/`.

`walk.pxl`, `run.pxl` and `field_move.pxl` share these letters:

| Letter | Colour | Role |
|---|---|---|
| K | #000000 | outline |
| A | #293941 | near-black: bike shorts |
| B | #4a3139 | dark brown: hair shade, hair outline |
| C | #7b5a52 | hair mid shade |
| D | #626273 | grey: shoes, shorts shade |
| E | #c54141 | red: bandana, shirt |
| F | #a46a52 | hair base |
| G | #bd9c5a | gold: bag |
| H | #ff625a | light red highlight: bandana |
| I | #cd8373 | skin shade |
| J | #dea494 | skin base |
| L | #ffc55a | yellow: accents |
| M | #cdcdde | white shade: skirt, shoes |
| N | #ffdecd | skin light: face |
| O | #ffffff | white |

| File | Cell | Frames | What it is |
|---|---|---|---|
| `walk.pxl` | 16×32 | down / left / right / up × 4 | **walk cycle**: stand, step A, stand (copy), step B |
| `run.pxl` | 16×32 | same | run cycle: body leans forward, longer stride |
| `field_move.pxl` | 32×32 | 5 | facing down, reaching into the bag and throwing a Poké Ball |
| `front.pxl` | 64×64 | 1 | full-body front battle art (own 15-colour palette) |

The sheet has no right-facing row: the game mirrors left, so `right_N = mirror left_N` in both
cycle files. Note her bandana tails and hair bunches flip with it.

Body: 14 px wide, 20 rows tall standing (rows 11–30 of the 16×32 cell); hair bunches stick out
past the face on both sides. Step frames drop the whole sprite 1 px; the stand frame is the
high point.

Cut from these source rectangles (x, y): walk columns 11/28/45, run 66/83/100, rows 139/172/205
(down, up, left); field move 11/44/77/110/143 at y 470; front 11,53 (64×64).

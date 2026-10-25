# character_male_ref.png: what each file is

Source: `refs/local/character_male_ref.png`, 345×509, Pokémon Ruby/Sapphire Brendan sheet
(ripped by RetroniGamer), **1×**, cells framed on a mint `#73c5a5` background.
The user's private reference: study only, don't copy pixels.
This is **the authority on how a boy trainer looks and walks**, together with
`../character_female_ref/`.

`walk.pxl`, `run.pxl` and `field_move.pxl` share these letters:

| Letter | Colour | Role |
|---|---|---|
| K | #000000 | outline |
| A | #10213a | darkest navy: shirt/hair shade |
| B | #293a63 | navy base: shirt, shorts |
| C | #3a4a7b | navy light: hair, highlights |
| D | #7b4242 | skin outline / brown shade |
| E | #c54242 | red: hat band, shirt panel |
| F | #bd9c5a | gold shade: bag |
| G | #ff635a | light red highlight |
| H | #de9473 | skin shade |
| I | #ffc55a | yellow: gloves, bag |
| J | #ffc594 | skin base |
| L | #ffd6b5 | skin light: face |
| M | #dee6ef | white shade: hat |
| N | #ffffff | white: hat |

| File | Cell | Frames | What it is |
|---|---|---|---|
| `walk.pxl` | 16×32 | down / left / right / up × 4 | **walk cycle**: stand, step A, stand (copy), step B |
| `run.pxl` | 16×32 | same | run cycle: body leans forward, longer stride |
| `field_move.pxl` | 32×32 | 5 | facing down, reaching into the bag and throwing a Poké Ball |
| `front.pxl` | 64×64 | 1 | full-body front battle art (own 14-colour palette) |

Body: 14 px wide, 21 rows tall standing (rows 10–30 of the 16×32 cell), head + hat ≈ rows 10–21.
Step frames drop the whole sprite 1 px (rows 11–31); the stand frame is the high point.

Cut from these source rectangles (x, y): walk columns 2/19/36, run 56/73/90, rows 90/123/156/189
(down, right, left, up); field move 139/172/205/238/271 at y 376; front 2,14 (64×64).

# cat_ref.png: what each row is

Source: `refs/local/cat_ref.png`, 352×1696, **32×32 cells at 1×** (11 columns × 53 rows),
transparent background, 8 colours. The user's private reference: study only, don't copy pixels.
This is **the authority on how cats look, move and behave**. Where `style/STYLE_GUIDE.md`
disagrees, copy this.

Every `.pxl` here uses the same letters:

| Letter | Colour | Role |
|---|---|---|
| K | #120e14 | outline, eyes, whiskers, inner lines |
| A | #8f3622 | fur shade: far legs, belly, under the tail, rump |
| B | #ab572c | fur base |
| C | #cc7f3f | fur light: one stripe along the top of the back |
| D | #ca719f | nose |
| E | #c2b1a9 | inner ear |
| F | #e197c6 | open mouth / tongue (meow) |
| G | #e1dee7 | eye glint (blink) |

| File | Sheet rows | Frames | What it is |
|---|---|---|---|
| `move.pxl` | 4 down, 7 left, 6 right, 5 up | 4 / 8 / 8 / 4 | **locomotion cycle** (walk/run) |
| `move_diag.pxl` | 8–11 | 6 each | locomotion, diagonals |
| `idle_tail.pxl` | 20 down, 22 left, 23 right, 21 up | 8 each | standing idle: legs locked, head turns, tail sways |
| `idle_tail_diag.pxl` | 24–27 | 8 each | same, diagonals |
| `turn.pxl` | 44 down, 47 left, 46 right, 45 up | 9 / 7 / 7 / 5 | standing, shifting weight / turning (one paw lifts at the end) |
| `turn_diag.pxl` | 48–51 | 9 / 9 / 5 / 5 | same, diagonals |
| `idle.pxl` | 1 | 8 | standing still in 8 directions |
| `sit.pxl` | 0, 52 | 6 / 4 | sitting in several directions |
| `lie.pxl` | 2, 3 | 6 / 10 | lying, loaf, curled sleep, stretched out |
| `blink.pxl` | 28–31 | 3 each | blink: sit, stand front, stand back, lie |
| `meow.pxl` | 32–35 | 8 each | meow (mouth opens, F shows) in the same 4 poses |
| `groom.pxl` | 36–38 | 9 / 9 / 7 | licking a paw / washing: sit, stand, lie |
| `look.pxl` | 39, 40 | 11 each | sitting, looking around / scratching |
| `hiss.pxl` | 41–43 | 2 / 2 / 1 | arched back, hiss |

Rows 12–19 (lying and sleeping in each direction, 2 frames) aren't converted yet:
`python3 -m pixelkit.img2pxl refs/local/cat_ref.png -o refs/local/cat_ref/<name>.pxl --cell 32x32 --bg-all --rows 12,13 --names a,b`

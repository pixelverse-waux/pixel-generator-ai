FLOWER & PLANT PACK  (v1.0)
32 plant types - 82 designs - 7 flower colors - 4 seasons - animated - 2 sizes
pixel art for 16x16 tile grids: top-down RPGs, farming sims and adventure games

============================================================
CONTENTS
============================================================
786 static sprites + 786 animated sprite strips
(every static sprite also comes as a looping wind-sway animation)

  sprites/<category>/<type>/     static PNGs, one folder per plant type
                                   flowers/  grass/  plants/  bushes/
  animated/<category>/<type>/    12-frame looping "sway" strips, each with
                                 a preview GIF (see ANIMATIONS below)
  animated/animations.json       frame size, frame count and speed of
                                 every strip
  atlas/                         one sprite atlas per category
                                 (PNG + JSON, TexturePacker "JSON Hash" format)
  palette.gpl                    the shared 85-color palette
                                 (Aseprite / GIMP / Krita)
  overview.png                   every design at a glance

Types (32 types, several different designs of each).
File name prefix, description, number of designs, variants, size (small size):
  FLOWERS
    flower_tulip       Tulip                     x3  7 colors  32x32  (small 16x16)
    flower_daisy       Daisies                   x3  7 colors  32x32  (small 16x16)
    flower_rose        Rose                      x2  7 colors  32x32  (small 16x16)
    flower_sunflower   Sunflower                 x3  7 colors  32x48  (small 16x32)
    flower_lavender    Lavender                  x3  7 colors  32x32  (small 16x16)
    flower_poppy       Poppies                   x3  7 colors  32x32  (small 16x16)
    flower_bluebell    Bluebells                 x3  7 colors  32x32  (small 16x16)
    flower_dandelion   Yellow pompom flowers     x3  7 colors  32x32  (small 16x16)
    flower_wildflowers Mixed wildflowers         x2  1 color   32x32  (small -)
    flower_waterlily   Water lily                x3  7 colors  32x32  (small 16x16)
  GRASS
    grass_tuft         Grass tuft                x3  4 seasons 32x32  (small 16x16)
    grass_tall         Tall grass                x2  4 seasons 32x32  (small 16x16)
    grass_flowering    Grass with small flowers  x2  7 colors  32x32  (small 16x16)
    grass_cattail      Cattails (reeds)          x3  4 seasons 32x48  (small 16x32)
    grass_wheat        Wheat                     x3  4 seasons 32x32  (small 16x16)
    grass_clover       Clover                    x2  4 seasons 32x32  (small 16x16)
  PLANTS
    plant_leafy        Broad-leaf plant          x3  4 seasons 32x32  (small 16x16)
    plant_longleaf     Long-leaf plant           x2  4 seasons 32x32  (small 16x16)
    plant_fern         Fern                      x4  4 seasons 32x32  (small 16x16)
    plant_thistle      Thistle                   x3  4 seasons 32x32  (small 16x16)
    plant_vine         Hanging vine              x3  4 seasons 32x32  (small 16x16)
    plant_sprout       Sprout / seedling         x1  4 seasons 32x32  (small 16x16)
    plant_lilypad      Lily pads                 x3  4 seasons 32x32  (small 16x16)
    plant_cactus       Barrel cactus             x2  1 color   32x32  (small 16x16)
    plant_succulent    Succulent                 x3  1 color   32x32  (small 16x16)
    plant_mushroom     Red mushrooms             x3  1 color   32x32  (small 16x16)
  BUSHES
    bush_round         Round bush                x3  4 seasons 32x32  (small 16x16)
    bush_large         Large bush                x3  4 seasons 48x48  (small 32x32)
    bush_flowering     Flowering bush            x2  7 colors  32x32  (small 16x16)
    bush_berry         Berry bush                x2  7 colors  32x32  (small 16x16)
    bush_hedge         Hedge block               x1  4 seasons 32x32  (small 16x16)
    bush_wild          Wild shrub                x1  4 seasons 32x32  (small 16x16)

============================================================
VARIANTS
============================================================
Flowers - plus the flowering grass, flowering bush and berry bush -
come in 7 colors:
  red, pink, yellow, orange, white, blue, purple
  (only the petals / berries change color, the leaves stay green)

Grass, plants and bushes come in 4 seasons:
  spring   fresh green with tiny blossoms
  summer   full green
  autumn   golden dry grass, golden ferns; orange-red bushes and vines
  winter   frosted, snow-covered leaves
The leaf colors match the Seasonal Tree Pack season by season.

Barrel cactus, succulent, red mushrooms and mixed wildflowers come in one
version.

============================================================
FILE NAMES
============================================================
  <type>_<design>_<variant>.png                flower_tulip_02_purple.png
  <type>_<design>_small_<variant>.png          bush_berry_01_small_blue.png
  <type>_<design>[_small]_<variant>_sway.png   grass_tall_03_autumn_sway.png

Every design exists in 2 sizes. The "small" version is the same design at
half size, with its outline redrawn for the smaller size (not a blurry
downscale).

============================================================
FORMAT
============================================================
- PNG with true alpha transparency, no background, no semi-transparent
  pixels.
- Made for 16x16 tile grids. Every canvas is a multiple of 16
  (see the size list above):
    16x16 = 1x1 tile (small flowers and grass)   32x32 = 2x2 tiles
    16x32 = 1x2 tiles (small sunflower, cattails) 32x48 = 2x3 tiles
    48x48 = 3x3 tiles (large bush)
- Every sprite is bottom-aligned and horizontally centered on its canvas,
  so plants line up on your tile grid.
- All sprites share one limited palette (palette.gpl), so they sit
  together without clashing - and they match the other packs in the
  series.
- Light comes from the top left; every sprite has a dark outline.
- Use the sprites at their original size. Use nearest-neighbour / "point"
  filtering in your engine to keep pixels sharp.

============================================================
ANIMATIONS
============================================================
Each animated file is a horizontal strip of 12 frames.
Play at 120 ms per frame (about 8 fps), looping - the same timing as the
Seasonal Tree Pack, so trees and plants sway together.

  sway   stems, leaves and flowers sway in the wind; the base stays still.
         Rigid or floating plants (cactus, succulent, mushrooms, lily pads,
         water lily, hedge) only move gently at the top.

Frame size = the sprite's size (e.g. 32x32 -> the strip is 384x32).
animated/animations.json lists every strip with its frame size, frame
count, frame duration, variant and matching static sprite.

Every strip has a matching *_preview.gif next to it: the same animation,
enlarged 4x on a transparent background, so you can see it in any image
viewer. The GIFs are previews only - use the PNG strips in your game.
(Unity imports GIFs as textures; delete the preview GIFs before importing
the folder if you don't want them in your project.)
Animated plants use the same design, size and base position as their
static counterpart, so the two can be mixed in the same scene.

Godot:   AnimatedSprite2D -> SpriteFrames -> "Add frames from sprite sheet",
         Horizontal 12, Vertical 1.
Unity:   Sprite Mode = Multiple, Sprite Editor -> Slice -> Grid By Cell
         Size (frame width x height), Filter Mode = Point, Compression = None.
GameMaker / Phaser / others: 12 equal frames, left to right.

Godot:   import with Filter = Nearest (Project Settings -> Rendering ->
         Textures -> Default Texture Filter = Nearest).
Unity:   Texture Type = Sprite, Pixels Per Unit = 16, Filter Mode = Point,
         Compression = None.
Atlases: the JSON files use the common TexturePacker "JSON Hash" format
         (Phaser, PixiJS, Godot importers and most engines).

============================================================
LICENSE
============================================================
See LICENSE.txt. Short version: use it in unlimited commercial or
non-commercial games; don't resell or redistribute the asset files
themselves.

============================================================
CREDITS
============================================================
Generated with PixelLab AI, then cleaned up, recolored (flower colors and
seasons) and animated by hand and with a custom pixel-art pipeline.

Questions or feedback? Leave a comment on the itch.io page.

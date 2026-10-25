/*
 * catsprite.js: play the cat sprites exported by `python3 -m pixelkit.web`. No dependencies.
 *
 *   <canvas id="cat"></canvas>
 *   <script src="catsprite.js"></script>
 *   <script>
 *     CatSprite.load("cats/ginger_tabby.json").then((cat) => {
 *       const player = cat.attach(document.getElementById("cat"), { scale: 4 });
 *       player.play("move/left");          // any key of cat.animations
 *       // player.pose("sit/sit", 0);      // a still from cat.poses
 *       // player.play("meow/sit", () => player.play("idle_tail/down"));  // runs once, then continues
 *     });

 *   </script>
 */
(function (global) {
  "use strict";

  class CatSprite {
    constructor(meta, image) {
      this.meta = meta;
      this.image = image;
      this.animations = meta.animations;
      this.poses = meta.poses;
    }

    static load(jsonUrl) {
      return fetch(jsonUrl, { cache: "no-cache" })
        .then((r) => {
          if (!r.ok) throw new Error(`CatSprite: ${jsonUrl} returned ${r.status}`);
          return r.json();
        })
        .then((meta) => new Promise((resolve, reject) => {
          const img = new Image();
          img.onload = () => resolve(new CatSprite(meta, img));
          img.onerror = () => reject(new Error(`CatSprite: could not load ${meta.image}`));
          img.src = new URL(meta.image, new URL(jsonUrl, document.baseURI)).href;
        }));
    }

    /** Draw frame `index` at (x, y), scaled by whole pixels. */
    drawFrame(ctx, index, x, y, scale) {
      const [sx, sy] = this.meta.frames[index];
      const w = this.meta.frameWidth;
      const h = this.meta.frameHeight;
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(this.image, sx, sy, w, h, x, y, w * scale, h * scale);
    }

    /** A player bound to one canvas. Sizes the canvas to one frame × scale.
     *  Attaching again to the same canvas stops the previous player. */
    attach(canvas, { scale = 4 } = {}) {
      return new Player(this, canvas, scale);
    }
  }

  class Player {
    constructor(cat, canvas, scale) {
      // one player per canvas: a new cat replaces the old one instead of drawing over it
      if (canvas.__catspritePlayer) canvas.__catspritePlayer.stop();
      canvas.__catspritePlayer = this;
      this.cat = cat;
      this.canvas = canvas;
      this.scale = scale;
      canvas.width = cat.meta.frameWidth * scale;
      canvas.height = cat.meta.frameHeight * scale;
      canvas.style.imageRendering = "pixelated";
      this.ctx = canvas.getContext("2d");
      this.raf = null;
      this.current = null;
    }

    _show(index) {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.cat.drawFrame(this.ctx, index, 0, 0, this.scale);
    }

    /** Play an animation. Non-looping ones call onEnd once, holding their last frame. */
    play(name, onEnd) {
      const anim = this.cat.animations[name];
      if (!anim) throw new Error(`CatSprite: no animation "${name}"`);
      this.stop();
      this.current = name;
      // start the clock on the first frame: rAF timestamps can be earlier than performance.now()
      let start = null;
      const step = 1000 / anim.fps;
      const tick = (now) => {
        if (start === null) start = now;
        const i = Math.max(0, Math.floor((now - start) / step));
        if (i >= anim.frames.length && !anim.loop) {
          this._show(anim.frames[anim.frames.length - 1]);
          this.raf = null;
          if (onEnd) onEnd();
          return;
        }
        this._show(anim.frames[i % anim.frames.length]);
        this.raf = requestAnimationFrame(tick);
      };
      this.raf = requestAnimationFrame(tick);
    }

    /** Hold frame `i` of an animation (e.g. the standing frame of "walk/left"). */
    still(name, i = 0) {
      const anim = this.cat.animations[name];
      if (!anim) throw new Error(`CatSprite: no animation "${name}"`);
      this.stop();
      this.current = name;
      this._show(anim.frames[i % anim.frames.length]);
    }

    /** Show one still from a pose set (e.g. "sit/sit", 0). */
    pose(name, i = 0) {
      const set = this.cat.poses[name];
      if (!set) throw new Error(`CatSprite: no pose set "${name}"`);
      this.stop();
      this.current = name;
      this._show(set[i % set.length]);
    }

    stop() {
      if (this.raf) cancelAnimationFrame(this.raf);
      this.raf = null;
    }
  }

  global.CatSprite = CatSprite;
})(window);

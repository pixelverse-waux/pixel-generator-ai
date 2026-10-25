/*
 * viewer.js: the gallery shown at /cats/ and /characters/. Needs catsprite.js.
 *
 *   <div id="app"></div>
 *   <script src="../catsprite.js"></script>
 *   <script src="../viewer.js"></script>
 *   <script>SpriteViewer.mount(document.getElementById("app"), { label: "cat" });</script>
 *
 * Reads index.json next to the page, then <name>.json for the one picked. The pick is kept in
 * the URL hash (/characters/#yellow_bomber), so a link opens that sprite.
 */
(function (global) {
  "use strict";

  const DIRS = ["down", "left", "right", "up"];
  const KEYS = {
    ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up",
    s: "down", a: "left", d: "right", w: "up",
  };
  const STEP = { down: [0, 1], left: [-1, 0], right: [1, 0], up: [0, -1] };

  function el(tag, attrs = {}, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") e.className = v;
      else if (k.startsWith("on")) e[k] = v;
      else e.setAttribute(k, v);
    }
    e.append(...kids);
    return e;
  }

  // whole-pixel scale that makes one frame about `px` big (3 for 32x32 cats, 2 for 64x64 dogs at 96)
  function fit(sprite, px) {
    return Math.max(1, Math.round(px / Math.max(sprite.meta.frameWidth, sprite.meta.frameHeight)));
  }

  // the walk set a sprite moves with: its hand-drawn walk, else the cat_ref move cycle
  function walkSet(sprite) {
    for (const prefix of ["walk", "move"]) {
      if (DIRS.every((d) => sprite.animations[`${prefix}/${d}`])) return prefix;
    }
    return null;
  }

  function mount(root, { label = "sprite" } = {}) {
    const picker = el("div", { class: "picker", role: "group", "aria-label": `Pick a ${label}` });
    const view = el("canvas");
    const now = el("div", { class: "now", "aria-live": "polite" });
    const anims = el("div", { class: "list" });
    const poses = el("div", { class: "list" });
    const posesTitle = el("h2", {}, "Poses");
    const dirs = el("div", { class: "dirs" });
    const dirsTitle = el("h2", {}, "Every direction");
    const strip = el("div", { class: "strip" }, el("canvas"));
    const walker = strip.firstChild;
    const fieldCanvas = el("canvas");
    const field = el("div", { class: "field", tabindex: "0", "aria-label": `Walk the ${label} with the arrow keys or WASD` },
      fieldCanvas, el("div", { class: "hint" }, "Click here, then walk with the arrow keys or WASD"));
    const pad = el("div", { class: "pad" });
    const walkSection = el("div", { class: "section" }, el("h2", {}, "Walk it around"), field, pad);
    const stripSection = el("div", { class: "section" }, el("h2", {}, "Strolling"), strip);

    root.replaceChildren(
      picker,
      el("div", { class: "stage" },
        el("div", { class: "view" }, view, now),
        el("div", {}, dirsTitle, dirs, el("h2", {}, "Animations"), anims, posesTitle, poses)),
      walkSection, stripSection);

    let loading = 0;
    let stripTimer = null;
    let fieldState = null;

    function pressOnly(container, btn) {
      container.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    }

    function buttons(container, names, onPick) {
      container.replaceChildren(...names.map((n) => el("button", {
        "aria-pressed": "false",
        onclick: (e) => {
          [anims, poses].forEach((c) => pressOnly(c, null));
          e.currentTarget.setAttribute("aria-pressed", "true");
          onPick(n);
          now.textContent = n;
        },
      }, n)));
    }

    function showDirections(sprite, prefix) {
      dirsTitle.hidden = dirs.hidden = !prefix;
      if (!prefix) return dirs.replaceChildren();
      dirs.replaceChildren(...DIRS.map((d) => {
        const c = el("canvas");
        sprite.attach(c, { scale: 2 }).play(`${prefix}/${d}`);
        return el("figure", {}, c, el("figcaption", {}, d));
      }));
    }

    // walks back and forth along the strip, turning at the edges
    function startStrip(sprite, prefix) {
      clearInterval(stripTimer);
      stripSection.hidden = !prefix;
      if (!prefix) return;
      const p = sprite.attach(walker, { scale: fit(sprite, 96) });
      strip.style.height = Math.max(96, walker.height) + "px";
      let x = 0, dir = 1;
      p.play(`${prefix}/right`);
      stripTimer = setInterval(() => {
        const max = strip.clientWidth - walker.width;
        x += dir * 2;
        if (x <= 0 || x >= max) {
          dir = -dir;
          x = Math.max(0, Math.min(x, max));
          p.play(`${prefix}/${dir > 0 ? "right" : "left"}`);
        }
        walker.style.left = x + "px";
      }, 40);
    }

    // a little field: held direction keys walk the sprite, letting go leaves it standing
    function startField(sprite, prefix) {
      if (fieldState) cancelAnimationFrame(fieldState.raf);
      walkSection.hidden = !prefix;
      if (!prefix) { fieldState = null; return; }
      const player = sprite.attach(fieldCanvas, { scale: fit(sprite, 96) });
      const s = { player, prefix, x: 0, y: 0, facing: "down", held: [], walking: false, last: null, raf: 0 };
      s.x = (field.clientWidth - fieldCanvas.width) / 2;
      s.y = (field.clientHeight - fieldCanvas.height) / 2;
      player.still(`${prefix}/down`, 0);
      const tick = (t) => {
        const dt = s.last === null ? 0 : Math.min(50, t - s.last);
        s.last = t;
        const dir = s.held[s.held.length - 1];
        if (dir) {
          if (!s.walking || dir !== s.facing) player.play(`${prefix}/${dir}`);
          s.walking = true;
          s.facing = dir;
          const speed = 0.09 * dt;
          s.x = Math.max(0, Math.min(field.clientWidth - fieldCanvas.width, s.x + STEP[dir][0] * speed));
          s.y = Math.max(0, Math.min(field.clientHeight - fieldCanvas.height, s.y + STEP[dir][1] * speed));
        } else if (s.walking) {
          s.walking = false;
          player.still(`${prefix}/${s.facing}`, 0);
        }
        fieldCanvas.style.transform = `translate(${Math.round(s.x)}px, ${Math.round(s.y)}px)`;
        s.raf = requestAnimationFrame(tick);
      };
      s.raf = requestAnimationFrame(tick);
      fieldState = s;
    }

    function hold(dir) {
      if (fieldState && !fieldState.held.includes(dir)) fieldState.held.push(dir);
    }
    function release(dir) {
      if (fieldState) fieldState.held = fieldState.held.filter((d) => d !== dir);
    }

    field.addEventListener("keydown", (e) => {
      const dir = KEYS[e.key] || KEYS[e.key.toLowerCase()];
      if (!dir) return;
      e.preventDefault();
      hold(dir);
    });
    field.addEventListener("keyup", (e) => {
      const dir = KEYS[e.key] || KEYS[e.key.toLowerCase()];
      if (dir) release(dir);
    });
    field.addEventListener("blur", () => { if (fieldState) fieldState.held = []; });
    pad.append(...["left", "up", "down", "right"].map((d) => {
      const b = el("button", { "aria-label": `Walk ${d}` }, { left: "←", up: "↑", down: "↓", right: "→" }[d]);
      b.addEventListener("pointerdown", (e) => { e.preventDefault(); hold(d); });
      ["pointerup", "pointerleave", "pointercancel"].forEach((ev) => b.addEventListener(ev, () => release(d)));
      return b;
    }));

    function show(sprite) {
      // scale the big view so any frame size fits in about 160 px
      const scale = Math.max(1, Math.floor(160 / Math.max(sprite.meta.frameWidth, sprite.meta.frameHeight)));
      const player = sprite.attach(view, { scale });
      const animNames = Object.keys(sprite.animations);
      const poseNames = Object.entries(sprite.poses || {}).flatMap(([k, v]) => v.map((_, i) => `${k}#${i}`));
      buttons(anims, animNames, (n) => player.play(n));
      buttons(poses, poseNames, (n) => { const [k, i] = n.split("#"); player.pose(k, Number(i)); });
      posesTitle.hidden = poses.hidden = !poseNames.length;
      const first = animNames.includes("walk/down") ? "walk/down" : animNames[0];
      player.play(first);
      pressOnly(anims, [...anims.children].find((b) => b.textContent === first));
      now.textContent = first;
      const prefix = walkSet(sprite);
      showDirections(sprite, prefix);
      startStrip(sprite, prefix);
      startField(sprite, prefix);
    }

    // every load gets a ticket; a slower, older load is ignored when it finally arrives
    function open(name) {
      const btn = [...picker.children].find((b) => b.textContent === name);
      if (!btn) return;
      pressOnly(picker, btn);
      if (decodeURIComponent(location.hash.slice(1)) !== name) history.replaceState(null, "", `#${name}`);
      const ticket = ++loading;
      CatSprite.load(`${name}.json`)
        .then((sprite) => { if (ticket === loading) show(sprite); })
        .catch((e) => { if (ticket === loading) now.textContent = e.message; });
    }

    fetch("index.json", { cache: "no-cache" }).then((r) => {
      if (!r.ok) throw new Error(`index.json returned ${r.status}`);
      return r.json();
    }).then((names) => {
      if (!names.length) { now.textContent = `No ${label}s exported yet: run python3 -m pixelkit.web`; return; }
      picker.replaceChildren(...names.map((n) => el("button", { "aria-pressed": "false", onclick: () => open(n) }, n)));
      const wanted = decodeURIComponent(location.hash.slice(1));
      open(names.includes(wanted) ? wanted : names[0]);
      addEventListener("hashchange", () => open(decodeURIComponent(location.hash.slice(1))));
    }).catch(() => {
      now.textContent = "Open this page through a web server, e.g. python3 -m http.server -d web";
    });
  }

  global.SpriteViewer = { mount, walkSet };
})(window);

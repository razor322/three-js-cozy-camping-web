# Rain Fix + Real Textures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rain falls from above the terrain over the camping footprint, and every main asset ships standard GLTF albedo+roughness image textures (256–512px, embedded) with proper UVs — removing repeating-line artifacts.

**Architecture:** Two independent tracks. (1) Pure web fix: rewrite the `useFrame` rain math so drops span y ∈ [terrainTop, terrainTop+15] with wraparound reset, vertical streaks, tiny wind. (2) Blender pipeline: generate ~13 near-neutral PNG textures with a dependency-free pixel painter, wire them into Principled BSDF via Image Texture nodes, add UVs (manual planar for ground, `smart_project` for the rest), export GLB with `export_texcoords=True` + embedded images + `export_vertex_color='NONE'`. Web code loads them untouched via GLTFLoader.

**Tech Stack:** Three.js r186 / R3F v9 (no web deps added), Blender 5.2 background Python (stdlib `zlib`/`struct` PNG encoder — no PIL, no new packages), oxlint + tsc for verification.

## Global Constraints

- Texture sizes: ground/tent/pine **512×512** albedo; rocks/logs/bush/lantern/campfire **256×256**; roughness maps **256×256** (non-color). No 2K/4K. No normal maps.
- Texture files live in `camping-assets/textures/*.png`, embedded into GLB on export.
- Material node graph: `Image Texture → Base Color`, `Image Texture → Roughness`, `Principled BSDF → Output`. No Noise/Wave/Voronoi/procedural nodes, no Blender-only shaders.
- Textures are **near-neutral detail** (mean luma ≈0.9, subtle hue drift); the existing HEX palette stays in `Base Color` as the glTF factor. Preserves current art direction and lets shared materials (foliage used by pine+bush, stone×2, wood×2) reuse one texture without color clashes.
- `Base Color` default set to **white** whenever an albedo texture is connected (otherwise factor×texture double-darkens).
- Ground UV: one non-repeating planar mapping across the full 18×18 (no tiling). Other assets: `bpy.ops.uv.smart_project(angle_limit, island_margin)`.
- Keep vertex colors **out** of the export (`export_vertex_color='NONE'`) — textures own the color; COLOR_0 would multiply and darken. The one thing COLOR_0 currently provides uniquely (campfire log end-caps) must switch to `material_index`.
- No layout/composition changes: `CampingScene.tsx` object positions untouched (RainEffect.tsx is in scope for Task 1).
- Rain: no React state per particle, no new deps, keep `InstancedMesh` + `useFrame`; world-space, identity transform.
- Color: albedo textures `SRGBColorSpace`, roughness linear/non-color (GLTFLoader does this automatically — verify, don't override).
- Perf: rain ≤ 800 instances desktop / 400 mobile; GLB total target ≤ ~1.5 MB (switch `export_image_format='JPEG'`, quality 90 if PNG exceeds).
- Every task ends with: Blender validation script pass, `npm run lint`, `npm run build`.

---

### Task 1: Rain above terrain, falling downward

**Files:**
- Modify: `src/effects/RainEffect.tsx` (useFrame block + constants; lines ~7–11, ~38–56)

**Interfaces:**
- Consumes: store `weather` toggle (unchanged), existing `positions` Float32Array (x,z ∈ ±10, generated once in `useMemo`).
- Produces: same rendered `<instancedMesh>` — no prop/API changes for `CampingScene`.

- [ ] **Step 1: Replace constants**

```ts
const DROP_LEN = 0.5;
const SPEED = 6;            // m/s downward
const AREA = 10;            // ±10 in x/z covers 18×18 terrain + margin
const TERRAIN_TOP = 0.8;    // flat ground top (validated: bbox 0..0.814)
const RAIN_HEIGHT = 15;     // spawn at top+15; column centre ≈ top+7.5 (spec: centre ≈ top+8, height 10–15)
const WIND_X = 0.06;        // spec allows x -0.05..0.1
const WIND_Z = 0.03;        // spec allows z 0..0.05
```
Delete `SLANT_X` (no diagonal storm, no drift term).

- [ ] **Step 2: Keep positions init as-is** (`x = Math.random()*20-10`, `z = Math.random()*20-10` — already the ±10 footprint).

- [ ] **Step 3: Rewrite useFrame particle loop**

```ts
const time = performance.now() * 0.001;
for (let i = 0; i < COUNT; i++) {
  const bx = positions[i * 2];
  const bz = positions[i * 2 + 1];
  // phase grows -> y decreases: velocity.y = -SPEED, wraps top->top+RAIN_HEIGHT
  const phase = (time * SPEED + i * 1.37) % RAIN_HEIGHT;
  const y = TERRAIN_TOP + RAIN_HEIGHT - phase;          // y ∈ [0.8, 15.8] — never below terrain
  const x = ((bx + WIND_X * time + AREA) % (AREA * 2)) - AREA; // wraps inside ±10
  const z = ((bz + WIND_Z * time + AREA) % (AREA * 2)) - AREA;
  dummy.position.set(x, y, z);
  dummy.scale.set(1, DROP_LEN, 1);
  dummy.rotation.set(0, 0, 0);                          // vertical streaks, world-Y fall
  dummy.updateMatrixWorld();
  grp.current.setMatrixAt(i, dummy.matrixWorld);
}
```
Semantics match spec pseudo-code: fall, then reset at top (modulo wrap = identical continuous rainfall). `i * 1.37` decorrelates phases so drops don't fall in lockstep.

- [ ] **Step 4: Build check**

Run: `npm run build`
Expected: `✓ built`, no TS errors.

- [ ] **Step 5: Visual check** — `npm run dev`, toggle **Rain**: streaks visible above/through the scene from tent level up to sky, none clustered under the island, vertical fall, correct while orbiting (world-space mesh, no parent transform).

---

### Task 2: PNG texture generator (no dependencies)

**Files:**
- Create: `blender_build/textures.py` — standalone module; also `exec`'d from `run.py` so builds regenerate textures.

**Interfaces:**
- Produces: `camping-assets/textures/{grass_albedo, grass_rough, soil_albedo, canvas_albedo, canvas_rough, foliage_albedo, foliage_rough, stone_albedo, stone_rough, wood_albedo, wood_rough, metal_albedo, metal_rough}.png` — exact filenames consumed by Task 3's `TEX_ALBEDO`/`TEX_ROUGH` tables.

- [ ] **Step 1: Write dependency-free PNG encoder + noise helpers**

```python
# blender_build/textures.py
import os, math, random, zlib, struct

def write_png(path, w, h, rgb):          # rgb: bytes, w*h*3, 8-bit sRGB
    raw = b''.join(b'\x00' + rgb[y*w*3:(y+1)*w*3] for y in range(h))
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
                + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))

def _h(ix, iy, seed):                    # deterministic hash -> [0,1)
    n = (ix * 374761393 + iy * 668265263 + seed * 2246822519) & 0xffffffff
    n = (n ^ (n >> 13)) * 1274126177 & 0xffffffff
    return ((n ^ (n >> 16)) & 0xffff) / 65535.0

def vnoise(x, y, scale, seed):           # bilinear value noise
    x0, y0 = int(x // scale), int(y // scale)
    fx, fy = (x % scale) / scale, (y % scale) / scale
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)   # smoothstep
    a, b = _h(x0, y0, seed), _h(x0 + 1, y0, seed)
    c, d = _h(x0, y0 + 1, seed), _h(x0 + 1, y0 + 1, seed)
    return (a + (b - a) * fx) * (1 - fy) + (c + (d - c) * fx) * fy

def fbm(x, y, scales, seed):             # octaves, returns 0..1
    v = sum(vnoise(x, y, s, seed + k) for k, s in enumerate(scales))
    return v / len(scales)
```

- [ ] **Step 2: Write the 13 texture painters** — one function per texture, all **near-neutral** (mean luma ≈ 230/255) so Base Color carries the palette:

| file | size | painter recipe |
|---|---|---|
| `grass_albedo` | 512 | base 232 + `fbm(scales=64,16)` ±14 luma + warm/cool hue drift (r×1.03,b×0.97 on odd patches) + ~1800 vertical blade strokes (1–2px wide, 5–12px tall, luma 190 or 245, ±8% green tint) + ~40 soil blobs (r=9px, luma 175 warm) |
| `grass_rough` | 256 | gray `228 + fbm ± 18` |
| `soil_albedo` | 256 | base 225 warm (r>b) + `fbm ± 16` + ~300 pebble dots (2–4px, luma 195/240) |
| `canvas_albedo` | 512 | base 234 + weave: `±5` alternating 4px stripes in x and y + `fbm(scales=32,8)` ±8 |
| `canvas_rough` | 256 | gray `236 ± 15` |
| `foliage_albedo` | 512 | base 230 + `fbm(48,12)` ±16 + ~1400 leaf ellipses (3–8px, random rotation-ish dx/dy, luma 200/245, ±6% hue) |
| `foliage_rough` | 256 | gray `217 ± 20` |
| `stone_albedo` | 256 | base 232 + low-freq `fbm(64,24)` ±22 + fine speckle ±10 + ~60 pits (dark 3px dots) |
| `stone_rough` | 256 | gray `178 ± 26` |
| `wood_albedo` | 256 | base 230 + grain `luma = 230 + 26*sin(y*0.45 + fbm*6)` horizontal + fine noise ±6 + occasional dark streak lines (1px, luma 170, 40–100px long) |
| `wood_rough` | 256 | gray `205 ± 20` |
| `metal_albedo` | 256 | base 210 + vertical brushed streaks (column noise ±10) + `fbm` ±5 |
| `metal_rough` | 256 | gray `165 ± 25` |

- [ ] **Step 3: Add `generate()` entry point**

```python
TEXTURE_DIR = os.path.join(ROOT, 'camping-assets', 'textures')

def generate_textures():
    os.makedirs(TEXTURE_DIR, exist_ok=True)
    for name, (w, h, painter) in TEXTURE_SPECS.items():
        buf = bytearray(w * h * 3)
        painter(buf, w, h)
        write_png(os.path.join(TEXTURE_DIR, name + '.png'), w, h, bytes(buf))
        print('TEX', name, w, 'x', h)
```
`TEXTURE_SPECS` = the table above mapping name → (size, painter fn).

- [ ] **Step 4: Run and verify files**

Run via Blender or plain python (module takes `ROOT` as parameter — no Blender API needed):
Expected: 13 `TEX ...` lines; verify each PNG header (width/height) with an IHDR reader; total bytes < ~1.5 MB.

---

### Task 3: UVs, material wiring, exporter flags

**Files:**
- Modify: `blender_build/common.py` — `get_mat()` (Image Texture nodes), `build_ground()` (manual UV layer), `export_glb()` (flags)
- Modify: `blender_build/batch2.py` — campfire cap → `material_index`
- Modify: `blender_build/run.py` — `generate_textures()` call + `smart_project` for UV-less meshes

**Interfaces:**
- Consumes: Task 2 filenames via tables:
```python
TEX_ALBEDO = {'M_Grass':'grass_albedo','M_Soil':'soil_albedo','M_TentOrange':'canvas_albedo',
  'M_FoliageDark':'foliage_albedo','M_FoliageLight':'foliage_albedo','M_BushMid':'foliage_albedo',
  'M_Stone':'stone_albedo','M_StoneWarm':'stone_albedo','M_Bark':'wood_albedo','M_LogEnd':'wood_albedo',
  'M_LanternMetal':'metal_albedo'}
TEX_ROUGH = {'M_Grass':'grass_rough','M_Soil':'grass_rough','M_TentOrange':'canvas_rough',
  'M_FoliageDark':'foliage_rough','M_FoliageLight':'foliage_rough','M_BushMid':'foliage_rough',
  'M_Stone':'stone_rough','M_StoneWarm':'stone_rough','M_Bark':'wood_rough','M_LogEnd':'wood_rough',
  'M_LanternMetal':'metal_rough'}
```
- Untextured materials keep current simple path: `M_TentCream`, `M_TentTrim`, `M_Pole`, `M_LogRing`, `M_LanternGlass`, `M_LanternLight`, `M_Flame*` (emissive stays as-is per spec §7).
- Produces: GLBs with `TEXCOORD_0` + embedded images + `pbrMetallicRoughness.baseColorTexture`/`roughnessTexture`.

- [ ] **Step 1: `get_mat()` texture branch in `common.py`**

```python
def _tex_image(file, non_color):
    img = bpy.data.images.load(os.path.join(TEXTURE_DIR, file + '.png'), check=True)
    img.colorspace_settings.name = 'Non-Color' if non_color else 'sRGB'
    return img

def get_mat(name):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    albedo = TEX_ALBEDO.get(name)
    rough = TEX_ROUGH.get(name)
    if albedo:
        t = nt.nodes.new('ShaderNodeTexImage')
        t.image = _tex_image(albedo, False)
        t.location = (-360, 200)
        nt.links.new(t.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)   # white factor: texture owns detail
    else:
        bsdf.inputs['Base Color'].default_value = hexrgb(HEX[name])
    if rough:
        t = nt.nodes.new('ShaderNodeTexImage')
        t.image = _tex_image(rough, True)                        # roughness = non-color data
        t.location = (-360, -160)
        nt.links.new(t.outputs['Color'], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = ROUGH.get(name, 0.9)
    bsdf.inputs['Metallic'].default_value = 0.3 if name == 'M_LanternMetal' else 0.0
    if name in EMISSIVE:
        try:
            bsdf.inputs['Emission Color'].default_value = hexrgb(HEX[name])
            bsdf.inputs['Emission Strength'].default_value = 2.0
        except KeyError:
            pass
    return m
```
(`TEXTURE_DIR` from `textures.py`; node lookup by `n.type`, never by localized name.)

- [ ] **Step 2: Manual non-repeating UVs for ground in `build_ground()`** — after each `bake()` call:

```python
def _uv_ground_top(mesh):                # one planar map over the full 18x18, zero tiling
    uv = mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:
        x, depth, _ = mesh.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = ((x + 9.0) / 18.0, (depth + 9.0) / 18.0)

def _uv_ground_sides(mesh):              # u wraps perimeter once, v = height band
    uv = mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:
        x, depth, h = mesh.vertices[loop.vertex_index].co
        u = 0.5 + math.atan2(depth, x) / (2 * math.pi)
        uv.data[loop.index].uv = (u, h / 0.814)
_uv_ground_top(o_top.data)
_uv_ground_sides(o_side.data)
```
Skirt top ring height ≈0.8 ± jitter → v≈1 at top, 0 at bottom; 1-px atan2 seam on soil sides is acceptable (hidden back edge). Mesh stores `(x, depth, height)` — matches the Z-up bake.

- [ ] **Step 3: `run.py` — generate textures + UV the rest**

```python
# textures.py exec'd alongside batch2/batch3 at top of run.py
...
for name in todo:
    ...
    objs, blend_rel, glb_name = fn()
    generate_textures()                  # idempotent, deterministic
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        if o.data.uv_layers: continue    # ground already has manual UVs
        bpy.ops.object.select_all(action='DESELECT')
        o.select_set(True); bpy.context.view_layer.objects.active = o
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.03)
        bpy.ops.object.mode_set(mode='OBJECT')
    # then existing transform_apply loop, then lift loop (order already fixed)
```

- [ ] **Step 4: Campfire end-caps via `material_index` (replaces vertex-color-only coloring)** — in `batch2.py` cap recolor block:

```python
    for poly in m.polygons:
        if max(abs(m.vertices[vi].co.z) for vi in poly.vertices) > L/2 - 0.02:
            poly.material_index = 1      # M_LogEnd (slot 1)
```
(`v.z` check valid: object rotation still unapplied, cylinder axis = local Z.)

- [ ] **Step 5: Exporter flags in `export_glb()`**

```python
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
        export_yup=True, export_materials='EXPORT', export_image_format='AUTO',
        export_texcoords=True, export_normals=True,
        export_vertex_color='NONE', export_animations=anim)
```
(`'NONE'` → `'AUTO'` embeds images; `export_texcoords` False → True; drop `export_vertex_color='NAME'` + `export_all_vertex_colors`. If final GLB set > ~1.5 MB: `export_image_format='JPEG', export_image_quality=90`.)

- [ ] **Step 6: Rebuild everything**

Run: `& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python blender_build\run.py -- all`
Expected: 8 × `SAVED`, 13 × `TEX`, no Tracebacks.

---

### Task 4: Validate GLBs (test gate)

**Files:**
- Create/Modify: `tools/validate_glb.py` (project-side validation script; supersedes ad-hoc temp copies)

**Interfaces:**
- Consumes: the 8 GLBs from Task 3.
- Produces: per-file PASS/FAIL report (stdout + exit code).

- [ ] **Step 1: Validation script checks** — for each primitive:
```python
attrs = p['attributes']
assert 'TEXCOORD_0' in attrs, name + ': missing UVs'
assert 'COLOR_0' not in attrs, name + ': vertex colors still exported'
pbr = js['materials'][p['material']]['pbrMetallicRoughness']
if textured: assert 'baseColorTexture' in pbr and 'roughnessTexture' in pbr
uv_acc = js['accessors'][attrs['TEXCOORD_0']]
assert 0 <= uv_acc['min'][0] <= 1 and 0 <= uv_acc['max'][0] <= 1  # same for [1]
# plus: ground bbox 18x18x0.814 unchanged, issues==[] (loose/dup/normal checks), images>0 for textured GLBs
```
Simple-material meshes (flames, glass, trim, poles, cream) may lack textures — whitelist them.

- [ ] **Step 2: Run over all 8 GLBs**
Expected: every assert passes; report per-file KB (total ≤ ~1.5 MB, else apply JPEG switch in Task 3 Step 5 and re-run).

- [ ] **Step 3: Ground-specific** — silhouette script: shape unchanged; `Ground_Top` bbox still z ∈ [0.785, 0.814].

---

### Task 5: Web-side color management + no-override verification

**Files:**
- Read-only verification of `src/scenes/camping/models.tsx` (`hygiene()`), `src/effects/Environment.tsx`, `src/scenes/camping/CampingScene.tsx`; `npm run lint` + `npm run build`.

- [ ] **Step 1: Confirm no material override** — grep for `material = new` / wholesale traverse replacement: only allowed hits are lantern glow clone (`models.tsx:261`, specific reason) and rain's own material. No code change expected (hygiene only toggles `flatShading`).
- [ ] **Step 2: Confirm color spaces** — R3F v9/three r186 defaults: `renderer.outputColorSpace = SRGBColorSpace`; `GLTFLoader` tags baseColor textures sRGB and roughness/metallic linear automatically. No code change unless a render shows washed/dark colors (then set `gl.outputColorSpace` once in Canvas).
- [ ] **Step 3: lint + build** — `npm run lint` exit 0, `npm run build` `✓ built`.

---

### Task 6: Performance + visual QA sign-off

- [ ] **Step 1: Size/perf numbers** — GLB sizes (expect ~0.5–1.5 MB total); rain instances 800/400; `package.json` diff empty.
- [ ] **Step 2: Walk spec §19 checklist in dev** — rain boxes (above/vertical/footprint/reset/orbit-safe) + texture boxes (embedded, UV'd, no line artifacts on ground, natural grass, canvas tent, stone rocks, wood logs, foliage variation) + visual boxes (low-poly preserved, composition unchanged, soft lighting) — user does the eyeball pass (agent cannot view renders).
- [ ] **Step 3: Optional polish only if requested** — JPEG export if size demands, texture tuning, lighting touch-ups (spec §14: no over-lighting compensation).

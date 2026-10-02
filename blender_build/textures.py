"""Procedural PNG texture generator (stdlib only, no bpy). Run: python textures.py
Writes 13 8-bit RGB maps into camping-assets/textures/ for the Principled BSDF
materials. All maps are near-neutral detail (~230/255 mean luma): the HEX palette
stays in Base Color as the glTF factor, so one map can serve several materials.
Deterministic: fixed seeds -> byte-identical output every run.
"""
import os, math, random, zlib, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTURE_DIR = os.path.join(ROOT, 'camping-assets', 'textures')

# ---------------------------------------------------------------- png + noise

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

def _d(fbmv, amp):                       # fbm 0..1 -> -amp..+amp
    return (fbmv - 0.5) * 2 * amp

# ---------------------------------------------------------------- pixel prims

def _put(buf, w, h, x, y, luma, tint=(1.0, 1.0, 1.0)):
    """One clamped pixel; tint drifts hue around the near-neutral luma."""
    if not (0 <= x < w and 0 <= y < h):
        return
    i = (y * w + x) * 3
    for k, t in enumerate(tint):
        v = int(luma * t + 0.5)
        buf[i + k] = 0 if v < 0 else (255 if v > 255 else v)

def _fill(buf, w, h, shade):
    """shade(x, y) -> (luma, tint)"""
    for y in range(h):
        for x in range(w):
            l, t = shade(x, y)
            _put(buf, w, h, x, y, l, t)

def _disc(buf, w, h, cx, cy, r, luma, tint=(1.0, 1.0, 1.0)):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                _put(buf, w, h, x, y, luma, tint)

def _ellipse(buf, w, h, cx, cy, rx, ry, luma, tint=(1.0, 1.0, 1.0)):
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                _put(buf, w, h, x, y, luma, tint)

def _vbar(buf, w, h, x, y, thick, length, luma, tint=(1.0, 1.0, 1.0)):
    """Vertical streak: one grass blade / column-noise stroke."""
    for dy in range(length):
        for dx in range(thick):
            _put(buf, w, h, x + dx, y + dy, luma, tint)

def _hbar(buf, w, h, x, y, length, luma, tint=(1.0, 1.0, 1.0)):
    for dx in range(length):
        _put(buf, w, h, x + dx, y, luma, tint)

# ---------------------------------------------------------------- painters

def grass_albedo(buf, w, h):
    rng = random.Random(11)
    def shade(x, y):
        warm = vnoise(x, y, 128, 71) < 0.5
        return 232 + _d(fbm(x, y, (64, 16), 3), 14), \
               (1.03, 1.0, 0.97) if warm else (0.97, 1.0, 1.03)
    _fill(buf, w, h, shade)
    for _ in range(1800):                      # vertical blade strokes
        g = 1.0 + rng.uniform(-0.08, 0.08)
        _vbar(buf, w, h, rng.randrange(w), rng.randrange(h), rng.choice((1, 1, 2)),
              rng.randint(5, 12), rng.choice((190, 245)), (1.0, g, 1.0))
    for _ in range(40):                        # bare soil showing through
        _disc(buf, w, h, rng.randrange(w), rng.randrange(h), 9, 175, (1.06, 1.0, 0.88))

def grass_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (228 + _d(fbm(x, y, (64, 16), 5), 18), (1, 1, 1)))

def soil_albedo(buf, w, h):
    rng = random.Random(12)
    def shade(x, y):
        return 225 + _d(fbm(x, y, (32, 10), 7), 16), (1.04, 1.0, 0.92)
    _fill(buf, w, h, shade)
    for _ in range(300):                       # pebble dots
        _disc(buf, w, h, rng.randrange(w), rng.randrange(h), rng.randint(2, 4),
              rng.choice((195, 240)), (1.03, 1.0, 0.95))

def canvas_albedo(buf, w, h):
    def shade(x, y):
        weave = (5 if (x // 4) % 2 else -5) + (5 if (y // 4) % 2 else -5)
        return 234 + weave + _d(fbm(x, y, (32, 8), 13), 8), (1, 1, 1)
    _fill(buf, w, h, shade)

def canvas_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (236 + _d(fbm(x, y, (48, 16), 17), 15), (1, 1, 1)))

def foliage_albedo(buf, w, h):
    rng = random.Random(14)
    def shade(x, y):
        t = (_h(x, y, 23) - 0.5) * 0.12      # deterministic per-pixel hue drift
        return 230 + _d(fbm(x, y, (48, 12), 19), 16), (1 + t, 1 + t, 1 - t)
    _fill(buf, w, h, shade)
    for _ in range(1400):                      # leaf ellipses
        rx = rng.randint(3, 8); ry = max(2, rx + rng.randint(-2, 3))
        t = rng.uniform(-0.06, 0.06)
        _ellipse(buf, w, h, rng.randrange(w), rng.randrange(h), rx, ry,
                 rng.choice((200, 245)), (1 + t, 1 + t, 1 - t))

def foliage_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (217 + _d(fbm(x, y, (48, 12), 29), 20), (1, 1, 1)))

def stone_albedo(buf, w, h):
    rng = random.Random(16)
    def shade(x, y):
        speckle = (_h(x, y, 31) - 0.5) * 20
        return 232 + _d(fbm(x, y, (64, 24), 37), 22) + speckle, (1, 1, 1)
    _fill(buf, w, h, shade)
    for _ in range(60):                        # pits
        _disc(buf, w, h, rng.randrange(w), rng.randrange(h), 3, 150, (1, 1, 1))

def stone_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (178 + _d(fbm(x, y, (64, 24), 41), 26), (1, 1, 1)))

def wood_albedo(buf, w, h):
    rng = random.Random(18)
    def shade(x, y):
        grain = 230 + 26 * math.sin(y * 0.45 + fbm(x, y, (16, 4), 43) * 6)
        return grain + (_h(x, y, 47) - 0.5) * 12, (1, 1, 1)
    _fill(buf, w, h, shade)
    for _ in range(18):                        # dark streaks along the grain
        _hbar(buf, w, h, rng.randrange(w), rng.randrange(h), rng.randint(40, 100),
              170, (1.0, 0.97, 0.93))

def wood_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (205 + _d(fbm(x, y, (32, 8), 53), 20), (1, 1, 1)))

def metal_albedo(buf, w, h):
    def shade(x, y):
        brushed = (_h(x, 0, 59) - 0.5) * 20   # constant per column -> vertical streaks
        return 210 + brushed + _d(fbm(x, y, (64, 16), 61), 5), (1, 1, 1)
    _fill(buf, w, h, shade)

def metal_rough(buf, w, h):
    _fill(buf, w, h, lambda x, y: (165 + _d(fbm(x, y, (64, 16), 67), 25), (1, 1, 1)))

# ---------------------------------------------------------------- entry point

TEXTURE_SPECS = {
  'grass_albedo':   (512, grass_albedo),   'canvas_albedo':  (512, canvas_albedo),
  'foliage_albedo': (512, foliage_albedo),
  'grass_rough':    (256, grass_rough),    'soil_albedo':    (256, soil_albedo),
  'canvas_rough':   (256, canvas_rough),   'foliage_rough':  (256, foliage_rough),
  'stone_albedo':   (256, stone_albedo),   'stone_rough':    (256, stone_rough),
  'wood_albedo':    (256, wood_albedo),    'wood_rough':     (256, wood_rough),
  'metal_albedo':   (256, metal_albedo),   'metal_rough':    (256, metal_rough),
}

def generate_textures():
    os.makedirs(TEXTURE_DIR, exist_ok=True)
    for name, (size, painter) in TEXTURE_SPECS.items():
        buf = bytearray(size * size * 3)
        painter(buf, size, size)
        write_png(os.path.join(TEXTURE_DIR, name + '.png'), size, size, bytes(buf))
        print('TEX', name, size, 'x', size)

def _ihdr(path):                              # re-read the written header
    with open(path, 'rb') as f:
        head = f.read(26)
    assert head[:8] == b'\x89PNG\r\n\x1a\n', 'bad signature: ' + path
    assert head[12:16] == b'IHDR', 'missing IHDR: ' + path
    w, h, depth, ctype = struct.unpack('>IIBB', head[16:26])
    return w, h, depth, ctype

if __name__ == '__main__':
    generate_textures()
    total = 0
    for name, (size, _) in TEXTURE_SPECS.items():
        path = os.path.join(TEXTURE_DIR, name + '.png')
        w, h, depth, ctype = _ihdr(path)
        assert (w, h) == (size, size), '%s is %dx%d, expected %d' % (name, w, h, size)
        assert (depth, ctype) == (8, 2), '%s is depth %d type %d' % (name, depth, ctype)
        total += os.path.getsize(path)
    assert total < 1_572_864, 'total %d bytes over 1.5 MB' % total
    print('PASS %d files, %d bytes (%.1f KB)' % (len(TEXTURE_SPECS), total, total / 1024))
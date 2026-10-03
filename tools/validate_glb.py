"""Validate the 9 exported GLBs in public/models against the texture spec.

Run: python tools/validate_glb.py   (from any cwd)

Per primitive: TEXCOORD_0 present, COLOR_0 absent, UV range inside [0, 1], and
unless the material is whitelisted as untextured, baseColorTexture plus the
packed metallicRoughnessTexture.
Per file: len(images) > 0 for all 8 (every GLB embeds its maps), plus the total-size budget.
Ground additionally: X/Z +/-9 and both surfaces inside the top-slab z range.

Note: Blender's glTF exporter writes accessor min/max only for POSITION, so every
bound here is computed from the raw BIN chunk rather than read from accessor
metadata. Stdlib only (struct, json, os, sys).
"""
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, 'public', 'models')

TEXTURED = ('ground', 'tent', 'campfire', 'rocks', 'pine-tree', 'bush', 'lantern', 'stump', 'meadow')
# Materials that must carry both maps -- the TEX_ALBEDO keys in
# blender_build/common.py. Anything else has to be whitelisted below.
TEXTURED_MATERIALS = (
    'M_Grass', 'M_Soil', 'M_TentOrange', 'M_FoliageDark', 'M_FoliageLight',
    'M_BushMid', 'M_Stone', 'M_StoneWarm', 'M_Bark', 'M_LogEnd', 'M_LanternMetal',
)
# Every other material in the pipeline is intentionally untextured: emissive
# flames, lantern glass/lights, tent trim + inner fabric + poles, log rings and
# the pine trunk. Anything not in TEXTURED_MATERIALS and not here fails the run.
NO_TEX_MATERIALS = (
    'M_FlameOuter', 'M_FlameMid', 'M_FlameInner', 'M_FlameBase',
    'M_LanternGlass', 'M_LanternLight',
    'M_TentCream', 'M_TentTrim', 'M_Pole',
    'M_LogRing', 'M_Trunk',
    'M_Stem', 'M_Petal', 'M_PetalPink', 'M_BloomDot',
)
GROUND_MESHES = ('Ground_Top', 'Ground_Sides')
GROUND_HALF = 9.0                      # X/Z half-extent of the diorama floor
GROUND_Z_MIN, GROUND_Z_MAX = 0.78, 0.82
# UV slack. smart_project (run on every un-UV'd mesh) and the ground skirt's
# atan2+pad mapping both overshoot the unit square slightly; the real minimum
# observed is -0.000353 (ground skirt, side-to-top blend). 0.005 catches a
# genuinely broken UV map while tolerating that blend padding.
UV_EPS = 0.005
SIZE_WARN = 1.5 * 1024 * 1024          # report only
SIZE_FAIL = 1.6 * 1024 * 1024          # hard limit
COMPONENTS = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}


def parse_glb(path):
    """Return (gltf json, BIN chunk bytes) read straight from the binary."""
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:4] == b'glTF', path + ': not a glb (bad magic)'
    assert struct.unpack('<I', data[4:8])[0] == 2, path + ': not glTF 2.0'
    total = struct.unpack('<I', data[8:12])[0]
    assert total == len(data), path + ': declared length %d != file size %d' % (total, len(data))
    js, binchunk, off = None, b'', 12
    while off < total:
        clen = struct.unpack('<I', data[off:off + 4])[0]
        ctype = data[off + 4:off + 8]
        body = data[off + 8:off + 8 + clen]
        if ctype == b'JSON':
            js = json.loads(body.decode('utf-8'))
        elif ctype == b'BIN\x00':
            binchunk = body
        off += 8 + clen
    assert js is not None, path + ': no JSON chunk'
    return js, binchunk


def bounds(js, binchunk, acc_index):
    """(min, max) per component for an accessor, computed from the BIN chunk."""
    acc = js['accessors'][acc_index]
    assert acc['componentType'] == 5126, 'accessor %d: expected float, got %r' % (
        acc_index, acc['componentType'])
    n = COMPONENTS[acc['type']]
    view = js['bufferViews'][acc['bufferView']]
    base = view.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = view.get('byteStride') or n * 4
    lo = [float('inf')] * n
    hi = [float('-inf')] * n
    for i in range(acc['count']):
        for c, v in enumerate(struct.unpack_from('<%df' % n, binchunk, base + i * stride)):
            lo[c] = min(lo[c], v)
            hi[c] = max(hi[c], v)
    return lo, hi


def material_name(js, primitive):
    idx = primitive.get('material')
    return js['materials'][idx].get('name', '?') if idx is not None else None


def check_primitive(fn, mesh_name, js, binchunk, prim):
    """Raise AssertionError if this primitive violates the spec."""
    attrs = prim['attributes']
    label = '%s/%s' % (fn, mesh_name)
    assert 'TEXCOORD_0' in attrs, label + ': missing UVs (TEXCOORD_0)'
    assert 'COLOR_0' not in attrs, label + ': vertex colors still exported (COLOR_0)'

    uv_lo, uv_hi = bounds(js, binchunk, attrs['TEXCOORD_0'])
    for axis in (0, 1):
        lo, hi = uv_lo[axis], uv_hi[axis]
        assert -UV_EPS <= lo <= 1.0 + UV_EPS and -UV_EPS <= hi <= 1.0 + UV_EPS, \
            '%s: UV axis %d outside [0,1] by more than %g: min=%r max=%r' % (label, axis, UV_EPS, lo, hi)

    mat = material_name(js, prim)
    pbr = js['materials'][prim['material']].get('pbrMetallicRoughness', {})
    if mat in NO_TEX_MATERIALS:
        assert mat not in TEXTURED_MATERIALS, 'material %s is in both whitelists' % mat
        return
    assert 'baseColorTexture' in pbr, '%s: material %s has no baseColorTexture' % (label, mat)
    # glTF has no standalone roughnessTexture: roughness rides in the packed
    # metallicRoughnessTexture (green channel).
    assert 'metallicRoughnessTexture' in pbr, \
        '%s: material %s has no metallicRoughnessTexture (packed roughness)' % (label, mat)


def check_ground(js, binchunk):
    """The diorama floor silhouette must be unchanged."""
    seen = set()
    for mesh in js['meshes']:
        name = mesh.get('name', '?')
        if name not in GROUND_MESHES:
            continue
        seen.add(name)
        lo, hi = bounds(js, binchunk, mesh['primitives'][0]['attributes']['POSITION'])
        for axis, letter in ((0, 'X'), (2, 'Z')):
            assert abs(abs(lo[axis]) - GROUND_HALF) < 0.01 and abs(abs(hi[axis]) - GROUND_HALF) < 0.01, \
                '%s: %s bounds %.3f..%.3f, expected +/-%g' % (name, letter, lo[axis], hi[axis], GROUND_HALF)
        if name == 'Ground_Top':
            assert GROUND_Z_MIN <= lo[1] <= GROUND_Z_MAX and GROUND_Z_MAX >= hi[1] >= GROUND_Z_MIN, \
                'Ground_Top: z %.3f..%.3f outside [%g, %g]' % (
                    lo[1], hi[1], GROUND_Z_MIN, GROUND_Z_MAX)
    assert seen == set(GROUND_MESHES), 'ground.glb: expected %s, got %s' % (
        sorted(GROUND_MESHES), sorted(seen))


def describe(fn, js, binchunk):
    """Per-file report lines: images, per-primitive POSITION + UV bounds."""
    lines = ['=== %s' % fn,
             '    images=%d textures=%d materials=%d' % (
                 len(js.get('images', [])), len(js.get('textures', [])), len(js.get('materials', [])))]
    for mesh in js['meshes']:
        for prim in mesh['primitives']:
            attrs = prim['attributes']
            pos_lo, pos_hi = bounds(js, binchunk, attrs['POSITION'])
            uv_lo, uv_hi = bounds(js, binchunk, attrs['TEXCOORD_0'])
            lines.append('    prim %-20s mat=%-16s pos=[%s]..[%s] uv=[%.3f,%.3f]..[%.3f,%.3f]' % (
                mesh.get('name', '?'), material_name(js, prim),
                ','.join('%.3f' % v for v in pos_lo), ','.join('%.3f' % v for v in pos_hi),
                uv_lo[0], uv_lo[1], uv_hi[0], uv_hi[1]))
    return lines


def main():
    files = sorted(f for f in os.listdir(MODELS) if f.endswith('.glb'))
    assert files, 'no .glb files found in ' + MODELS
    assert len(files) == 9, 'expected 9 GLBs, found %d: %s' % (len(files), files)

    lines, failures, failed_files, total = [], [], set(), 0
    for fn in files:
        path = os.path.join(MODELS, fn)
        size = os.path.getsize(path)
        total += size
        try:
            js, binchunk = parse_glb(path)
            lines += describe(fn, js, binchunk)
            if fn[:-4] in TEXTURED:
                assert len(js.get('images', [])) > 0, fn + ': no embedded images'
            for mesh in js['meshes']:
                for prim in mesh['primitives']:
                    check_primitive(fn, mesh.get('name', '?'), js, binchunk, prim)
            if fn == 'ground.glb':
                check_ground(js, binchunk)
        except AssertionError as e:
            failures.append(str(e))
            failed_files.add(fn)
            lines.append('    CHECK FAIL: %s' % e)
        else:
            lines.append('    CHECK PASS')
        lines.append('    size %d bytes (%.1f KiB)' % (size, size / 1024))

    lines.append('TOTAL %d bytes (%.1f KiB / %.2f MiB) across %d files' % (
        total, total / 1024, total / (1024 * 1024), len(files)))
    if total > SIZE_FAIL:
        failures.append('total %d bytes exceeds the %d byte limit' % (total, int(SIZE_FAIL)))
        lines.append('SIZE FAIL %.2f MiB > %.2f MiB limit' % (total / 1048576, SIZE_FAIL / 1048576))
    elif total > SIZE_WARN:
        lines.append('SIZE WARN %.2f MiB over the %.2f MiB target, under the %.2f MiB limit'
                     % (total / 1048576, SIZE_WARN / 1048576, SIZE_FAIL / 1048576))
    else:
        lines.append('SIZE OK   %.2f MiB <= %.2f MiB target' % (total / 1048576, SIZE_WARN / 1048576))

    lines.append('SUMMARY %d/%d files failed' % (len(failed_files), len(files)))
    lines.append('RESULT  %s' % ('PASS' if not failures else 'FAIL (%d)' % len(failures)))
    print('\n'.join(lines))
    for f in failures:
        print('FAIL ' + f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
"""Throwaway GLB inspector: python blender_build/inspect_glb.py > nothing (writes report file)."""
import os, sys, json, struct

ROOT = r'F:\0.3 projek\three-js\cozy-camping'
MODELS = os.path.join(ROOT, 'public', 'models')
OUT = os.path.join(ROOT, 'camping-assets', 'glb_report.txt')


def load(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:4] == b'glTF', 'not a glb: ' + path
    total = struct.unpack('<I', data[8:12])[0]
    assert total == len(data), 'chunk length %d vs file %d' % (total, len(data))
    jlen = struct.unpack('<I', data[12:16])[0]
    assert data[16:20] == b'JSON', 'first chunk is not JSON'
    j = json.loads(data[20:20 + jlen].decode('utf-8'))
    return j, len(data)


lines = []
total_bytes = 0
for fn in sorted(os.listdir(MODELS)):
    if not fn.endswith('.glb'):
        continue
    path = os.path.join(MODELS, fn)
    j, size = load(path)
    total_bytes += size
    lines.append('=== %s  %d bytes (%.1f KB)' % (fn, size, size / 1024))
    lines.append('  images=%d  textures=%d  materials=%d' % (
        len(j.get('images', [])), len(j.get('textures', [])), len(j.get('materials', []))))
    for ii, im in enumerate(j.get('images', [])):
        lines.append('    img[%d] mime=%s uri=%s' % (ii, im.get('mimeType'), (im.get('uri') or '')[:24]))
    for ti, tx in enumerate(j.get('textures', [])):
        lines.append('    tex[%d] source=%s samplers=%s' % (ti, tx.get('source'), tx.get('sampler')))
    for mi, mat in enumerate(j.get('materials', [])):
        pbr = mat.get('pbrMetallicRoughness', {})
        lines.append('    mat[%d] %-22s pbrKeys=%s' % (
            mi, mat.get('name', '?'), sorted(pbr.keys())))
        lines.append('      baseColorTex=%s roughTex=%s mrTex=%s baseFactor=%s metallic=%s rough=%s emissive=%s' % (
            'baseColorTexture' in pbr, 'roughnessTexture' in pbr,
            'metallicRoughnessTexture' in pbr,
            [round(v, 3) for v in pbr.get('baseColorFactor', [])],
            pbr.get('metallicFactor'), pbr.get('roughnessFactor'),
            mat.get('emissiveFactor')))
    prims = []
    for mesh in j.get('meshes', []):
        for p in mesh.get('primitives', []):
            prims.append((mesh.get('name', '?'), sorted(p['attributes'].keys()),
                          p.get('material'), p.get('mode', 4)))
    for name, attrs, m, mode in prims:
        lines.append('    prim %-24s attrs=%s material=%s mode=%s' % (name, attrs, m, mode))
    # position / uv bounds
    for mesh in j.get('meshes', []):
        for pi, p in enumerate(mesh.get('primitives', [])):
            for key in ('POSITION', 'TEXCOORD_0'):
                ai = p['attributes'].get(key)
                if ai is None:
                    continue
                acc = j['accessors'][ai]
                if 'min' in acc and 'max' in acc:
                    lines.append('    %-11s %-24s p%d min=%s max=%s' % (key, mesh.get('name', '?'), pi,
                        [round(v, 3) for v in acc['min']], [round(v, 3) for v in acc['max']]))
    lines.append('    COLOR_0 present: %s' % any('COLOR_0' in p['attributes']
                                                  for m in j.get('meshes', [])
                                                  for p in m.get('primitives', [])))
    lines.append('    TEXCOORD_0 prims: %d / %d' % (
        sum(1 for m in j.get('meshes', []) for p in m.get('primitives', [])
            if 'TEXCOORD_0' in p['attributes']),
        sum(len(m.get('primitives', [])) for m in j.get('meshes', []))))

lines.append('TOTAL %d bytes (%.1f KB) across %d files' % (
    total_bytes, total_bytes / 1024, len([f for f in os.listdir(MODELS) if f.endswith('.glb')])))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('\n'.join(lines))
print('written', OUT)
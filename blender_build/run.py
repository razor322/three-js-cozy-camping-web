"""Runner: blender --background --python run.py -- <asset|all>"""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
exec(open(os.path.join(os.path.dirname(__file__),'common.py')).read())
exec(open(os.path.join(os.path.dirname(__file__),'textures.py')).read())
exec(open(os.path.join(os.path.dirname(__file__),'batch2.py')).read())
exec(open(os.path.join(os.path.dirname(__file__),'batch3.py')).read())

def uv_mesh(o):
    """smart_project for meshes that arrive without a UV layer (ground gets
    its manual non-repeating map inside build_ground)."""
    if o.data.uv_layers: return
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.03)
    bpy.ops.object.mode_set(mode='OBJECT')
    o.select_set(False)

ARGS = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['all']
BUILDERS = {'ground':build_ground,'tent':build_tent,'campfire':build_campfire,'rocks':build_rocks,
 'pine-tree':build_pine,'bush':build_bush,'lantern':build_lantern,'stump':build_stump}
todo = list(BUILDERS) if 'all' in ARGS else ARGS
generate_textures()              # idempotent, deterministic; must precede get_mat()
for name in todo:
    fn = BUILDERS[name]
    clear()
    print('=== BUILD', name, '===')
    objs, blend_rel, glb_name = fn()
    for o in bpy.data.objects:
        if o.type == 'MESH': uv_mesh(o)
    # apply transforms FIRST so lift measures world height, not local
    for o in objs:
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        try: bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        except RuntimeError: pass
        o.select_set(False)
    for o in objs:
        lift_to_zero(o)
        o.select_set(False)
    bp = os.path.join(ROOT,'camping-assets',blend_rel)
    os.makedirs(os.path.dirname(bp), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=bp)
    gp = os.path.join(ROOT,'public','models',glb_name)
    export_glb(objs, gp)
    tris = 0
    for o in objs:
        me = o.data
        if hasattr(me,'polygons'): tris += sum(len(p.vertices)-2 for p in me.polygons)
    print('SAVED', bp, gp, 'tris=', tris)
print('DONE', todo)

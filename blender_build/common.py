"""Cozy camping GLB builder. Run: blender --background --python build_assets.py -- <asset|all>
Assets: ground tent campfire rocks pine-tree bush lantern stump
GLOBAL RULES: stylized low-poly, flat shading, matte. No textures. M_ materials.
Scale 1 unit=1m. Origin bottom-center. +Y up, front +Z. Transforms applied (identity).
"""
import bpy, math, random, sys
from mathutils import Matrix, Vector

ARGS = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['all']

ROOT = r'F:\0.3 projek\three-js\cozy-camping'
HEX = {
 'M_Grass':'7FA650','M_GrassPatch':'6E9A45','M_Soil':'6B4A32',
 'M_FoliageDark':'2F5D3A','M_FoliageLight':'3F7A47','M_BushMid':'4E8B4F',
 'M_Trunk':'6B4B35','M_Bark':'7A5638','M_LogEnd':'B88A5E','M_LogRing':'8A5E3B',
 'M_TentOrange':'E07A2F','M_TentCream':'F3E3C3','M_TentTrim':'4A3426','M_Pole':'5A4030',
  'M_Stone':'8A8680','M_StoneWarm':'8C7F72',
  'M_Stem':'4E7A3A','M_Petal':'F5EFE0','M_PetalPink':'E88CA0','M_BloomDot':'FFD84A',
 'M_FlameOuter':'FF7A1A','M_FlameMid':'FFA928','M_FlameInner':'FFD84A','M_FlameBase':'D9560F',
 'M_LanternMetal':'3E3A2E','M_LanternGlass':'F6E6BF','M_LanternLight':'FFC95C',
}
EMISSIVE = {'M_FlameOuter','M_FlameMid','M_FlameInner','M_FlameBase','M_LanternLight'}
ROUGH = {'M_LanternMetal':0.6,'M_LanternGlass':0.4}
GLASSY = {'M_LanternGlass'}
# Maps are near-neutral detail (~230/255), so one map serves several materials.
# The palette still rides Base Color: a direct Image Texture -> Base Color link
# makes the glTF exporter DROP baseColorFactor (texture then multiplies against
# white and the HEX is gone), so the colour must reach Base Color through a
# ShaderNodeMix multiply -- the exporter then reads the constant as the factor.
TEX_ALBEDO = {'M_Grass':'grass_albedo','M_Soil':'soil_albedo','M_TentOrange':'canvas_albedo',
  'M_FoliageDark':'foliage_albedo','M_FoliageLight':'foliage_albedo','M_BushMid':'foliage_albedo',
  'M_Stone':'stone_albedo','M_StoneWarm':'stone_albedo','M_Bark':'wood_albedo','M_LogEnd':'wood_albedo',
  'M_LanternMetal':'metal_albedo'}
TEX_ROUGH = {'M_Grass':'grass_rough','M_Soil':'grass_rough','M_TentOrange':'canvas_rough',
  'M_FoliageDark':'foliage_rough','M_FoliageLight':'foliage_rough','M_BushMid':'foliage_rough',
  'M_Stone':'stone_rough','M_StoneWarm':'stone_rough','M_Bark':'wood_rough','M_LogEnd':'wood_rough',
  'M_LanternMetal':'metal_rough'}

def hexrgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1.0,)

def _tex_image(file, non_color):
    img = bpy.data.images.load(os.path.join(TEXTURE_DIR, file + '.png'), check_existing=True)
    img.colorspace_settings.name = 'Non-Color' if non_color else 'sRGB'
    return img

def _tex_link(nt, bsdf, file, non_color, socket, loc):
    t = nt.nodes.new('ShaderNodeTexImage')
    t.image = _tex_image(file, non_color)
    t.location = loc
    nt.links.new(t.outputs['Color'], bsdf.inputs[socket])

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
        t.location = (-700, 260)
        rgb = nt.nodes.new('ShaderNodeRGB')
        rgb.outputs[0].default_value = hexrgb(HEX[name])
        rgb.location = (-700, 20)
        mix = nt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.location = (-440, 200)
        nt.links.new(t.outputs['Color'], mix.inputs[6])      # A
        nt.links.new(rgb.outputs[0], mix.inputs[7])          # B
        mix.inputs[0].default_value = 1.0                     # Factor
        nt.links.new(mix.outputs[2], bsdf.inputs['Base Color'])  # Result (RGBA)
    else:
        bsdf.inputs['Base Color'].default_value = hexrgb(HEX[name])
    if rough:
        _tex_link(nt, bsdf, rough, True, 'Roughness', (-360, -160))
    else:
        bsdf.inputs['Roughness'].default_value = ROUGH.get(name, 0.9)
    bsdf.inputs['Metallic'].default_value = 0.3 if name=='M_LanternMetal' else 0.0
    if name in EMISSIVE:
        try:
            bsdf.inputs['Emission Color'].default_value = hexrgb(HEX[name])
            bsdf.inputs['Emission Strength'].default_value = 2.0
        except KeyError:
            pass
    return m

class MB:
    """Mesh builder with per-corner colors and auto winding fix."""
    def __init__(self):
        self.v=[]; self.f=[]; self.mi=[]; self.fc=[]; self.want=[]
    def corner(self, co, col):
        x,y,z = co
        self.v.append((x,z,y)); return len(self.v)-1
    def face(self, cos, mat, col, want):
        idx=[self.corner(p, col) for p in cos]
        self.f.append(tuple(idx)); self.mi.append(mat); self.fc.append(col); self.want.append(tuple(want))
    def tri(self, a,b,c, mat, col, want): self.face([a,b,c], mat, col, want)
    def quad(self, a,b,c,d, mat, col, want): self.face([a,b,c,d], mat, col, want)
    def cuboid(self, c0, c1, mat, col, want_top=(0,1,0)):
        (x0,y0,z0),(x1,y1,z1)=c0,c1
        v=[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),
           (x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]
        for vs,w,m in [((v[0],v[1],v[2],v[3]),(0,-1,0),mat),((v[4],v[7],v[6],v[5]),(0,1,0),mat),
                       ((v[0],v[4],v[5],v[1]),(0,0,-1),mat),((v[2],v[6],v[7],v[3]),(0,0,1),mat),
                       ((v[1],v[5],v[6],v[2]),(1,0,0),mat),((v[3],v[7],v[4],v[0]),(-1,0,0),mat)]:
            self.face(list(vs), m, col, w)
    @staticmethod
    def _normal(cos):
        n=[0.0,0.0,0.0]
        for i in range(len(cos)):
            a,b=cos[i],cos[(i+1)%len(cos)]
            n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
        return n
    def bake(self, mesh_name, obj_name, mat_names):
        f2=[]; mi2=[]
        for ids,mi,w in zip(self.f,self.mi,self.want):
            cos=[self.v[i] for i in ids]
            n=self._normal(cos)
            # want authored Y-up; stored verts are Z-up after corner() swap
            w=(w[0],w[2],w[1])
            if n[0]*w[0]+n[1]*w[1]+n[2]*w[2] < 0:
                ids=tuple([ids[0]]+list(reversed(ids[1:])))
            f2.append(ids); mi2.append(mi)
        mesh=bpy.data.meshes.new(mesh_name)
        mesh.from_pydata(self.v, [], f2); mesh.update()
        col=mesh.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        li=0
        for p,mid in zip(mesh.polygons, mi2):
            p.material_index=mid; p.use_smooth=False
            for _ in p.loop_indices:
                col.data[li].color=HEX and self._col(p, li) or (1,1,1,1); li+=1
        obj=bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)
        for m in mat_names: obj.data.materials.append(get_mat(m))
        return obj
    def _col(self, poly, li):
        # corner colors stored per appended corner in order; loop order matches face order
        return (1,1,1,1)

# simpler: store color per loop directly
class MB2(MB):
    c = None
    def __init__(self):
        self.v=[]; self.f=[]; self.mi=[]; self.want=[]; self.loopcols=[]
    def tri(self, *args):
        if len(args)==4 and isinstance(args[0],(list,tuple)):
            (a,b,c),mat,col,want=args
        else: a,b,c,mat,col,want=args
        self.face([a,b,c], mat, col, want)
    def quad(self, *args):
        if len(args)==4 and isinstance(args[0],(list,tuple)):
            (a,b,c,d),mat,col,want=args
        else: a,b,c,d,mat,col,want=args
        self.face([a,b,c,d], mat, col, want)
    def cuboid(self, c0, c1, mat, col, want_top=(0,1,0)):
        (x0,y0,z0),(x1,y1,z1)=c0,c1
        v=[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),
           (x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]
        for vs,w,m in [((v[0],v[1],v[2],v[3]),(0,-1,0),mat),((v[4],v[7],v[6],v[5]),(0,1,0),mat),
                       ((v[0],v[4],v[5],v[1]),(0,0,-1),mat),((v[2],v[6],v[7],v[3]),(0,0,1),mat),
                       ((v[1],v[5],v[6],v[2]),(1,0,0),mat),((v[3],v[7],v[4],v[0]),(-1,0,0),mat)]:
            self.face(list(vs), m, col, w)
    def face(self, cos, mat, col, want):
        idx=[self.corner(p, col) for p in cos]
        self.f.append(tuple(idx)); self.mi.append(mat); self.want.append(tuple(want))
        self.loopcols.append([tuple(col)]*len(cos))
    def bake(self, mesh_name, obj_name, mat_names):
        f2=[]; mi2=[]; lc2=[]
        for ids,mi,w,lc in zip(self.f,self.mi,self.want,self.loopcols):
            cos=[self.v[i] for i in ids]
            n=self._normal(cos)
            # want authored Y-up; stored verts are Z-up after corner() swap
            w=(w[0],w[2],w[1])
            if n[0]*w[0]+n[1]*w[1]+n[2]*w[2] < 0:
                ids=tuple([ids[0]]+list(reversed(ids[1:])))
                lc=list(reversed(lc))
            f2.append(ids); mi2.append(mi); lc2.append(lc)
        mesh=bpy.data.meshes.new(mesh_name)
        mesh.from_pydata(self.v, [], f2); mesh.update()
        col=mesh.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        li=0
        for p,mid,lcs in zip(mesh.polygons, mi2, lc2):
            p.material_index=mid; p.use_smooth=False
            for c in lcs:
                col.data[li].color=c; li+=1
        obj=bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)
        for m in mat_names: obj.data.materials.append(get_mat(m))
        return obj

def C(name, jitter=0.0, seed=0):
    r,g,b,_ = hexrgb(HEX[name])
    if jitter:
        rr=random.Random(hash((name,seed)) & 0xffffffff)
        f=1+rr.uniform(-jitter, jitter)
        r,g,b=min(r*f,1),min(g*f,1),min(b*f,1)
    return (r,g,b,1.0)

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def select_only(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0] if objs else None

def ground_min_y(obj):
    # stored verts are Z-up (Blender native)
    return min(v.co.z for v in obj.data.vertices)

def lift_to_zero(obj):
    # only pull up: parts designed above ground (pine cones, lantern glass)
    # must keep their authored heights
    d = -ground_min_y(obj)
    if d > 1e-6:
        obj.data.transform(Matrix.Translation((0, 0, d)))

def bake_transforms(o):
    # bake location/rotation/scale into mesh data, reset object to identity.
    # join() + the runner's transform_apply must never see a non-identity
    # part, otherwise offsets get applied twice (measured: flower +0.150).
    select_only([o])
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def export_glb(objs, path, anim=False):
    select_only(objs)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
    # verts are Blender Z-up; exporter converts to glTF Y-up
        export_yup=True, export_materials='EXPORT', export_image_format='AUTO',
        export_texcoords=True, export_normals=True, export_vertex_color='NONE',
        export_animations=anim)

def rounded_rect(n=96, size=18.0, r=3.0):
    s=size/2; pts=[]
    for cx,cy,a0 in [(s-r,s-r,0),(s-r,-(s-r),-90),(-(s-r),-(s-r),180),(-(s-r),s-r,90)]:
        for i in range(n//4):
            a=math.radians(a0)+(i/(n//4))*math.pi/2
            pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    return pts

# ---------------- builders ----------------
GROUND_H = 0.814          # skirt top band height: v=1 at the top edge, 0 at y=0

def _uv_ground_top(mesh):
    """One planar map over the full 18x18 ground: zero tiling, u/v in [0,1]."""
    uv = mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:
        x, depth, _ = mesh.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = ((x + 9.0) / 18.0, (depth + 9.0) / 18.0)

def _uv_ground_sides(mesh):
    """Soil skirt: u wraps the perimeter once, v is the height band."""
    uv = mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:
        x, depth, h = mesh.vertices[loop.vertex_index].co
        u = 0.5 + math.atan2(depth, x) / (2 * math.pi)
        uv.data[loop.index].uv = (u, h / GROUND_H)

def build_ground():
    # Rounded-square grid 18x18, r=3 corners projected onto the arc (no
    # staircase cut). Flat center, subtle edge jitter +-0.06, skirt down to
    # y=0.0 tapering 0.93, flat bottom fan. Authored at final height (top ~0.8).
    random.seed(7)
    N = 24
    half = 9.0
    R = 3.0
    Q = half - R  # corner circle centers at (+-Q, +-Q)
    step = 18.0 / N

    def project(x, z):
        ax, az = abs(x), abs(z)
        if ax > Q and az > Q:
            dx, dz = ax - Q, az - Q
            d = math.hypot(dx, dz)
            if d > R:
                s = R / d
                ax, az = Q + dx * s, Q + dz * s
        return math.copysign(ax, x), math.copysign(az, z)

    def height(x, z):
        d = math.hypot(x, z)
        if d < 5:
            return 0.8
        edge = min(1.0, math.hypot(max(0, abs(x)-(half-1)), max(0, abs(z)-(half-1))) / 4.0)
        return 0.8 + random.uniform(-0.06, 0.06) * edge

    top = MB2()
    V = {}
    for j in range(N+1):
        for i in range(N+1):
            x = -half + i*step
            z = -half + j*step
            x, z = project(x, z)
            V[(i, j)] = (x, height(x, z), z)
    for j in range(N):
        for i in range(N):
            p00 = V[(i, j)]; p10 = V[(i+1, j)]; p11 = V[(i+1, j+1)]; p01 = V[(i, j+1)]
            col = C('M_Grass', 0.05, seed=i*31+j)
            top.quad(p00, p10, p11, p01, 0, col, (0, 1, 0))
    o_top = top.bake('Ground_Top', 'Ground_Top', ['M_Grass'])

    # perimeter ring (grid boundary), ordered around the outline
    ring = [(i, 0) for i in range(N+1)]
    ring += [(N, j) for j in range(1, N+1)]
    ring += [(i, N) for i in range(N-1, -1, -1)]
    ring += [(0, j) for j in range(N-1, 0, -1)]

    side = MB2()
    for k in range(len(ring)):
        a = ring[k]; b = ring[(k+1) % len(ring)]
        t0 = V[a]; t1 = V[b]
        b0 = (t0[0]*0.93, 0.0, t0[2]*0.93)
        b1 = (t1[0]*0.93, 0.0, t1[2]*0.93)
        mx, mz = (t0[0]+t1[0])/2, (t0[2]+t1[2])/2
        L = math.hypot(mx, mz) or 1
        side.quad(t0, t1, b1, b0, 0, C('M_Soil', 0.06, seed=k), (mx/L, 0, mz/L))
    # bottom fan
    cb = side.corner((0, 0.0, 0), C('M_Soil'))
    for k in range(len(ring)):
        pa = V[ring[k]]; pb = V[ring[(k+1) % len(ring)]]
        i0 = side.corner((pa[0]*0.93, 0.0, pa[2]*0.93), C('M_Soil'))
        i1 = side.corner((pb[0]*0.93, 0.0, pb[2]*0.93), C('M_Soil'))
        side.f.append((cb, i1, i0)); side.mi.append(0)
        side.want.append((0, -1, 0))
        side.loopcols.append([C('M_Soil')]*3)
    o_side = side.bake('Ground_Sides', 'Ground_Sides', ['M_Soil'])
    _uv_ground_top(o_top.data)
    _uv_ground_sides(o_side.data)
    return [o_top, o_side], 'environment/ground.blend', 'ground.glb'

def build_tent():
    W,D,H,E=1.5,1.5,2.2,0.12
    slope=lambda x: H-((H-E)/W)*abs(x)
    body=MB2(); OR='M_TentOrange'
    # roof panels with overhang
    body.quad([(-W-0.15,E-0.1,-D-0.15),(-W-0.15,E-0.1,D+0.15),(0,H+0.04,D+0.15),(0,H+0.04,-D-0.15)],0,C(OR,0.03,1),(-0.8,0.6,0))
    body.quad([(W+0.15,E-0.1,D+0.15),(W+0.15,E-0.1,-D-0.15),(0,H+0.04,-D-0.15),(0,H+0.04,D+0.15)],0,C(OR,0.03,2),(0.8,0.6,0))
    # front gable z=+D with doorway |x|<0.5,h<1.5
    y2=slope(0.5)
    body.tri([(-W,E,D),(-0.5,E,D),(-0.5,y2,D)],0,C(OR),(0,0,1))
    body.tri([(-W,E,D),(-0.5,y2,D),(0,H,D)],0,C(OR),(0,0,1))
    body.tri([(0.5,y2,D),(0.5,E,D),(W,E,D)],0,C(OR),(0,0,1))
    body.tri([(0,H,D),(0.5,y2,D),(W,E,D)],0,C(OR),(0,0,1))
    body.tri([(-0.5,1.5,D),(0.5,1.5,D),(0,H,D)],0,C(OR),(0,0,1))
    # back gable full z=-D
    body.tri([(-W,E,-D),(W,E,-D),(0,H,-D)],0,C(OR,0.02,3),(0,0,-1))
    # trim: ridge + bottom edges + eaves + corner battens
    body.cuboid((-0.05,H-0.02,-D-0.15),(0.05,H+0.08,D+0.15),1,C('M_TentTrim'),(0,1,0))
    body.cuboid((-W-0.15,0.0,D-0.06),(W+0.15,0.1,D+0.06),1,C('M_TentTrim'),(0,1,0))
    body.cuboid((-W-0.15,0.0,-D-0.06),(W+0.15,0.1,-D+0.06),1,C('M_TentTrim'),(0,1,0))
    for sx in (-W-0.15, W+0.15):
        body.cuboid((sx-0.04,E-0.1,-D-0.15),(sx+0.04,E+0.06,D+0.15),1,C('M_TentTrim'),(0,1,0))
    # guy-line pegs already separate; add ridge end caps
    for sz in (-D-0.15, D+0.15):
        body.cuboid((-0.06,H-0.06,sz-0.05),(0.06,H+0.08,sz+0.05),1,C('M_TentTrim'),(0,1,0))
    o_body=body.bake('Tent_Body','Tent_Body',['M_TentOrange','M_TentTrim'])
    # flap hinged open 20deg
    import math as _m
    ang=_m.radians(20); L=1.5
    flap=MB2()
    flap.quad([(-0.5,1.5,D),(0.5,1.5,D),(0.5,1.5-L*_m.cos(ang),D+L*_m.sin(ang)),(-0.5,1.5-L*_m.cos(ang),D+L*_m.sin(ang))],0,C(OR,0.02,4),(0,0,1))
    o_flap=flap.bake('Tent_Flap','Tent_Flap',['M_TentOrange'])
    # cream interior plane
    cr=MB2()
    cr.quad([(-0.55,0.0,D-0.3),(0.55,0.0,D-0.3),(0.55,1.55,D-0.3),(-0.55,1.55,D-0.3)],0,C('M_TentCream'),(0,0,1))
    o_cream=cr.bake('Tent_Inner','Tent_Inner',['M_TentCream'])
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=H+0.1, location=(0,D,(H+0.1)/2))
    p1=bpy.context.view_layer.objects.active
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=H+0.1, location=(0,-D,(H+0.1)/2))
    p2=bpy.context.view_layer.objects.active
    for p in (p1,p2):
        m=p.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for i in range(len(col.data)): col.data[i].color=C('M_Pole')
        for poly in m.polygons: poly.use_smooth=False
        p.data.materials.append(get_mat('M_Pole'))
    select_only([p1,p2]); bpy.ops.object.join()
    poles=bpy.context.view_layer.objects.active; poles.name='Tent_Poles'; poles.data.name='Tent_Poles'
    return [o_body,o_flap,o_cream,poles],'camping/tent.blend','tent.glb'

print('common loaded')

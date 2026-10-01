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
 'M_FlameOuter':'FF7A1A','M_FlameMid':'FFA928','M_FlameInner':'FFD84A','M_FlameBase':'D9560F',
 'M_LanternMetal':'3E3A2E','M_LanternGlass':'F6E6BF','M_LanternLight':'FFC95C',
}
EMISSIVE = {'M_FlameOuter','M_FlameMid','M_FlameInner','M_FlameBase','M_LanternLight'}
ROUGH = {'M_LanternMetal':0.6,'M_LanternGlass':0.4}
GLASSY = {'M_LanternGlass'}

def hexrgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1.0,)

def get_mat(name):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = hexrgb(HEX[name])
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
        self.v.append(tuple(co)); return len(self.v)-1
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
    return min(v.co.y for v in obj.data.vertices)

def lift_to_zero(obj):
    d = -ground_min_y(obj)
    if abs(d) > 1e-6:
        obj.data.transform(Matrix.Translation((0, d, 0)))

def export_glb(objs, path, anim=False):
    select_only(objs)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
        export_yup=True, export_materials='EXPORT', export_image_format='NONE',
        export_texcoords=False, export_normals=True, export_vertex_color='NAME',
        export_vertex_color_name='Color', export_all_vertex_colors=True,
        export_animations=anim)

def rounded_rect(n=96, size=18.0, r=3.0):
    s=size/2; pts=[]
    for cx,cy,a0 in [(s-r,s-r,0),(s-r,-(s-r),-90),(-(s-r),-(s-r),180),(-(s-r),s-r,90)]:
        for i in range(n//4):
            a=math.radians(a0)+(i/(n//4))*math.pi/2
            pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    return pts

# ---------------- builders ----------------
def build_ground():
    random.seed(7)
    pts=rounded_rect(); NV=len(pts)
    rings=[0.0,0.2,0.35,0.5,0.65,0.8,0.9,1.0]
    top=MB2(); GR='M_Grass'
    ringpts=[]
    for t in rings:
        rp=[]
        for (x,z) in pts:
            d=math.hypot(x,z)
            y=0.0 if d<5 else random.uniform(-0.15,0.15)*min(1,(d-5)/4)*t
            rp.append((x*t, y*t, z*t))
        ringpts.append(rp)
    for b in range(len(rings)-1):
        for i in range(NV):
            j=(i+1)%NV
            a,b2=ringpts[b][i],ringpts[b][j]; c,d=ringpts[b+1][j],ringpts[b+1][i]
            mx=(a[0]+b2[0]+c[0]+d[0])/4; mz=(a[2]+b2[2]+c[2]+d[2])/4
            dd=math.hypot(mx,mz)
            patch=math.sin(mx*1.3)*math.sin(mz*1.7+1.0)
            col=C('M_GrassPatch') if (dd<5.5 and patch>0.45) else C('M_Grass',0.05,seed=i+b*99)
            top.quad(a,b2,c,d,0,col,(0,1,0))
    o_top=top.bake('Ground_Top','Ground_Top',['M_Grass'])
    side=MB2()
    for i in range(NV):
        j=(i+1)%NV
        t0=ringpts[-1][i]; t1=ringpts[-1][j]
        b0=(t0[0]*0.93,-0.8,t0[2]*0.93); b1=(t1[0]*0.93,-0.8,t1[2]*0.93)
        mx,my,mz=(t0[0]+t1[0])/2,(t0[1]-0.4),(t0[2]+t1[2])/2
        w=(mx,0,mz); L=math.hypot(mx,mz) or 1; w=(w[0]/L,0,w[2]/L)
        side.quad(t0,t1,b1,b0,0,C('M_Soil',0.06,seed=i),w)
    bot=side  # bottom fan into same object
    bot.v.append((0,-0.8,0))
    cx=len(bot.v)-1
    for i in range(NV):
        j=(i+1)%NV
        p0=(ringpts[-1][i][0]*0.93,-0.8,ringpts[-1][i][2]*0.93)
        p1=(ringpts[-1][j][0]*0.93,-0.8,ringpts[-1][j][2]*0.93)
        i0=bot.corner(p0,C('M_Soil')); i1=bot.corner(p1,C('M_Soil'))
        bot.f.append((cx,i1,i0)); bot.mi.append(0); bot.want.append((0,-1,0))
        bot.loopcols.append([C('M_Soil')]*3)
    o_side=bot.bake('Ground_Sides','Ground_Sides',['M_Soil'])
    return [o_top,o_side], 'environment/ground.blend', 'ground.glb'

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
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=H+0.1, location=(0,(H+0.1)/2,D))
    p1=bpy.context.view_layer.objects.active
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=H+0.1, location=(0,(H+0.1)/2,-D))
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

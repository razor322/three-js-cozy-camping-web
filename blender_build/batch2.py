"""Batch 2: campfire, rocks, pine-tree, bush. Appended to common.py via exec."""
import bpy, math, random
from mathutils import Matrix, Vector

def build_campfire():
    objs=[]
    for i in range(4):
        a=i*math.pi/2+0.4
        cx,cz=math.cos(a)*0.32,math.sin(a)*0.32
        dx,dz=math.cos(a+math.pi/2),math.sin(a+math.pi/2)
        L=0.8; r=0.06; seg=10
        bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=L,
            location=(cx,cz,0.12), rotation=(math.pi/2,0,math.atan2(dx,-dz)))
        log=bpy.context.view_layer.objects.active
        log.name='Campfire_Log_%d'%(i+1); log.data.name=log.name
        m=log.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)):
            col.data[li].color=C('M_Bark',0.05,seed=i*10+li)
        m.materials.append(get_mat('M_Bark'))
        m.materials.append(get_mat('M_LogEnd'))
        for poly in m.polygons: poly.use_smooth=False
        objs.append(log)
    # end caps get M_LogEnd by material_index (slot 1), not vertex colour: the
    # exporter drops COLOR_0, so tinting per-corner would not survive the GLB.
    # Object rotation is still unapplied here, so the cylinder axis is local Z.
    for log in objs[:]:
        m=log.data
        for poly in m.polygons:
            if abs(poly.normal.z) > 0.9:
                poly.material_index = 1
    # flames: 3 nested cones-ish (6-sided, bent tip via offset top ring)
    specs=[('Campfire_Flame_Outer','M_FlameOuter',0.30,0.90),('Campfire_Flame_Mid','M_FlameMid',0.22,0.75),('Campfire_Flame_Inner','M_FlameInner',0.14,0.60)]
    for nm,mt,R,H in specs:
        fl=MB2()
        seg=10
        tiers=3
        prev=None
        for ti in range(tiers):
            y0=H*ti/tiers; y1=H*(ti+1)/tiers
            r0=R*(1-ti/tiers*0.65); r1=R*(1-(ti+1)/tiers*0.65)
            ox0=0.03*ti; ox1=0.03*(ti+1)
            for i in range(seg):
                a0=i/seg*2*math.pi; a1=(i+1)/seg*2*math.pi
                p0=(math.cos(a0)*r0+ox0,y0,math.sin(a0)*r0); p1=(math.cos(a1)*r0+ox0,y0,math.sin(a1)*r0)
                t0=(math.cos(a0)*r1+ox1,y1,math.sin(a0)*r1); t1=(math.cos(a1)*r1+ox1,y1,math.sin(a1)*r1)
                cx,cz=(p0[0]+p1[0])/2,(p0[2]+p1[2])/2
                L=math.hypot(cx,cz) or 1
                fl.quad(p0,p1,t1,t0,0,C(mt,0.04,seed=i+ti*20),(cx/L,0.2,cz/L))
        tip=(0.06+0.03*tiers,H+0.12,0.02)
        # tip cap ring
        rT=R*0.35; oxT=0.03*tiers
        for i in range(seg):
            a0=i/seg*2*math.pi; a1=(i+1)/seg*2*math.pi
            t0=(math.cos(a0)*rT+oxT,H,math.sin(a0)*rT); t1=(math.cos(a1)*rT+oxT,H,math.sin(a1)*rT)
            cx,cz=(t0[0]+t1[0])/2,(t0[2]+t1[2])/2
            L=math.hypot(cx,cz) or 1
            fl.tri(t0,t1,tip,0,C(mt),(cx/L,0.6,cz/L))
        # base fan
        cb=len(fl.v); fl.v.append((0,0,0))
        for i in range(seg):
            a0=i/seg*2*math.pi; a1=(i+1)/seg*2*math.pi
            i0=fl.corner((math.cos(a0)*R,0,math.sin(a0)*R),C(mt)); i1=fl.corner((math.cos(a1)*R,0,math.sin(a1)*R),C(mt))
            fl.f.append((cb,i1,i0)); fl.mi.append(0); fl.want.append((0,-1,0)); fl.loopcols.append([C(mt)]*3)
        o=fl.bake(nm,nm,[mt])
        objs.append(o)
    # base disc
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.35, depth=0.04, location=(0,0,0.02))
    base=bpy.context.view_layer.objects.active
    base.name='Campfire_Base'; base.data.name='Campfire_Base'
    m=base.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(col.data)): col.data[i].color=C('M_FlameBase')
    for poly in m.polygons: poly.use_smooth=False
    m.materials.append(get_mat('M_FlameBase'))
    objs.append(base)
    return objs,'camping/campfire.blend','campfire.glb'

def blob(obj_name, mesh_name, center, radii, mat, seed, detail=2):
    # center/radii authored Y-up (x, height, depth); store native Z-up
    cx, cy, cz = center
    rx, ry, rz = radii  # (x, height, depth)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=detail, radius=1, location=(cx, cz, cy))
    o=bpy.context.view_layer.objects.active
    o.name=obj_name; o.data.name=mesh_name
    for v in o.data.vertices:
        v.co.x*=rx; v.co.y*=rz; v.co.z*=ry
    m=o.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    rr=random.Random(seed)
    # per-face shade variation via loop colors
    for poly in m.polygons:
        poly.use_smooth=False
        f=1+rr.uniform(-0.06,0.06)
        base=hexrgb(HEX[mat]); c=(min(base[0]*f,1),min(base[1]*f,1),min(base[2]*f,1),1.0)
        for li in poly.loop_indices: col.data[li].color=c
    m.materials.append(get_mat(mat))
    o.data.transform(Matrix.Translation((-cx, -cz, -cy)))
    o.location=(0,0,0)
    # NOTE: caller positions; keep origin bottom-center by lifting later
    return o

def build_rocks():
    sma=blob('Rock_Small','Rock_Small',(0,0.2,0),(0.22,0.2,0.2),'M_Stone',11)
    med=blob('Rock_Medium','Rock_Medium',(0,0.35,0),(0.45,0.35,0.38),'M_StoneWarm',22)
    flat=blob('Rock_Flat','Rock_Flat',(0,0.18,0),(0.75,0.18,0.55),'M_Stone',33)
    for o,h in [(sma,0.0),(med,0.0),(flat,0.0)]:
        lift_to_zero(o)
        for p in o.data.polygons: p.use_smooth=False
    return [sma,med,flat],'environment/rocks.blend','rocks.glb'

def build_pine():
    # Proper stylized pine: tapered trunk + root flare, 4 tiers of rounded
    # blob clusters (wide bottom -> narrow top), soft bud tip. No sharp cones,
    # no object rotation except identity (join-safe: previous quaternion boughs
    # measured 8.72m tall vs 4.4m design). Total height ~4.2m, base at z=0.
    trunk_parts=[]
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.16, depth=1.4, location=(0,0,0.7))
    tr=bpy.context.view_layer.objects.active; tr.name='Pine_Trunk'; tr.data.name='Pine_Trunk'
    m=tr.data
    for v in m.vertices:  # taper toward the top ring
        if v.co.z > 1.2:
            v.co.x *= 0.7; v.co.y *= 0.7
    col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(col.data)): col.data[i].color=C('M_Trunk')
    for poly in m.polygons: poly.use_smooth=False
    m.materials.append(get_mat('M_Trunk')); trunk_parts.append(tr)
    for i in range(5):  # root flare blobs around the base, wide enough
        # to swallow the trunk bottom (trunk r=0.16) so no floating edge shows
        a=i/5*2*math.pi+0.3
        cx,cy,cz=math.cos(a)*0.19,0.10,math.sin(a)*0.19
        o=blob('Pine_Root_%d'%(i+1),'Pine_Root_%d'%(i+1),
               (0,0,0),(0.28,0.10,0.14),'M_Trunk',51+i,detail=1)
        o.location=(cx,cz,cy)
        lift_to_zero(o)
        trunk_parts.append(o)
    foliage=[]
    # (center-height, x-radius, y-radius, mat, seed, detail)
    tiers=[(1.35,1.15,0.75,'M_FoliageDark',101,2),
           (2.10,0.92,0.65,'M_FoliageLight',102,1),
           (2.80,0.70,0.55,'M_FoliageDark',103,1),
           (3.45,0.50,0.45,'M_FoliageLight',104,1)]
    for i,(hy,rx,ry,mt,sd,det) in enumerate(tiers):
        for k,(ox,oz,s) in enumerate([(0,0,1.0),(rx*0.62,ry*0.3,0.62),(-rx*0.6,-ry*0.35,0.58)]):
            cx,cy,cz=ox,hy-0.12+k*0.06,oz
            o=blob('Pine_Tier%d_Blob%d'%(i+1,k+1),'Pine_Tier%d_Blob%d'%(i+1,k+1),
                   (0,0,0),(rx*s,ry*s,rx*0.92*s),mt,sd+k,detail=det)
            o.location=(cx,cz,cy)
            foliage.append(o)
    bud=blob('Pine_Bud','Pine_Bud',(0,0,0),(0.30,0.32,0.28),'M_FoliageLight',77,detail=1)
    bud.location=(0,0,3.95)
    foliage.append(bud)
    # join reads matrix_world: refresh AFTER all locations are set, else every
    # part joins at identity (measured: foliage collapsed to +/-0.75 = one blob)
    bpy.context.view_layer.update()
    # join into 2 meshes: trunk group + foliage group (Dark/Light slots).
    # ponytail: ~40 parts -> 2 draw calls; geometry shared via clone(true)
    select_only(trunk_parts); bpy.ops.object.join()
    trunk=bpy.context.view_layer.objects.active; trunk.name='Pine_Trunk'; trunk.data.name='Pine_Trunk'
    select_only(foliage); bpy.ops.object.join()
    fol=bpy.context.view_layer.objects.active; fol.name='Pine_Foliage'; fol.data.name='Pine_Foliage'
    bpy.context.view_layer.update()  # join leaves matrix_world stale; refresh before measuring
    for o in (trunk, fol):  # hard guard: nothing below origin, trunk base ON origin
        ws=[o.matrix_world @ v.co for v in o.data.vertices]
        mn,mx=min(c[2] for c in ws),max(c[2] for c in ws)
        print('PINE CHECK', o.name, 'minz=%.3f maxz=%.3f' % (mn, mx))
        assert mn >= -0.01, 'pine part below origin: %s minz=%.3f' % (o.name, mn)
    wtr=[trunk.matrix_world @ v.co for v in trunk.data.vertices]
    assert min(c[2] for c in wtr) <= 0.05, 'trunk base off origin'
    wfol=[fol.matrix_world @ v.co for v in fol.data.vertices]
    fmn,fmx=min(c[2] for c in wfol),max(c[2] for c in wfol)
    assert 0.3 <= fmn <= 0.9, 'foliage bottom wrong: minz=%.3f' % fmn
    assert 3.8 <= fmx <= 4.8, 'pine height wrong: maxz=%.3f' % fmx
    return [trunk,fol],'vegetation/pine-tree.blend','pine-tree.glb'

def build_meadow():
    # Loose ground dressing, scattered code-side: grass tuft (joined blades),
    # two flowers (stem + bloom + petals, joined, 3 material slots each),
    # one pebble. Origin bottom-center, lifted to zero.
    parts=[]
    rng=random.Random(9)
    blades=[]
    for i in range(7):
        a=i/7*2*math.pi+rng.uniform(-0.2,0.2)
        tilt=rng.uniform(0.08,0.3)
        h=rng.uniform(0.22,0.38)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.035, depth=h,
            location=(math.cos(a)*0.05,math.sin(a)*0.05,h/2),
            rotation=(math.sin(a)*tilt,-math.cos(a)*tilt,a))
        b=bpy.context.view_layer.objects.active
        b.name='Blade_%d'%i; b.data.name=b.name
        b.scale=(0.45,1.0,1.0)
        m=b.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)): col.data[li].color=C('M_Grass',0.05,seed=i*3+li)
        for poly in m.polygons: poly.use_smooth=False
        m.materials.append(get_mat('M_Grass')); blades.append(b)
    # bake every part to identity BEFORE join so no offset can survive twice,
    # then a single lift_to_zero on the joined result fixes the base
    bpy.context.view_layer.update()
    for b in blades: bake_transforms(b)
    select_only(blades); bpy.ops.object.join()
    tuft=bpy.context.view_layer.objects.active; tuft.name='GrassTuft'; tuft.data.name='GrassTuft'
    lift_to_zero(tuft); parts.append(tuft)
    for fname, petal_mat, fseed in [('Flower','M_Petal',61),('FlowerPink','M_PetalPink',62)]:
        fparts=[]
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.015, depth=0.3, location=(0,0,0.15))
        stem=bpy.context.view_layer.objects.active
        stem.name=fname+'_Stem'; stem.data.name=stem.name
        m=stem.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)): col.data[li].color=C('M_Stem')
        for poly in m.polygons: poly.use_smooth=False
        m.materials.append(get_mat('M_Stem')); fparts.append(stem)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.045, depth=0.03, location=(0,0,0.31))
        dot=bpy.context.view_layer.objects.active
        dot.name=fname+'_Bloom'; dot.data.name=dot.name
        m=dot.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)): col.data[li].color=C('M_BloomDot')
        for poly in m.polygons: poly.use_smooth=False
        m.materials.append(get_mat('M_BloomDot')); fparts.append(dot)
        for k in range(6):
            a=k/6*2*math.pi
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.05,
                location=(math.cos(a)*0.075,math.sin(a)*0.075,0.31))
            p=bpy.context.view_layer.objects.active
            p.name='%s_Petal%d'%(fname,k+1); p.data.name=p.name
            p.scale=(1.0,1.0,0.45)
            m=p.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
            for li in range(len(col.data)): col.data[li].color=C(petal_mat,0.03,seed=fseed+k)
            for poly in m.polygons: poly.use_smooth=False
            m.materials.append(get_mat(petal_mat)); fparts.append(p)
        bpy.context.view_layer.update()
        for o in fparts: bake_transforms(o)
        select_only(fparts); bpy.ops.object.join()
        fl=bpy.context.view_layer.objects.active; fl.name=fname; fl.data.name=fname
        lift_to_zero(fl); parts.append(fl)
    peb=blob('Pebble','Pebble',(0,0.06,0),(0.09,0.055,0.07),'M_Stone',71,detail=1)
    lift_to_zero(peb); parts.append(peb)
    return parts,'vegetation/meadow.blend','meadow.glb'

def build_bush():
    parts=[]
    cl=[((0,0.4,0),(0.55,0.42,0.5),'M_FoliageDark',41),
        ((0.4,0.3,0.15),(0.4,0.3,0.38),'M_BushMid',42),
        ((-0.38,0.32,-0.1),(0.42,0.32,0.4),'M_BushMid',43),
        ((0.05,0.55,-0.15),(0.38,0.3,0.36),'M_FoliageDark',44)]
    for i,(c,r,mt,sd) in enumerate(cl):
        o=blob('Bush_Cluster_%d'%(i+1),'Bush_Cluster_%d'%(i+1),c,r,mt,sd)
        parts.append(o)
    for o in parts: lift_to_zero(o)
    # join into single object with 4 meshes? keep separate objects per plan
    return parts,'vegetation/bush.blend','bush.glb'

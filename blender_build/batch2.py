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
            location=(cx,0.12,cz), rotation=(math.pi/2,0,-math.atan2(dz,dx)+math.pi/2))
        log=bpy.context.view_layer.objects.active
        log.name='Campfire_Log_%d'%(i+1); log.data.name=log.name
        m=log.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)):
            v=m.vertices[m.loops[li].vertex_index].co
            col.data[li].color=C('M_Bark',0.05,seed=i*10+li)
        m.materials.append(get_mat('M_Bark'))
        # end caps get LogEnd: find cap loops by normal
        m2=m; 
        for poly in m.polygons: poly.use_smooth=False
        log.data.materials.append(get_mat('M_LogEnd'))
        for poly in m.polygons:
            if abs(poly.normal.z)>0.99 or (abs(poly.normal.x)<0.01 and abs(poly.normal.y)<0.01):
                pass
        objs.append(log)
    # recolor caps: vertices near ends
    for log in objs[:]:
        m=log.data
        col=m.color_attributes['Color']
        for li in range(len(col.data)):
            v=m.vertices[m.loops[li].vertex_index].co
            if abs(v.z)>L/2-0.02:
                col.data[li].color=C('M_LogEnd')
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
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.35, depth=0.04, location=(0,0.02,0))
    base=bpy.context.view_layer.objects.active
    base.name='Campfire_Base'; base.data.name='Campfire_Base'
    m=base.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(col.data)): col.data[i].color=C('M_FlameBase')
    for poly in m.polygons: poly.use_smooth=False
    m.materials.append(get_mat('M_FlameBase'))
    objs.append(base)
    return objs,'camping/campfire.blend','campfire.glb'

def blob(obj_name, mesh_name, center, radii, mat, seed, detail=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=detail, radius=1, location=center)
    o=bpy.context.view_layer.objects.active
    o.name=obj_name; o.data.name=mesh_name
    rx,ry,rz=radii
    for v in o.data.vertices:
        v.co.x*=rx; v.co.y*=ry; v.co.z*=rz
    m=o.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    rr=random.Random(seed)
    # per-face shade variation via loop colors
    for poly in m.polygons:
        poly.use_smooth=False
        f=1+rr.uniform(-0.06,0.06)
        base=hexrgb(HEX[mat]); c=(min(base[0]*f,1),min(base[1]*f,1),min(base[2]*f,1),1.0)
        for li in poly.loop_indices: col.data[li].color=c
    m.materials.append(get_mat(mat))
    o.data.transform(Matrix.Translation((-center[0],-center[1],-center[2])))
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
    parts=[]
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.125, depth=1.0, location=(0,0.5,0))
    tr=bpy.context.view_layer.objects.active; tr.name='Pine_Trunk'; tr.data.name='Pine_Trunk'
    m=tr.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(col.data)): col.data[i].color=C('M_Trunk')
    for poly in m.polygons: poly.use_smooth=False
    m.materials.append(get_mat('M_Trunk')); parts.append(tr)
    layers=[(2.4,1.5,1.05,'M_FoliageDark',0.4),(1.9,2.2,0.85,'M_FoliageLight',2.5),(1.4,2.85,0.7,'M_FoliageDark',1.2),(0.9,3.45,0.55,'M_FoliageLight',3.1)]
    for i,(W,Y,Hh,mt,rot) in enumerate(layers):
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=W/2, depth=Hh, location=(0.06*((i%2)*2-1)*0.3,Y,0.05*(1 if i%2 else -1)), rotation=(0,0,rot))
        cone=bpy.context.view_layer.objects.active
        cone.name='Pine_Foliage_%d'%(i+1); cone.data.name=cone.name
        m=cone.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for li in range(len(col.data)): col.data[li].color=C(mt,0.04,seed=i*7+li)
        for poly in m.polygons: poly.use_smooth=False
        m.materials.append(get_mat(mt)); parts.append(cone)
    return parts,'vegetation/pine-tree.blend','pine-tree.glb'

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

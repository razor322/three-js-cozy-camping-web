"""Batch 3: lantern + stump."""
import bpy, math

def build_lantern():
    parts=[]
    def cyl(name, verts, r, d, loc, mat, rot=None, shade_flat=True):
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot or (0,0,0))
        o=bpy.context.view_layer.objects.active; o.name=name; o.data.name=name
        m=o.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for i in range(len(col.data)): col.data[i].color=C(mat)
        for poly in m.polygons: poly.use_smooth=not shade_flat
        m.materials.append(get_mat(mat)); parts.append(o); return o
    base=cyl('Lantern_Body',16,0.09,0.05,(0,0,0.025),'M_LanternMetal')
    cap=cyl('Lantern_Body_Top',16,0.09,0.05,(0,0,0.375),'M_LanternMetal')
    parts.remove(cap); cap.name='Lantern_Body';  # merge naming: keep as body part
    glass=cyl('Lantern_Glass',16,0.07,0.26,(0,0,0.2),'M_LanternGlass',shade_flat=False)
    light=cyl('Lantern_Light',12,0.045,0.16,(0,0,0.2),'M_LanternLight',shade_flat=False)
    # posts L/R
    for sx,nm in [(-0.075,'Lantern_Post_L'),(0.075,'Lantern_Post_R')]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.012, depth=0.3, location=(sx,0,0.2))
        o=bpy.context.view_layer.objects.active; o.name=nm; o.data.name=nm
        m=o.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
        for i in range(len(col.data)): col.data[i].color=C('M_LanternMetal')
        for poly in m.polygons: poly.use_smooth=False
        m.materials.append(get_mat('M_LanternMetal')); parts.append(o)
    # handle: torus half
    bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.012, major_segments=16, minor_segments=8, location=(0,0,0.42), rotation=(math.pi/2,0,0))
    h=bpy.context.view_layer.objects.active; h.name='Lantern_Handle'; h.data.name='Lantern_Handle'
    m=h.data; col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(col.data)): col.data[i].color=C('M_LanternMetal')
    for poly in m.polygons: poly.use_smooth=False
    m.materials.append(get_mat('M_LanternMetal')); parts.append(h)
    for o in parts: pass
    # join metal parts into Lantern_Body (keep glass+light separate)
    metal=[o for o in parts if o.name not in ('Lantern_Glass','Lantern_Light','Lantern_Handle')]
    select_only(metal); bpy.ops.object.join()
    body=bpy.context.view_layer.objects.active; body.name='Lantern_Body'; body.data.name='Lantern_Body'
    return [body,glass,light,h],'camping/lantern.blend','lantern.glb'

def build_stump():
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.25, depth=0.45, location=(0,0,0.225))
    o=bpy.context.view_layer.objects.active; o.name='Stump'; o.data.name='Stump'
    m=o.data
    col=m.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for poly in m.polygons:
        poly.use_smooth=False
        is_top=poly.normal.z>0.9
        base=hexrgb(HEX['M_LogEnd'] if is_top else HEX['M_Bark'])
        for li in poly.loop_indices: col.data[li].color=(base[0],base[1],base[2],1.0)
    m.materials.append(get_mat('M_Bark')); m.materials.append(get_mat('M_LogEnd')); m.materials.append(get_mat('M_LogRing'))
    for poly in m.polygons:
        poly.material_index=1 if poly.normal.z>0.9 else 0
    # ring: thin torus on top face
    bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.015, major_segments=12, minor_segments=6, location=(0,0,0.451), rotation=(0,0,0))
    ring=bpy.context.view_layer.objects.active; ring.name='Stump_Ring'; ring.data.name='Stump_Ring'
    rm=ring.data; rcol=rm.color_attributes.new('Color','FLOAT_COLOR','CORNER')
    for i in range(len(rcol.data)): rcol.data[i].color=C('M_LogRing')
    for poly in rm.polygons: poly.use_smooth=False
    rm.materials.append(get_mat('M_LogRing'))
    select_only([o,ring]); bpy.ops.object.join()
    stump=bpy.context.view_layer.objects.active; stump.name='Stump'; stump.data.name='Stump'
    return [stump],'camping/stump.blend','stump.glb'

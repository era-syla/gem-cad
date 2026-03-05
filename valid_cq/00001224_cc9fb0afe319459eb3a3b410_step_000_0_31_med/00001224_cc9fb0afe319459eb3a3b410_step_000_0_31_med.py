import cadquery as cq

# Parameters
r_vert = 5.0
r_angled = 5.0
r_collar = 6.5
collar_h = 2.0
wall_thickness = 0.4
r_vert_in = r_vert - wall_thickness
r_angled_in = r_angled - wall_thickness

# Outer components
v_out = cq.Workplane("XY").workplane(offset=-25).circle(r_vert).extrude(50)
collar_out = cq.Workplane("XY").workplane(offset=-collar_h/2).circle(r_collar).extrude(collar_h)

# Path and profile for the angled tube
t_x = 1.5
t_z = 1.0
start_x = -2.0
start_z = start_x * (t_z / t_x)

path_wire = cq.Workplane("XZ").moveTo(start_x, start_z).spline(
    [(12, 10), (22, 0), (25, -25)], 
    tangents=[(t_x, t_z), (0.0, -1.0)]
).val()

profile_out = cq.Face.makeFromWires(
    cq.Wire.makeCircle(r_angled, cq.Vector(start_x, 0, start_z), cq.Vector(t_x, 0, t_z))
)
a_out = cq.Workplane("XY").add(cq.Solid.sweep(profile_out, path_wire))

outer = v_out.union(collar_out).union(a_out)

# Inner components for hollowing
v_in = cq.Workplane("XY").workplane(offset=-30).circle(r_vert_in).extrude(60)

profile_in = cq.Face.makeFromWires(
    cq.Wire.makeCircle(r_angled_in, cq.Vector(start_x, 0, start_z), cq.Vector(t_x, 0, t_z))
)
a_in = cq.Workplane("XY").add(cq.Solid.sweep(profile_in, path_wire))

inner = v_in.union(a_in)

# Combine outers and hollow out
result = outer.cut(inner)

# Trim off the uneven ends to leave clean open faces
box_cut_bottom = cq.Workplane("XY").workplane(offset=-30).box(100, 100, 10, centered=(True, True, False))
box_cut_top = cq.Workplane("XY").workplane(offset=20).box(100, 100, 10, centered=(True, True, False))

result = result.cut(box_cut_bottom).cut(box_cut_top)
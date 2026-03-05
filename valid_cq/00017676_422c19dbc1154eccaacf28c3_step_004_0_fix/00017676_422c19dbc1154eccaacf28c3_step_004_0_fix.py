import cadquery as cq

# Parameters
outer_r = 10
inner_r = 5
cyl_th = 8
flange_outer_r = 12
flange_th = 3
hub_r = 3
hub_th = 4
lever_length = 30
lever_width = 6
lever_th = 2
strut_r = 1.5
strut_y_offset = lever_width/2 - strut_r

# Main hollow cylinder
cyl = cq.Workplane("XY") \
    .circle(outer_r) \
    .circle(inner_r) \
    .extrude(cyl_th)

# Conical flange on top of cylinder
flange_profile = [
    (inner_r, 0),
    (flange_outer_r, 0),
    (flange_outer_r, flange_th),
    (inner_r, flange_th),
]
flange = (
    cq.Workplane("XZ")
    .polyline(flange_profile)
    .close()
    .revolve()
    .translate((0, 0, cyl_th))
)

# Small hub cylinder on top of flange
hub = (
    cq.Workplane("XY")
    .workplane(offset=cyl_th + flange_th)
    .circle(hub_r)
    .extrude(hub_th)
)

# Lever bar
lever_z = cyl_th + flange_th
lever = (
    cq.Workplane("XY")
    .workplane(offset=lever_z)
    .rect(lever_length, lever_width)
    .extrude(lever_th)
)

# Support struts connecting lever to flange
strut1 = (
    cq.Workplane("XY")
    .workplane(offset=lever_z)
    .transformed(offset=(lever_length/2, -strut_y_offset, 0))
    .circle(strut_r)
    .extrude(-flange_th)
)
strut2 = (
    cq.Workplane("XY")
    .workplane(offset=lever_z)
    .transformed(offset=(lever_length/2, strut_y_offset, 0))
    .circle(strut_r)
    .extrude(-flange_th)
)

# Combine everything
result = cyl.union(flange).union(hub).union(lever).union(strut1).union(strut2)
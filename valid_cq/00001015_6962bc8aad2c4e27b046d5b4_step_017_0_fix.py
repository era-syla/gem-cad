import cadquery as cq

# Parameters
base_width = 60
base_depth = 60
base_height = 10
corner_radius = 8

cylinder_od = 30
cylinder_id = 14
cylinder_height = 40

bolt_hole_dia = 7
bolt_hole_offset = 22

# Build the base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_height)
)

# Round the corners of the base
base = base.edges("|Z").fillet(corner_radius)

# Add the hollow cylinder on top of the base
cylinder_outer = (
    cq.Workplane("XY")
    .circle(cylinder_od / 2)
    .extrude(base_height + cylinder_height)
)

# Combine base and cylinder
result = base.union(cylinder_outer)

# Cut the inner bore through the cylinder
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(cylinder_id / 2)
    .cutBlind(-cylinder_height - base_height)
)

# Cut bolt holes in the base corners
result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints([
        (bolt_hole_offset, bolt_hole_offset),
        (-bolt_hole_offset, bolt_hole_offset),
        (-bolt_hole_offset, -bolt_hole_offset),
        (bolt_hole_offset, -bolt_hole_offset),
    ])
    .circle(bolt_hole_dia / 2)
    .cutBlind(base_height)
)
import cadquery as cq

# Parameters
outer = 120
thickness = 3
inner = outer - 2 * thickness
height = 60
flange = 12
h_holes = 7
v_holes = 6
hole_dia = 5.0

# Spacings
h_spacing = inner / (h_holes - 1)
z_spacing = height / (v_holes + 1)

# Base square tube
result = cq.Workplane("XY") \
    .rect(outer, outer) \
    .rect(inner, inner) \
    .extrude(height)

# Top flange
top_flange = (
    cq.Workplane("XY")
    .box(inner, flange, thickness)
    .translate((0, inner/2 + flange/2, height + thickness/2))
)

# Bottom flange
bottom_flange = (
    cq.Workplane("XY")
    .box(inner, flange, thickness)
    .translate((0, -inner/2 - flange/2, -thickness/2))
)

result = result.union(top_flange).union(bottom_flange)

# Holes in top flange
result = result.cut(
    cq.Workplane("XY")
    .transformed(offset=(0, inner/2 + flange/2, height))
    .rarray(h_spacing, 0, h_holes, 1)
    .circle(hole_dia/2)
    .extrude(thickness + 1, both=True)
)

# Holes in bottom flange
result = result.cut(
    cq.Workplane("XY")
    .transformed(offset=(0, -inner/2 - flange/2, 0))
    .rarray(h_spacing, 0, h_holes, 1)
    .circle(hole_dia/2)
    .extrude(thickness + 1, both=True)
)

# Holes in inner vertical walls
for xpos in (inner/2, -inner/2):
    depth = thickness + 1 if xpos > 0 else -(thickness + 1)
    result = result.cut(
        cq.Workplane("YZ")
        .transformed(offset=(xpos, 0, 0))
        .rarray(0, z_spacing, 1, v_holes)
        .circle(hole_dia/2)
        .extrude(depth)
    )
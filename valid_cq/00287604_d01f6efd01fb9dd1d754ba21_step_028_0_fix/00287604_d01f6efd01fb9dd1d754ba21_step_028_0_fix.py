import cadquery as cq

# Parameters
outer_radius = 25.0
wall_thickness = 2.0
height = 10.0
base_thickness = 2.0
center_sep = 2 * outer_radius - 2 * wall_thickness

# Create the outer solid by fusing two cylinders
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .union(
        cq.Workplane("XY")
        .transformed(offset=(center_sep, 0, 0))
        .circle(outer_radius)
        .extrude(height)
    )
)

# Create inner cavities (to subtract) for both bowls
inner = (
    cq.Workplane("XY")
    .circle(outer_radius - wall_thickness)
    .extrude(height - base_thickness)
)
inner2 = (
    cq.Workplane("XY")
    .transformed(offset=(center_sep, 0, 0))
    .circle(outer_radius - wall_thickness)
    .extrude(height - base_thickness)
)

# Subtract cavities from the outer solid
result = outer.cut(inner).cut(inner2)
import cadquery as cq

# Parameters
outer_diameter = 20
inner_diameter = 16
center_radius = 80

# Build the path: a quarter‐circle arc in the XY plane
path = (
    cq.Workplane("XY")
    .moveTo(center_radius, 0)
    .threePointArc((0, center_radius), (-center_radius, 0))
    .wire()
    .val()
)

# Sweep the outer profile
outer = (
    cq.Workplane("YZ", origin=(center_radius, 0, 0))
    .circle(outer_diameter / 2)
    .sweep(path, isFrenet=True)
)

# Sweep the inner profile (to cut away)
inner = (
    cq.Workplane("YZ", origin=(center_radius, 0, 0))
    .circle(inner_diameter / 2)
    .sweep(path, isFrenet=True)
)

# Subtract inner from outer to get the hollow tube
result = outer.cut(inner)
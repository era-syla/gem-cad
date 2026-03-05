import cadquery as cq

# Parameters
outer_d = 40
inner_d = 30
height = 10
hole_d = 5

# Radii
R_outer = outer_d / 2
R_inner = inner_d / 2
R_mid = (R_outer + R_inner) / 2

# Create ring by extruding two concentric circles
ring = (
    cq.Workplane("XY")
    .circle(R_outer)
    .circle(R_inner)
    .extrude(height)
)

# Create a cylindrical cutter for the side hole
# Workplane on YZ plane at the mid-radius and mid-height
hole_cyl = (
    cq.Workplane("YZ", origin=(R_mid, 0, height / 2))
    .circle(hole_d / 2)
    .extrude(2 * outer_d, both=True)
)

# Subtract the hole from the ring
result = ring.cut(hole_cyl)
import cadquery as cq

# Parameters
rod_length = 260
rod_radius = 3
body_length = 100
body_radius = 10
nut_flats = 10
nut_thickness = 5
# Circumcircle diameter so that flats-to-flats is nut_flats
nut_circ_diam = 2 * nut_flats / (3 ** 0.5)

# Build the rod
rod = (
    cq.Workplane("XY")
    .circle(rod_radius)
    .extrude(rod_length)
    .translate((0, 0, -rod_length / 2))
)

# Build the central cylinder body
body = (
    cq.Workplane("XY")
    .circle(body_radius)
    .extrude(body_length)
    .translate((0, 0, -body_length / 2))
)

# Build the two hex nuts
nut1 = (
    cq.Workplane("XY")
    .polygon(6, nut_circ_diam)
    .extrude(nut_thickness)
    .translate((0, 0, -body_length / 2 - nut_thickness))
)
nut2 = (
    cq.Workplane("XY")
    .polygon(6, nut_circ_diam)
    .extrude(nut_thickness)
    .translate((0, 0, body_length / 2))
)

# Combine everything
result = rod.union(body).union(nut1).union(nut2)
import cadquery as cq

# Parameters
thickness = 10.0
base_length = 30.0
bend_radius = 20.0
vertical_length = 15.0
disc_radius = 15.0
hole_diameter = 6.0

# Main bracket body: sketch in XZ plane and extrude in Y
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_length, 0)
    .threePointArc((base_length + bend_radius, bend_radius), (base_length, 2 * bend_radius))
    .lineTo(0, 2 * bend_radius + vertical_length)
    .close()
    .extrude(thickness)
)

# Add circular head (disc) at the top of the bracket
head_center_z = 2 * bend_radius + vertical_length
disc = (
    cq.Workplane("ZX")
    .center(base_length, head_center_z)
    .circle(disc_radius)
    .extrude(thickness)
)
result = result.union(disc)

# Drill hole through the disc (and any overlapping bracket material)
result = (
    result
    .faces(">Y")
    .workplane()
    .center(base_length, head_center_z)
    .hole(hole_diameter)
)
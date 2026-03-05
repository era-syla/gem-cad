import cadquery as cq

# Main rectangular body
body = (
    cq.Workplane("XY")
    .box(60, 40, 70)
)

# Position body upward to make room for base flange
body = (
    cq.Workplane("XY")
    .center(0, 0)
    .box(60, 40, 70, centered=(True, True, False))
    .translate((0, 0, 15))
)

# Create the base flange (wider flat plate)
flange = (
    cq.Workplane("XY")
    .box(90, 55, 8, centered=(True, True, False))
    .translate((0, 0, 7))
)

# Create cylindrical pedestal/foot below flange
pedestal = (
    cq.Workplane("XY")
    .cylinder(12, 18)
    .translate((0, 0, 6))
)

# Combine body and flange
result = body.union(flange).union(pedestal)

# Add mounting hole in flange
hole_offset_x = 32
hole_offset_y = 0

result = (
    result
    .cut(
        cq.Workplane("XY")
        .center(-hole_offset_x + 5, hole_offset_y)
        .circle(4)
        .extrude(8)
        .translate((0, 0, 7))
    )
)

# Add slight chamfer to top edges of main body
result = (
    result
    .edges("|Z")
    .chamfer(1.5)
)
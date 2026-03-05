import cadquery as cq

# Main disk (front large disk)
main_disk = (
    cq.Workplane("YZ")
    .circle(22)
    .extrude(8)
)

# Back disk (slightly smaller, behind main disk)
back_disk = (
    cq.Workplane("YZ")
    .workplane(offset=-8)
    .circle(20)
    .extrude(6)
)

# Combine main and back disk
body = main_disk.union(back_disk)

# Add groove/rim details on the front disk edge - create a torus-like groove
# We'll add a rim ring on the front face
front_rim = (
    cq.Workplane("YZ")
    .circle(22)
    .circle(19)
    .extrude(2)
)

body = body.union(front_rim)

# Back plate (flat circular plate)
back_plate = (
    cq.Workplane("YZ")
    .workplane(offset=-14)
    .circle(24)
    .extrude(4)
)

body = body.union(back_plate)

# Add a groove ring between main disk and back disk
groove_ring = (
    cq.Workplane("YZ")
    .workplane(offset=-7)
    .circle(21)
    .circle(18)
    .extrude(3)
)

body = body.union(groove_ring)

# Add the mounting post/pin that sticks out to the left/back
pin = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-18, 5)
    .circle(3)
    .extrude(20)
)

body = body.union(pin)

# Add a small rectangular bracket connecting pin to back plate
bracket = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-10, 5)
    .rect(16, 6)
    .extrude(12)
)

body = body.union(bracket)

# Apply fillets to smooth edges - select edges carefully
# Try to fillet the back plate edges
try:
    result = body.edges("|Y").fillet(1.0)
except:
    result = body

# Clean up the result
try:
    result = result.edges(">>X[-1]").fillet(1.5)
except:
    pass

result = body
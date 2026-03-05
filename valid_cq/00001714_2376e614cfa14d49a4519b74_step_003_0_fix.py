import cadquery as cq

# Main body block
body = (
    cq.Workplane("XY")
    .box(40, 35, 45)
)

# Chamfer the top front edge
body = (
    body
    .edges("|Z and >Y")
    .edges(">Z")
    .chamfer(4)
)

# Add mounting plate on the front face
plate = (
    cq.Workplane("XY")
    .box(44, 4, 48)
    .translate((0, 19.5, 0))
)

# Combine body and plate
result = body.union(plate)

# Add two cylindrical rods extending from the back
rod1 = (
    cq.Workplane("YZ")
    .center(0, 8)
    .circle(4)
    .extrude(60)
    .translate((-30, -17.5, 8))
)

rod2 = (
    cq.Workplane("YZ")
    .center(0, -8)
    .circle(4)
    .extrude(60)
    .translate((-30, -17.5, -8))
)

result = result.union(rod1).union(rod2)

# Add small screw holes on front plate
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(16, 18), (-16, 18), (16, -18), (-16, -18)])
    .hole(3.5, 4)
)

# Add a small nub/clip on top
clip = (
    cq.Workplane("XY")
    .box(20, 10, 6)
    .translate((0, 12, 25.5))
)

result = result.union(clip)

# Add rod support brackets (horizontal slats between rods)
bracket = (
    cq.Workplane("XY")
    .box(12, 15, 3)
    .translate((-10, -17.5, 0))
)

result = result.union(bracket)

# Final cleanup - ensure valid solid
result = result
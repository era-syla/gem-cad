import cadquery as cq

# Main body
main_body = (cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(12, 60)
    .extrude(20))

# Add angled support
angled_support = (cq.Workplane("XZ")
    .moveTo(0, 30)
    .lineTo(10, 45).lineTo(10, 75).lineTo(0, 75)
    .close().extrude(20))

# Cylindrical holes
hole1 = (cq.Workplane("XY")
    .moveTo(0, 20)
    .circle(5)
    .extrude(20))
hole2 = (cq.Workplane("XY")
    .moveTo(0, 50)
    .circle(5)
    .extrude(20))

# Assembly
result = (main_body
    .union(angled_support)
    .cut(hole1)
    .cut(hole2))
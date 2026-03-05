import cadquery as cq

# Main block dimensions
width = 40
depth = 40
height = 38

# Create the main body
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
)

# Round the vertical edges
result = result.edges("|Z").fillet(6)

# Round the top edges
result = result.edges(">Z").fillet(3)

# Round the bottom edges
result = result.edges("<Z").fillet(3)

# Add countersunk hole on top
result = (
    result
    .faces(">Z")
    .workplane()
    .cskHole(diameter=14, cskDiameter=26, cskAngle=82, depth=20)
)

# Cut a cylindrical notch on the left side (the curved cutout visible on left face)
result = (
    result
    .faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .center(0, -4)
    .circle(12)
    .cutBlind(-15)
)

# Add a small tab/protrusion on the top-right area (visible in image)
tab = (
    cq.Workplane("XY")
    .box(8, 6, 4)
    .translate((width/2 + 4, -4, height/2 - 2))
)

result = result.union(tab)

# Clean up the tab edges
result = result.edges(">X").fillet(1)
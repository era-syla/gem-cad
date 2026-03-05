import cadquery as cq

# Define main dimensions
length = 100
width = 20
height = 20
handle_curve = 10

# Create basic block
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, 0, handle_curve))
    .box(length * 0.8, width * 0.8, handle_curve, combine=False)
)

# Blend the top face into the main block and add curvature
result = (
    result.faces(">Y")
    .workplane(centerOption='CenterOfBoundBox')
    .transformed(offset=(0, 0, handle_curve))
    .line(length * 0.8, 0)
    .threePointArc((length * 0.4, handle_curve), (0, 0))
    .close()
    .cutBlind(-width * 0.1)
)

# Add a round to the edges
result = result.edges("|Z").fillet(5)
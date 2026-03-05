import cadquery as cq

# Main box dimensions
width = 80
depth = 80
height = 70

# Create the main box
box = cq.Workplane("XY").box(width, depth, height)

# Add fillets to vertical edges and top edges
box = box.edges("|Z").fillet(5)
box = box.edges(">Z").fillet(5)

# Cut a circular hole on the front face (right side face)
# Circular hole - positioned on the right face
box = (box
    .faces(">Y")
    .workplane()
    .center(-15, 5)
    .circle(5)
    .cutBlind(-10)
)

# Add a smaller inner circle (ring detail) around the hole
box = (box
    .faces(">Y")
    .workplane()
    .center(-15, 5)
    .circle(3)
    .cutBlind(-2)
)

# Cut a rectangular slot/port on the front face
box = (box
    .faces(">Y")
    .workplane()
    .center(10, -15)
    .rect(14, 6)
    .cutBlind(-5)
)

result = box
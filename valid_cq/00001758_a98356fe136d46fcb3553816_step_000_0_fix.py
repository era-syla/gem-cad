import cadquery as cq

# Main block dimensions
width = 60
depth = 50
height = 50

# Slot dimensions (U-shaped cutout from top)
slot_width = 20
slot_depth = 30
slot_height = 35

# Hole dimensions
hole_diameter = 8

# Create the main block
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    # Cut the U-shaped slot from the top, centered in width, open at front
    .faces(">Z")
    .workplane()
    .center(0, depth/4)
    .rect(slot_width, slot_depth)
    .cutBlind(-slot_height)
)

# Add the through hole on the front face (left side, lower area)
result = (
    result
    .faces("<Y")
    .workplane()
    .center(-width/4, -height/4)
    .hole(hole_diameter)
)
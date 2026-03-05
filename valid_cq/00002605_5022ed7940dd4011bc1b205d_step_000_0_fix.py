import cadquery as cq

# Main body dimensions
length = 60
width = 18
height = 20

# Create main rectangular body
body = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Add chamfer/fillet to edges
body = body.edges("|Z").fillet(2.5)
body = body.edges(">Z or <Z").fillet(1.5)

# Cut rectangular slots on the right face (two slots side by side)
slot_w = 10
slot_h = 12
slot_depth = 14
slot_spacing = 3
slot_offset_x = 8  # offset from right end

# Two rectangular slots on +X face
body = (
    body
    .faces(">X")
    .workplane()
    .rect(slot_w, slot_h)
    .cutBlind(-slot_depth)
)

# Actually let's create two slots
# First, rebuild with proper slot positions
body2 = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z").fillet(2.0)
)

# Cut two rectangular openings from the right face (+X direction)
# Slot 1 (top-ish position)
slot_width_each = 7
slot_height_each = 10
slot_depth_cut = 15
gap = 2

body2 = (
    body2
    .faces(">X")
    .workplane()
    .center(0, 3)
    .rect(slot_width_each, slot_height_each)
    .cutBlind(-slot_depth_cut)
)

body2 = (
    body2
    .faces(">X")
    .workplane()
    .center(0, -5)
    .rect(slot_width_each, slot_height_each)
    .cutBlind(-slot_depth_cut)
)

# Two small circular holes on the left face (-X direction), vertically stacked
hole_radius = 2
hole_spacing = 6

body2 = (
    body2
    .faces("<X")
    .workplane()
    .center(0, 3)
    .circle(hole_radius)
    .cutBlind(-6)
)

body2 = (
    body2
    .faces("<X")
    .workplane()
    .center(0, -3)
    .circle(hole_radius)
    .cutBlind(-6)
)

# Add a recessed notch/step on the bottom-front area (the angled cutout visible in image)
# Cut a wedge/step from bottom-front
step = (
    cq.Workplane("XZ")
    .workplane(offset=-width/2)
    .moveTo(-length/2 + 10, -height/2)
    .lineTo(-length/2 + 20, -height/2)
    .lineTo(-length/2 + 10, -height/2 + 8)
    .close()
    .extrude(width)
)

body2 = body2.cut(step)

# Fillet remaining sharp edges lightly
result = body2.edges(">Z").fillet(1.0)
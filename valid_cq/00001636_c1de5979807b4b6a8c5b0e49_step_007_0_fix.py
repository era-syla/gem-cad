import cadquery as cq

# Main block dimensions
L = 50  # length (X)
W = 28  # width (Y)
H = 12  # height (Z)

# Create the main rectangular block
result = (
    cq.Workplane("XY")
    .box(L, W, H)
)

# Round the two ends (along Y axis) - front and back rounded corners
result = (
    result
    .edges("|Z")
    .fillet(6)
)

# Add chamfer on the bottom front edge
result = (
    result
    .faces("<Z")
    .workplane()
    .center(0, 0)
)

# Re-approach: build from scratch with proper features
result = cq.Workplane("XY").box(L, W, H)

# Fillet vertical edges for rounded rectangle shape
result = result.edges("|Z").fillet(5)

# Add a slot/groove on the top face running along the length
# Groove on top surface
groove_depth = 1.5
groove_width = 3

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(L, groove_width)
    .cutBlind(-groove_depth)
)

# Add center hole through the part
hole_dia = 7
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(hole_dia)
)

# Add a slot/notch on the side (left side, front area) - the small step visible
# This is a rectangular notch on the left side
notch_w = 4
notch_h = 5
notch_d = 3

result = (
    result
    .faces("<X")
    .workplane()
    .center(0, H/2 - notch_h/2)
    .rect(notch_d * 2, notch_h)
    .cutBlind(-notch_d)
)

# Add chamfer on the bottom front/back long edges
result = (
    result
    .faces("<Z")
    .edges()
    .chamfer(1.5)
)
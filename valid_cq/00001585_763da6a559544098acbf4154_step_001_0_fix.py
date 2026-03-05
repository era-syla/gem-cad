import cadquery as cq

# Build a wire connector/plug shape
# Main body - rounded rectangular box
main_body = (
    cq.Workplane("XY")
    .box(40, 30, 25)
)

# Round the main body
main_body = main_body.edges("|Z").fillet(6)
main_body = main_body.edges(">Z").fillet(4)
main_body = main_body.edges("<Z").fillet(3)

# Create the front face with connector holes
# Add a slightly larger rounded front extension
front_ext = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 0))
    .box(38, 28, 10)
    .edges("|Z").fillet(5)
)

# Combine body parts
body = main_body.union(front_ext)

# Create the top ridged/fan section
# Multiple overlapping cylinders tilted to create fan effect
ridge1 = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 8, 0))
    .circle(22)
    .extrude(15)
)

ridge2 = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 12, 0))
    .circle(20)
    .extrude(12)
)

# Side wings/tabs
wing_left = (
    cq.Workplane("XY")
    .transformed(offset=(-25, 0, -2))
    .box(12, 20, 18)
    .edges("|Z").fillet(4)
    .edges(">Z").fillet(3)
)

wing_right = (
    cq.Workplane("XY")
    .transformed(offset=(25, 0, -2))
    .box(12, 20, 18)
    .edges("|Z").fillet(4)
    .edges(">Z").fillet(3)
)

# Combine all parts
combined = body.union(wing_left).union(wing_right)

# Add rounded top dome
top_dome = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 10))
    .ellipse(22, 16)
    .extrude(10)
)
top_dome2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 15))
    .ellipse(18, 13)
    .extrude(8)
)

combined = combined.union(top_dome).union(top_dome2)

# Cut connector holes in the front face
# Two rounded rectangular holes side by side
hole1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 4, 20))
    .rect(10, 14)
    .extrude(25)
)

hole2 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, -6, 20))
    .rect(10, 14)
    .extrude(25)
)

# Cut small circular notches at bottom of holes
notch1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 4, 20))
    .circle(5)
    .extrude(25)
)

notch2 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, -6, 20))
    .circle(5)
    .extrude(25)
)

# Apply cuts
result = combined.cut(hole1).cut(hole2).cut(notch1).cut(notch2)

# Final smoothing
try:
    result = result.edges(">Y and |Z").fillet(2)
except:
    pass
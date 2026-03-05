import cadquery as cq

# -- Parametric Dimensions --
length = 150.0
thickness = 8.0

# Profile Coordinates (Counter-Clockwise)
# Origin (0,0) is roughly at the vertical center of the left (narrow) face
p_top_left = (0, 25)
p_bot_left = (0, -15)

# Step feature coordinates on the bottom edge
# This creates the transition from the narrow section to the wide section
p_step_inner = (50, -20)  # The "inner" corner of the notch
p_step_outer = (60, -35)  # The "outer" corner of the notch

p_bot_right = (140, -45)
p_top_right = (140, 45)

# Hole Pattern Configuration
# Right Group: 3 holes in a vertical line near the wide end
holes_right = [
    (125, 30),
    (125, 0),
    (125, -30)
]

# Middle Group: 2 holes (top and bottom)
holes_mid = [
    (75, 25),
    (75, -20)
]

# Left Group: 1 hole near the narrow tip (top side)
holes_left = [
    (25, 10)
]

all_holes = holes_right + holes_mid + holes_left

# Hole Dimensions
hole_dia = 6.0
csk_dia = 11.0
csk_angle = 90.0

# -- Model Construction --

# 1. Generate Base Shape
# Define the perimeter points
pts = [
    p_top_left,
    p_bot_left,
    p_step_inner,
    p_step_outer,
    p_bot_right,
    p_top_right
]

# Create the solid extrusion
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 2. Add Fillets
# Fillet the vertical corners (Z-parallel edges)
result = result.edges("|Z").fillet(5.0)

# 3. Create Countersunk Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(all_holes)
    .cskHole(hole_dia, csk_dia, csk_angle)
)

# 4. Finish Edges
# Add a small fillet to the top and bottom contour edges for realism
result = result.edges("#Z").fillet(0.5)
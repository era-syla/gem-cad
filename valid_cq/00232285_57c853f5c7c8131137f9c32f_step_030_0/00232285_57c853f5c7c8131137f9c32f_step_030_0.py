import cadquery as cq

# Dimensions
plate_width = 60.0
plate_height = 100.0
thickness = 3.0
corner_radius = 5.0
hole_diameter = 5.0
hole_chamfer = 0.5

# Hole Positioning (Symmetrical about center)
# Horizontal spacing for pairs (distance from center)
x_offset = 20.0
# Vertical positions
y_top_row = 35.0
y_mid_row = 0.0
y_bot_hole = -35.0
# Vertical drop for the center hole in the "V" patterns
v_drop = 10.0

# Define hole coordinates
points = [
    # Top "V" cluster
    (-x_offset, y_top_row),
    (x_offset, y_top_row),
    (0, y_top_row - v_drop),
    
    # Middle "V" cluster
    (-x_offset, y_mid_row),
    (x_offset, y_mid_row),
    (0, y_mid_row - v_drop),
    
    # Bottom single hole
    (0, y_bot_hole)
]

# Create the plate geometry
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)

# Apply chamfer to the top edges of the holes
# We select edges on the top face, then filter by radius. 
# The holes (r=2.5) are smaller than the corner fillets (r=5.0), so we select the 0th radius.
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(hole_chamfer)
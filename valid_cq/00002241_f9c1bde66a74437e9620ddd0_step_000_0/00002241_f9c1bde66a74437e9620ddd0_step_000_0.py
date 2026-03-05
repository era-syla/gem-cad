import cadquery as cq

# --- Parametric Dimensions ---
part_length = 80.0      # Total length from tip to tip
part_width = 30.0       # Total width of the part
part_height = 25.0      # Total height of the extrusion
tip_length = 15.0       # Length of the pointed triangular section
pocket_length = 40.0    # Length of the rectangular recess
pocket_width = 14.0     # Width of the rectangular recess
pocket_depth = 8.0      # Depth of the rectangular recess

# --- Geometry Construction ---

# Calculate helper coordinates for the base profile
# The shape is centered at the origin (0,0)
x_straight_end = (part_length / 2.0) - tip_length
y_half_width = part_width / 2.0

# Define the vertices of the elongated hexagon profile
# Order: Right Tip -> Top Right -> Top Left -> Left Tip -> Bottom Left -> Bottom Right
profile_points = [
    (part_length / 2.0, 0.0),
    (x_straight_end, y_half_width),
    (-x_straight_end, y_half_width),
    (-part_length / 2.0, 0.0),
    (-x_straight_end, -y_half_width),
    (x_straight_end, -y_half_width)
]

# 1. Create the base prism
result = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .extrude(part_height)
)

# 2. Create the rectangular pocket on the top face
result = (
    result.faces(">Z")            # Select the top face
    .workplane()                  # Create a workplane on it
    .rect(pocket_length, pocket_width)  # Draw the rectangle for the pocket
    .cutBlind(-pocket_depth)      # Cut into the part by the specified depth
)
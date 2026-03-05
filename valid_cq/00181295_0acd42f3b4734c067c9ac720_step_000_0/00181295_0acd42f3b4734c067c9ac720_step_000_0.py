import cadquery as cq

# --- Parameters ---
# Overall dimensions estimated from image proportions
width = 240.0
height = 360.0
thickness = 15.0
frame_width = 45.0  # Width of the flange material
fillet_radius = 15.0
hole_diameter = 8.0

# Hole counts based on visual inspection (including corners)
holes_x_count = 8   # Top/Bottom edges
holes_y_count = 13  # Side edges

# --- Logic for Hole Coordinates ---
# Holes are placed on the centerline of the frame
centerline_width = width - frame_width
centerline_height = height - frame_width

pts = []

# Generate X coordinates for top and bottom rows
if holes_x_count > 1:
    step_x = centerline_width / (holes_x_count - 1)
    for i in range(holes_x_count):
        x = -centerline_width / 2 + i * step_x
        pts.append((x, centerline_height / 2))   # Top row
        pts.append((x, -centerline_height / 2))  # Bottom row

# Generate Y coordinates for side columns (skipping first/last to avoid double counting corners)
if holes_y_count > 2:
    step_y = centerline_height / (holes_y_count - 1)
    for i in range(1, holes_y_count - 1):
        y = -centerline_height / 2 + i * step_y
        pts.append((-centerline_width / 2, y))   # Left column
        pts.append((centerline_width / 2, y))    # Right column

# --- 3D Modeling ---

# 1. Create the base frame profile and extrude
# Using two rectangles to define the frame shape in 2D
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2 * frame_width, height - 2 * frame_width)
    .extrude(thickness)
)

# 2. Apply fillets to all vertical edges (outer and inner corners)
# Selecting edges parallel to Z axis ("|Z")
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(hole_diameter)
)
import cadquery as cq

# --- Parameters ---
# Overall dimensions
width = 160.0
depth = 100.0
thickness = 4.0

# Slot (cutout) dimensions
slot_width = 50.0
slot_depth = 40.0

# Wing corner chamfer
chamfer_size = 30.0

# Hole dimensions
large_hole_diam = 12.0
large_hole_spacing = 24.0

small_hole_diam = 4.0
mount_hole_margin_x = 20.0     # Distance from side edges
mount_hole_margin_back = 15.0  # Distance from back edge
mount_hole_margin_slot = 15.0  # Distance from slot inner edge

# --- Geometry Construction ---

# Coordinates calculation based on center (0,0)
x_max = width / 2.0
x_min = -width / 2.0
y_max = depth / 2.0
y_min = -depth / 2.0

# Slot boundaries
slot_x_right = slot_width / 2.0
slot_x_left = -slot_width / 2.0
slot_y_inner = y_min + slot_depth

# Define profile points (Counter-Clockwise starting from Top-Left)
points = [
    (x_min, y_max),                      # Back Left Corner
    (x_min, y_min + chamfer_size),       # Left Side Chamfer Start
    (x_min + chamfer_size, y_min),       # Left Wing Tip
    (slot_x_left, y_min),                # Left Front Inner
    (slot_x_left, slot_y_inner),         # Slot Bottom Left
    (slot_x_right, slot_y_inner),        # Slot Bottom Right
    (slot_x_right, y_min),               # Right Front Inner
    (x_max - chamfer_size, y_min),       # Right Wing Tip
    (x_max, y_min + chamfer_size),       # Right Side Chamfer Start
    (x_max, y_max),                      # Back Right Corner
]

# Create the base solid plate
plate = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# --- Add Holes ---

# 1. Central Large Holes
# Positioned in the middle of the main body (area above the slot)
center_y = (y_max + slot_y_inner) / 2.0
large_hole_pts = [
    (-large_hole_spacing / 2.0, center_y),
    (large_hole_spacing / 2.0, center_y)
]

plate_with_large_holes = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(large_hole_pts)
    .hole(large_hole_diam)
)

# 2. Mounting Holes (4x small holes)
# Calculate positions
back_y = y_max - mount_hole_margin_back
front_y = slot_y_inner + mount_hole_margin_slot
side_x = x_max - mount_hole_margin_x

mount_hole_pts = [
    (-side_x, back_y),   # Back Left
    (side_x, back_y),    # Back Right
    (-side_x, front_y),  # Front Left
    (side_x, front_y),   # Front Right
]

# Final result with all holes
result = (
    plate_with_large_holes
    .faces(">Z")
    .workplane()
    .pushPoints(mount_hole_pts)
    .hole(small_hole_diam)
)
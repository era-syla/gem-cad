import cadquery as cq

# --- Parametric Dimensions ---
part_width = 70.0       # X-axis dimension
part_length = 90.0      # Y-axis dimension
total_height = 15.0     # Z-axis dimension
wall_thickness = 2.0    # Thickness of walls and base
large_hole_dia = 50.0   # Central hole diameter
small_hole_dia = 3.2    # Mounting hole diameter

# --- Modeling ---

# 1. Base Plate
# Create the solid base block centered on the XY plane
result = cq.Workplane("XY").box(part_width, part_length, wall_thickness)

# 2. U-Shaped Walls
# Calculate half-dimensions for coordinate definitions
w2 = part_width / 2.0
l2 = part_length / 2.0
t = wall_thickness

# Define points for the U-shaped wall profile (top-down view)
# Orientation: Back wall at +Y, Open side at -Y
wall_profile_pts = [
    (w2, -l2),              # Outer Right Front
    (w2, l2),               # Outer Right Back
    (-w2, l2),              # Outer Left Back
    (-w2, -l2),             # Outer Left Front
    (-w2 + t, -l2),         # Inner Left Front
    (-w2 + t, l2 - t),      # Inner Left Back
    (w2 - t, l2 - t),       # Inner Right Back
    (w2 - t, -l2)           # Inner Right Front
]

# Select the top face of the base and extrude the walls
result = (result
    .faces(">Z").workplane()
    .polyline(wall_profile_pts)
    .close()
    .extrude(total_height - wall_thickness)
)

# 3. Features (Cuts)

# Large Central Hole
result = (result
    .faces(">Z").workplane()
    .center(0, 0)
    .circle(large_hole_dia / 2.0)
    .cutThruAll()
)

# Small Mounting Holes
# Located near the front-left corner (negative X, negative Y region)
mnt_offset_x = -w2 + 8.0  # 8mm from left edge
mnt_offset_y = -l2 + 8.0  # 8mm from front edge
mnt_spacing = 8.0         # Distance between the two small holes

result = (result
    .faces(">Z").workplane()
    .pushPoints([
        (mnt_offset_x, mnt_offset_y),
        (mnt_offset_x, mnt_offset_y + mnt_spacing)
    ])
    .circle(small_hole_dia / 2.0)
    .cutThruAll()
)
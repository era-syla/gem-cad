import cadquery as cq

# --- Parameters ---
height = 500.0           # Total height of the L-bracket
width_left = 60.0        # Width of the left flange
width_right = 100.0      # Width of the right flange
thickness = 4.0          # Material thickness

# Slot dimensions
slot_length = 25.0       # Length of the oblong slot
slot_width = 8.0         # Width of the oblong slot

# Pattern parameters
pitch_vert = 40.0        # Vertical pitch between slots
pitch_horz = 40.0        # Horizontal pitch (for double columns)
margin_z = 35.0          # Margin from top/bottom edges

# Feature counts
left_slots_count = 3     # Number of slots per group on left flange
right_rows_count = 4     # Number of rows per group on right flange

# --- Geometry Construction ---

# 1. Create Base L-Profile
# Defined in the XY plane with the corner at (0,0)
# Left leg extends along +Y, Right leg extends along +X
pts = [
    (0, width_left),
    (0, 0),
    (width_right, 0),
    (width_right, thickness),
    (thickness, thickness),
    (thickness, width_left)
]

# Extrude the profile
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# 2. Define Point Generation Logic
def generate_z_positions(count, pitch, margin, total_height):
    """Generates Z coordinates for symmetric top and bottom groups."""
    z_coords = []
    # Bottom group
    for i in range(count):
        z_coords.append(margin + i * pitch)
    # Top group
    for i in range(count):
        z_coords.append(total_height - margin - i * pitch)
    return z_coords

# 3. Create Cuts on Left Flange
# Face corresponds to X=0 plane.
# Local coordinates on this face: X -> Global Y (Width), Y -> Global Z (Height)
left_y_center = width_left / 2.0
left_pts = []
for z in generate_z_positions(left_slots_count, pitch_vert, margin_z, height):
    left_pts.append((left_y_center, z))

result = (
    result
    .faces("<X")
    .workplane()
    .pushPoints(left_pts)
    .slot2D(slot_length, slot_width, angle=90) # angle=90 orients slot vertically
    .cutThruAll()
)

# 4. Create Cuts on Right Flange
# Face corresponds to Y=0 plane.
# Local coordinates on this face: X -> Global X (Width), Y -> Global Z (Height)
right_x_center = width_right / 2.0
col_offsets = [-pitch_horz / 2.0, pitch_horz / 2.0]
right_pts = []

# Generate points for 2 columns for both top and bottom groups
z_positions_right = generate_z_positions(right_rows_count, pitch_vert, margin_z, height)
for z in z_positions_right:
    for offset in col_offsets:
        right_pts.append((right_x_center + offset, z))

result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(right_pts)
    .slot2D(slot_length, slot_width, angle=90)
    .cutThruAll()
)
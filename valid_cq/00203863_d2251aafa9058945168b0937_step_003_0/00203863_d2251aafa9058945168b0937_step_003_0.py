import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_width = 100.0   # Dimension along X axis
plate_length = 200.0  # Dimension along Y axis
plate_thickness = 4.0

# Circular hole parameters
hole_diameter = 24.0
hole_col_spacing = 50.0  # Distance between columns (X direction)
hole_row_spacing = 55.0  # Distance between rows (Y direction)

# Slot parameters
slot_width = 8.0
slot_overall_length = 24.0
# slot2D requires center-to-center length
slot_cc_length = slot_overall_length - slot_width 
slot_pos_y = 80.0 # Distance from center of plate to center of slot

# --- Modeling ---

# 1. Create the base rectangular plate
# The box is centered at the origin (0,0,0)
result = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# 2. Define coordinates for the 6 circular holes
# A 2x3 grid centered on the plate
hole_points = []
for row in [-1, 0, 1]:  # Three rows
    for col in [-1, 1]: # Two columns
        x = col * (hole_col_spacing / 2)
        y = row * hole_row_spacing
        hole_points.append((x, y))

# 3. Cut the circular holes
result = (result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# 4. Cut the oblong slot
# Positioned near the top edge, oriented horizontally (parallel to width)
result = (result
    .faces(">Z")
    .workplane()
    .center(0, slot_pos_y)
    .slot2D(slot_cc_length, slot_width, 0)
    .cutThruAll()
)
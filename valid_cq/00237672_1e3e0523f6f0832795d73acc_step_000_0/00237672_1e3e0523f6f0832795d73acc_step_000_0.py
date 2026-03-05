import cadquery as cq

# --- Parameter Definitions ---
# Plate dimensions
plate_width = 400.0
plate_depth = 400.0
plate_thickness = 8.0

# Feature dimensions
center_hole_diameter = 12.0
mounting_hole_diameter = 5.0
slot_length = 80.0
slot_width = 18.0

# Feature positions
slot_center_x = 110.0
slot_center_y = 30.0

# Mounting hole configuration
edge_margin = 20.0
hole_spacing = 30.0  # Spacing between the pairs of holes

# --- Geometry Construction ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_depth, plate_thickness)

# 2. Cut the central hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# 3. Cut the rectangular slot
# Move workplane center to slot position, create rectangle, and cut through
result = (
    result.faces(">Z")
    .workplane()
    .center(slot_center_x, slot_center_y)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# 4. Create mounting holes
# Define coordinates for the small mounting holes
hole_points = []

# X and Y offsets for the corner groups
x_off = plate_width / 2.0 - edge_margin
y_off = plate_depth / 2.0 - edge_margin

# Corner 1 (Front-Left): Pair aligned along Y edge
hole_points.append((-x_off, -y_off))
hole_points.append((-x_off, -y_off + hole_spacing))

# Corner 2 (Back-Left): Pair aligned along Y edge
hole_points.append((-x_off, y_off))
hole_points.append((-x_off, y_off - hole_spacing))

# Corner 3 (Front-Right): Pair aligned along Y edge
hole_points.append((x_off, -y_off))
hole_points.append((x_off, -y_off + hole_spacing))

# Corner 4 (Back-Right): Pair aligned along Y edge
hole_points.append((x_off, y_off))
hole_points.append((x_off, y_off - hole_spacing))

# Additional holes around the slot feature
# Approximating positions based on the image
hole_points.append((slot_center_x - slot_length/2 - 15, slot_center_y)) # Left of slot
hole_points.append((slot_center_x + slot_length/2 + 15, slot_center_y)) # Right of slot
hole_points.append((slot_center_x + 10, slot_center_y - slot_width/2 - 15)) # Below slot offset

# Apply the mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(mounting_hole_diameter)
)

# Return the final object
# result is now the completed CadQuery object
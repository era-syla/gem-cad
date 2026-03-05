import cadquery as cq

# --- Parametric Dimensions ---
# Base plate dimensions
plate_width = 140.0
plate_depth = 100.0
plate_thickness = 8.0
fillet_radius = 5.0

# Slot (pocket) dimensions
slot_len = 40.0
slot_width = 5.0
slot_depth = 2.0
slot_spacing_x = 60.0  # Horizontal distance between slot centers
slot_spacing_y = 30.0  # Vertical distance between slot centers

# Thin groove dimensions
groove_width = 1.0
groove_depth = 0.5

# Layout positioning
header_margin = 10.0   # Distance of header groove from top edge
pattern_offset_y = -8.0 # Shift the central slot pattern downwards to make room for header

# --- Modeling ---

# 1. Create the base plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Cut the four main slots (arranged in a 2x2 grid)
# Define the centers for the 4 slots relative to the pattern center
slot_centers = [
    (-slot_spacing_x / 2, pattern_offset_y - slot_spacing_y / 2),
    ( slot_spacing_x / 2, pattern_offset_y - slot_spacing_y / 2),
    (-slot_spacing_x / 2, pattern_offset_y + slot_spacing_y / 2),
    ( slot_spacing_x / 2, pattern_offset_y + slot_spacing_y / 2),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_centers)
    .slot2D(slot_len, slot_width, angle=0)
    .cutBlind(-slot_depth)
)

# 3. Cut the Header Groove (Long thin slot near the top edge)
header_y_pos = (plate_depth / 2) - header_margin
header_len = plate_width - 25.0

result = (
    result.faces(">Z")
    .workplane()
    .center(0, header_y_pos)
    .slot2D(header_len, groove_width, angle=0)
    .cutBlind(-groove_depth)
)

# 4. Cut the Central Crosshair Grooves (Divider lines)
# Vertical divider
v_groove_len = (slot_spacing_y * 2) + 15.0  # Span the height of the slot pattern plus margin
result = (
    result.faces(">Z")
    .workplane()
    .center(0, pattern_offset_y)
    .slot2D(v_groove_len, groove_width, angle=90)
    .cutBlind(-groove_depth)
)

# Horizontal divider
h_groove_len = plate_width - 25.0
result = (
    result.faces(">Z")
    .workplane()
    .center(0, pattern_offset_y)
    .slot2D(h_groove_len, groove_width, angle=0)
    .cutBlind(-groove_depth)
)
import cadquery as cq

# --- Parameters ---
# Main Plate
plate_width = 120.0
plate_height = 70.0
plate_thickness = 10.0

# Slots
slot_length = 30.0
slot_width = 8.0
# Slot positions (relative to center)
slot_x_offset = 35.0  # Horizontal distance from center
slot_y_top = 15.0     # Vertical position of top slot
slot_y_bot = -20.0    # Vertical position of bottom slots

# Mounting Bracket (Protrusion)
bracket_width = 40.0
bracket_height = 20.0
bracket_depth = 25.0  # Stick-out distance from plate face
bracket_x_pos = -slot_x_offset # Aligned with left slots

# Bracket Cutout (U-shape)
cutout_width = 20.0

# Gusset (Triangle Support)
gusset_height = 25.0

# Mounting Holes
hole_diameter = 6.0

# --- Modeling ---

# 1. Base Plate
# Create the main rectangular plate centered at origin
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Slots
# Define positions for the three slots
slot_locations = [
    (-slot_x_offset, slot_y_top),  # Top Left
    (-slot_x_offset, slot_y_bot),  # Bottom Left
    (slot_x_offset, slot_y_bot)    # Bottom Right
]

# Cut slots through the plate
result = result.faces(">Z").workplane().pushPoints(slot_locations) \
    .slot2D(slot_length, slot_width, angle=0).cutThruAll()

# 3. Bracket Body
# Calculate position for the bracket (Top-Left area)
# Y centered at: Top Edge - Half Bracket Height
bracket_y_center = (plate_height / 2) - (bracket_height / 2)
# Z starts at: Front Face of plate
plate_front_z = plate_thickness / 2

# Create the solid block for the bracket
bracket_geo = cq.Workplane("XY") \
    .workplane(offset=plate_front_z) \
    .center(bracket_x_pos, bracket_y_center) \
    .box(bracket_width, bracket_height, bracket_depth, centered=(True, True, False))

# 4. Gusset
# Create the triangular support underneath the bracket
# Defined on YZ plane (Side View)
# Coordinates: (Y, Z)
y_bracket_bottom = bracket_y_center - (bracket_height / 2)
z_bracket_tip = plate_front_z + bracket_depth
y_gusset_bottom = y_bracket_bottom - gusset_height

pts = [
    (y_bracket_bottom, plate_front_z),   # Top-Inner (at plate face)
    (y_bracket_bottom, z_bracket_tip),   # Top-Outer (at bracket tip)
    (y_gusset_bottom, plate_front_z)     # Bottom-Inner
]

# Extrude triangle and move to correct X position
gusset_geo = cq.Workplane("YZ").polyline(pts).close() \
    .extrude(bracket_width / 2, both=True) \
    .translate((bracket_x_pos, 0, 0))

# Union the bracket and gusset to the main body
result = result.union(bracket_geo).union(gusset_geo)

# 5. Clevis Cutout
# Cut the U-shape slot out of the bracket center
cutout_geo = cq.Workplane("XY") \
    .workplane(offset=plate_front_z) \
    .center(bracket_x_pos, bracket_y_center) \
    .box(cutout_width, bracket_height, bracket_depth, centered=(True, True, False))

result = result.cut(cutout_geo)

# 6. Pin Holes
# Create holes through the bracket ears (aligned along X axis)
# Z height: Middle of the bracket depth
hole_z = plate_front_z + (bracket_depth / 2)
# Y height: Middle of the bracket height
hole_y = bracket_y_center

# Cut hole using a cylinder generated on YZ plane
result = result.cut(
    cq.Workplane("YZ").center(hole_y, hole_z)
    .circle(hole_diameter / 2)
    .extrude(100, both=True) # Cut through everything in X path (safe as it is above plate Z)
)
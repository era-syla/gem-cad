import cadquery as cq

# Parametric dimensions for the model
plate_thickness = 4.0
outer_width = 200.0      # Overall width including corners
inner_hole_width = 110.0 # Central square hole width

# Handle / Recess configuration
recess_depth = 12.0      # How much the handle is inset from the corner outer edge
recess_length = 110.0    # Length of the recessed section along the side

# Handle Slot configuration
slot_length = 80.0
slot_width = 15.0
handle_bar_thickness = 8.0 # Thickness of the outer loop of the handle

# Mounting holes
hole_diameter = 3.5

# Calculate derived dimensions
# Center offset for the handle slots
# Outer edge of handle is at (outer_width/2 - recess_depth)
# Slot center is shifted inwards by handle_bar_thickness and half the slot width
handle_outer_limit = (outer_width / 2) - recess_depth
slot_center_offset = handle_outer_limit - handle_bar_thickness - (slot_width / 2)

# Coordinates for mounting holes (2 per corner, symmetric)
# Positioned in the corner blocks
h_offset_long = (outer_width / 2) - 10.0
h_offset_short = (outer_width / 2) - 25.0
hole_points = [
    (h_offset_long, h_offset_short), (h_offset_short, h_offset_long),    # Top Right
    (-h_offset_long, h_offset_short), (-h_offset_short, h_offset_long),  # Top Left
    (-h_offset_long, -h_offset_short), (-h_offset_short, -h_offset_long),# Bottom Left
    (h_offset_long, -h_offset_short), (h_offset_short, -h_offset_long)   # Bottom Right
]

# 1. Base Plate
result = cq.Workplane("XY").box(outer_width, outer_width, plate_thickness)

# 2. Cut Center Hole
result = result.faces(">Z").workplane().rect(inner_hole_width, inner_hole_width).cutThruAll()

# 3. Cut Side Recesses
# We cut rectangular notches from the four sides to define the handle areas vs corners
# Top and Bottom recesses
result = result.faces(">Z").workplane() \
    .pushPoints([(0, outer_width/2), (0, -outer_width/2)]) \
    .rect(recess_length, recess_depth * 2).cutThruAll()

# Left and Right recesses
result = result.faces(">Z").workplane() \
    .pushPoints([(outer_width/2, 0), (-outer_width/2, 0)]) \
    .rect(recess_depth * 2, recess_length).cutThruAll()

# 4. Cut Handle Slots
# Top and Bottom slots
result = result.faces(">Z").workplane() \
    .pushPoints([(0, slot_center_offset), (0, -slot_center_offset)]) \
    .rect(slot_length, slot_width).cutThruAll()

# Left and Right slots
result = result.faces(">Z").workplane() \
    .pushPoints([(slot_center_offset, 0), (-slot_center_offset, 0)]) \
    .rect(slot_width, slot_length).cutThruAll()

# 5. Drill Corner Holes
result = result.faces(">Z").workplane() \
    .pushPoints(hole_points) \
    .circle(hole_diameter / 2) \
    .cutThruAll()

# Helper for visualization in some environments (optional)
# show_object(result)
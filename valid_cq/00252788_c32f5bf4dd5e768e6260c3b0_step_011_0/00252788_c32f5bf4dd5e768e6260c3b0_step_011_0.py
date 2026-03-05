import cadquery as cq

# --- Geometric Parameters ---
plate_width = 300.0
plate_height = 220.0
plate_thickness = 10.0

# Top slot parameters
slot_length = 50.0
slot_height = 15.0
slot_top_offset = 35.0  # Distance from top edge to center of slot

# Bottom notch parameters
notch_width = 15.0
notch_depth = 8.0
notch_edge_offset = 50.0  # Distance from side edge to center of notch

# --- Modeling ---

# 1. Create base plate
# Using XZ plane so the model stands upright matching the image orientation
result = cq.Workplane("XZ").box(plate_width, plate_height, plate_thickness)

# 2. Cut the top slot
# We select the front face (>Y) and establish a 2D workplane
# Local coordinates: x is horizontal, y is vertical
slot_y_location = (plate_height / 2.0) - slot_top_offset

result = (
    result.faces(">Y")
    .workplane()
    .center(0, slot_y_location)
    .slot2D(slot_length, slot_height)
    .cutThruAll()
)

# 3. Cut the bottom notches
# We calculate the X positions for the notches based on the offset from the edges
notch_x_location = (plate_width / 2.0) - notch_edge_offset
notch_y_location = -(plate_height / 2.0)

# We use pushPoints to perform operations at multiple locations
# We cut a rectangle of double depth centered on the edge to ensure a clean cutout
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints([
        (notch_x_location, notch_y_location),
        (-notch_x_location, notch_y_location)
    ])
    .rect(notch_width, notch_depth * 2.0)
    .cutThruAll()
)
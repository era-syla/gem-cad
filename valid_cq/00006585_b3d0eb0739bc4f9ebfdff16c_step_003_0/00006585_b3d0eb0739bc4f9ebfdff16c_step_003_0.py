import cadquery as cq

# --- Parameter Definitions ---
# Main Plate Dimensions
plate_width = 100.0
plate_height = 50.0
plate_thickness = 8.0

# Rear Block Dimensions
block_width = 40.0
block_height = 25.0
block_depth = 20.0

# Slot Dimensions
slot_width = 8.0
slot_height = 25.0
slot_offset_x = 35.0  # Distance from center to slot center

# Pin Dimensions
pin_diameter = 5.0
pin_height = 10.0
pin_spacing = 20.0

# --- Modeling ---

# 1. Create the Base Plate
# Oriented on the XZ plane to stand vertically, extruded along Y (thickness)
result = cq.Workplane("XZ").box(plate_width, plate_height, plate_thickness)

# 2. Add the Rear Block
# Select the back face (>Y), create a workplane, and align the block 
# so it is centered horizontally and flush with the top edge.
# The center shift moves the drawing plane origin from the face center 
# to the desired center of the block.
result = (
    result.faces(">Y")
    .workplane()
    .center(0, (plate_height / 2.0) - (block_height / 2.0))
    .rect(block_width, block_height)
    .extrude(block_depth)
)

# 3. Cut the Slots
# Select the front face (<Y) and cut rectangular slots through the plate.
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints([(-slot_offset_x, 0), (slot_offset_x, 0)])
    .rect(slot_width, slot_height)
    .cutThruAll()
)

# 4. Add the Pins
# Create pins on the top surface. We use global coordinates to position
# the workplane on top of the block accurately.
# Top Z level = half of plate height.
# Center Y of block = half of plate thickness + half of block depth.
top_z_level = plate_height / 2.0
block_center_y = (plate_thickness / 2.0) + (block_depth / 2.0)

pins = (
    cq.Workplane("XY")
    .workplane(offset=top_z_level)
    .center(0, block_center_y)
    .pushPoints([(-pin_spacing / 2.0, 0), (pin_spacing / 2.0, 0)])
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)

# Combine the main body with the pins
result = result.union(pins)
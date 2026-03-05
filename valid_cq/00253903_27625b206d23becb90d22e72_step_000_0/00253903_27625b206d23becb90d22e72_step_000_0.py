import cadquery as cq

# Dimensions
length = 100.0
width = 30.0
thickness = 6.0
fillet_radius = 4.0

# Feature Parameters
slot_length = 30.0
slot_width = 10.0
notch_width = 10.0
notch_depth = 12.0
hole_diameter = 6.0
cbore_diameter = 12.0
cbore_depth = 3.0

# Positioning
# Calculated relative to center (0,0) of the part
slot_x = (length / 2) - (slot_length / 2) - 8.0
notch_x = -5.0
hole_x = -(length / 2) + 12.0

# 1. Create Base Plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply Corner Fillets
result = result.edges("|Z").fillet(fillet_radius)

# 3. Cut Slot (Right Side)
result = (
    result.faces(">Z")
    .workplane()
    .center(slot_x, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-thickness)
)

# 4. Cut Side Notch (Middle)
# Modeled as a slot entering from the side edge to create a U-shape
# Centered on the edge (Y = width/2)
result = (
    result.faces(">Z")
    .workplane()
    .center(notch_x, width / 2)
    .slot2D(notch_depth * 2, notch_width, 90)
    .cutBlind(-thickness)
)

# 5. Create Counterbored Hole (Left Side)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_x, 0)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)
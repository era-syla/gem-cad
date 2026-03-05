import cadquery as cq

# Parametric dimensions based on the visual proportions
plate_height = 80.0
plate_width = 50.0
thickness = 4.0
corner_radius = 8.0
slot_width = 6.0
slot_length = 40.0

# Create the base plate centered at the origin
result = cq.Workplane("XY").box(plate_width, plate_height, thickness)

# Apply fillets to the four vertical corners
result = result.edges("|Z").fillet(corner_radius)

# Calculate the position for the slot cut
# The slot starts at the bottom edge (y = -plate_height/2) and extends upwards
# The center of the cutting rectangle must be offset from the origin
slot_center_y = -plate_height / 2 + slot_length / 2

# Create the slot by cutting a rectangle through the plate
result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_center_y)
    .rect(slot_width, slot_length)
    .cutThruAll()
)
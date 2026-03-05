import cadquery as cq

# Parametric dimensions for the model
front_plate_width = 100.0
front_plate_height = 40.0
front_plate_thickness = 3.0

# Dimensions for the rear block (inset from the front plate)
inset_distance = 5.0
rear_block_width = front_plate_width - (2 * inset_distance)
rear_block_height = front_plate_height - (2 * inset_distance)
rear_block_thickness = 15.0

# Create the CAD model
# 1. Start with the thin front plate centered on the XY plane
result = cq.Workplane("XY").box(front_plate_width, front_plate_height, front_plate_thickness)

# 2. Select the top face (back of the plate), draw the rear block profile, and extrude
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(rear_block_width, rear_block_height)
    .extrude(rear_block_thickness)
)
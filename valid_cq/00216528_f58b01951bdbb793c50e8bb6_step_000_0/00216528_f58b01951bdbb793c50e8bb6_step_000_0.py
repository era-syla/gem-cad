import cadquery as cq

# Model Parameters
plate_length = 100.0
plate_height = 50.0
plate_thickness = 5.0
hole_width = 15.0
hole_height = 12.0
hole_vertical_offset = -10.0  # Distance from center (negative is downwards)

# Create the geometric model
# We start on the XZ plane to orient the plate vertically
result = (
    cq.Workplane("XZ")
    .box(plate_length, plate_height, plate_thickness)
    .faces(">Y")              # Select the front face (positive Y direction)
    .workplane()
    .center(0, hole_vertical_offset) # Move operation center relative to face center
    .rect(hole_width, hole_height)   # Sketch the rectangular hole
    .cutThruAll()             # Cut the sketch through the solid
)
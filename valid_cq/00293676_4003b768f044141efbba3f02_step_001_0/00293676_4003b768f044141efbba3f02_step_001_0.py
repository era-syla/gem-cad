import cadquery as cq

# Parametric dimensions
plate_length = 100.0
plate_height = 60.0
plate_thickness = 2.0

# Hole dimensions and position relative to center
hole_width = 12.0
hole_height = 6.0
hole_offset_x = 35.0  # Positive value shifts to the right
hole_offset_y = 0.0   # 0.0 keeps it vertically centered

# Create the model
# We use the XZ plane for the base box so the plate stands vertically
# matching the orientation in the provided image.
result = (
    cq.Workplane("XZ")
    .box(plate_length, plate_height, plate_thickness)
    .faces(">Y")              # Select the front face
    .workplane()              # Initialize a new workplane on the selected face
    .center(hole_offset_x, hole_offset_y) # Move local origin to hole position
    .rect(hole_width, hole_height)        # Sketch the rectangular hole profile
    .cutThruAll()             # Cut the geometry through the entire part
)
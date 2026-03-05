import cadquery as cq

# Parametric dimensions for the plate and holes
plate_width = 100.0
plate_height = 80.0
plate_thickness = 5.0
hole_diameter = 6.0

# Define hole positions relative to the center of the plate (0,0)
# Based on the image:
# - One hole near the top center
# - One hole near the top right
# - One hole on the right side, lower down
# This forms a right-angled triangle pattern
x_offset = plate_width * 0.35  # Position for right-side holes
y_top = plate_height * 0.3     # Position for top row holes
y_bottom = -plate_height * 0.2 # Position for bottom hole
x_center_ish = 0.0             # Position for the left-most hole

hole_locations = [
    (x_center_ish, y_top),    # Top-left (of the group)
    (x_offset, y_top),        # Top-right
    (x_offset, y_bottom)      # Bottom-right
]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)
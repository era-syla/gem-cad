import cadquery as cq

# Parametric dimensions
plate_length = 100.0  # Length of the rectangular plate
plate_width = 60.0    # Width of the rectangular plate
plate_thickness = 5.0 # Thickness of the plate

hole_diameter = 10.0  # Diameter of the corner hole
hole_margin_x = 10.0  # Distance from the edge (length-wise) to hole center
hole_margin_y = 10.0  # Distance from the edge (width-wise) to hole center

# Calculate hole position
# Assuming the plate is centered at (0,0), the corner would be at (length/2, width/2)
# We want the hole near one corner. Let's pick the top-right corner in the XY plane.
hole_x = (plate_length / 2.0) - hole_margin_x
hole_y = (plate_width / 2.0) - hole_margin_y

# Create the model
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_x, -hole_y)]) # Placing it in the bottom-right quadrant relative to center to match perspective
    .hole(hole_diameter)
)
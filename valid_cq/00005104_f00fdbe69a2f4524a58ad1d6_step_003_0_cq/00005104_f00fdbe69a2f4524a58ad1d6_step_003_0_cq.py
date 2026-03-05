import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Total width of the plate (X direction)
plate_height = 80.0  # Total height of the plate (Y direction)
plate_thickness = 10.0  # Thickness of the plate (Z direction)

hole_diameter = 40.0  # Diameter of the through-hole
# Position of the hole center relative to the center of the plate
# The hole is offset to the left in the image.
hole_center_x = -20.0 
hole_center_y = 0.0

# Create the base plate
# We start with a workplane on the XY plane
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .center(hole_center_x, hole_center_y)
    .hole(hole_diameter)
)
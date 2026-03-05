import cadquery as cq

# -- Parametric Dimensions --
length = 120.0       # Length of the rectangular plate
width = 50.0         # Height/Width of the plate
thickness = 15.0     # Thickness of the plate
hole_diameter = 4.0  # Diameter of the small hole

# Position of the hole (offset from the center)
# The hole is located towards the right side of the face
hole_x_offset = 40.0
hole_y_offset = 0.0

# -- Geometry Generation --
result = (
    cq.Workplane("XY")
    # Create the main rectangular prism centered at origin
    .box(length, width, thickness)
    # Select the top face (Z+) to sketch the hole on
    .faces(">Z")
    .workplane()
    # Move to the location of the hole
    .pushPoints([(hole_x_offset, hole_y_offset)])
    # Cut the through hole
    .hole(hole_diameter)
)
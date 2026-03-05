import cadquery as cq

# Parametric dimensions
# Main body (rectangular prism)
prism_width = 10.0
prism_height = 10.0
prism_length = 40.0

# Shaft (cylinder)
shaft_diameter = 6.0
shaft_length = 30.0

# Create the rectangular prism part
# We start by drawing a rectangle on the XY plane and extruding it
part1 = (
    cq.Workplane("XY")
    .rect(prism_width, prism_height)
    .extrude(prism_length)
)

# Create the cylindrical shaft part
# We select the face at the "bottom" (z=0) or "top" depending on orientation preference
# Here, let's select the face at Z=0 and extrude backwards for the shaft, 
# or select the far face and extrude forwards.
# To match the image where the shaft extends out from one end:
# We select the face at z=0 (the starting face of the extrusion)
# and extrude in the negative Z direction.
part2 = (
    part1.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# Combine into the final result
result = part2
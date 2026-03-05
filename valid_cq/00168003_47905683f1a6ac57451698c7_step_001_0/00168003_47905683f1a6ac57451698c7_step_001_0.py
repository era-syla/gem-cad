import cadquery as cq

# Parametric dimensions
length = 150.0       # Total length of the plate
width = 40.0         # Width of the plate
thickness = 3.0      # Thickness of the plate
hole_diameter = 8.0  # Diameter of the two holes
hole_margin = 20.0   # Distance from the center of the hole to the short edge

# Calculate the position of the holes along the X axis
# The box is centered at (0,0,0), so the ends are at +/- length/2
# We place holes inwards by 'hole_margin'
x_pos = (length / 2.0) - hole_margin

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-x_pos, 0), (x_pos, 0)])
    .hole(hole_diameter)
)
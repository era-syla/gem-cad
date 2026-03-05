import cadquery as cq

# Define parametric dimensions
length = 100.0   # Length of the part along the X axis
height = 50.0    # Height of the part along the Z axis
thickness = 10.0 # Thickness of the part along the Y axis

# Create the rectangular block
# We use the box operation to create the simple geometry
# The box is centered at the origin by default
result = cq.Workplane("XY").box(length, thickness, height)
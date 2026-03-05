import cadquery as cq

# Parametric dimensions for the rectangular box
length = 40.0  # Length along the X axis
width = 20.0   # Width along the Y axis
height = 10.0  # Height along the Z axis

# Create the rectangular box centered at the origin
result = cq.Workplane("XY").box(length, width, height)
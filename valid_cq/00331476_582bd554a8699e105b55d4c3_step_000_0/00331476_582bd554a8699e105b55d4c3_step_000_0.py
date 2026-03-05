import cadquery as cq

# Parametric dimensions for the rectangular box
length = 100.0  # Length along the X axis
width = 50.0    # Width along the Y axis
height = 30.0   # Height along the Z axis

# Create a solid rectangular box centered at the origin
result = cq.Workplane("XY").box(length, width, height)
import cadquery as cq

# Define parametric dimensions
length = 100.0   # Length along the X-axis
height = 30.0    # Height along the Z-axis
thickness = 2.0  # Thickness along the Y-axis

# Create the rectangular plate model
# We use the box operation to create a solid cuboid centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)
import cadquery as cq

# Parametric dimensions for the rectangular bar
length = 150.0   # Length along the X axis
height = 25.0    # Height along the Z axis
thickness = 3.0  # Thickness along the Y axis

# Create the rectangular prism (plate/bar)
# We create a box centered at the origin with the specified dimensions.
# This aligns with the isometric view where the object has length, height, and thin depth.
result = cq.Workplane("XY").box(length, thickness, height)
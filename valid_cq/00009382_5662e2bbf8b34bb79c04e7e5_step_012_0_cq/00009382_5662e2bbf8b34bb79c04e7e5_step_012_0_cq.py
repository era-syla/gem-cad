import cadquery as cq

# Parametric dimensions for the box
length = 50.0  # Length of the box (X-axis)
width = 30.0   # Width of the box (Y-axis)
height = 20.0  # Height of the box (Z-axis)

# Create a solid box centered on the XY plane but sitting on top of it (optional alignment)
# center=(True, True, False) centers it in X and Y, but starts Z from 0.
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
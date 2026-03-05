import cadquery as cq

# Define parametric dimensions
length = 100.0  # Dimension along the X-axis
width = 60.0    # Dimension along the Y-axis
height = 50.0   # Dimension along the Z-axis

# Create the box
# We center the box on the XY plane for convenience, but the Z starts from 0
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want it centered on all axes:
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, True))

# If you want it sitting on the "ground" (Z=0):
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
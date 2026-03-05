import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length along the X-axis
width = 60.0    # Width along the Y-axis
thickness = 2.0 # Thickness along the Z-axis

# Create the solid rectangular plate
# We use the box operation which creates a centered cuboid
result = cq.Workplane("XY").box(length, width, thickness)
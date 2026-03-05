import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length along the X axis
width = 50.0    # Width along the Y axis
thickness = 2.0 # Thickness along the Z axis

# Create a simple rectangular solid (box)
# .box() centers the geometry at the origin (0,0,0) by default
result = cq.Workplane("XY").box(length, width, thickness)
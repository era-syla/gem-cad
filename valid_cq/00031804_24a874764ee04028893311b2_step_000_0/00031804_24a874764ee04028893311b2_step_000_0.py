import cadquery as cq

# Define parameters for the rectangular plate
length = 120.0  # Length along the X axis
height = 25.0   # Height along the Z axis
thickness = 3.0 # Thickness along the Y axis

# Create the solid geometry
# We create a box centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)
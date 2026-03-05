import cadquery as cq

# Define parameters for the dimensions of the plate
length = 100.0  # Length along the X axis
width = 100.0   # Width along the Y axis
thickness = 5.0 # Thickness along the Z axis

# Create a simple rectangular solid (box)
# The box method creates a box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)
import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the solid geometry
# We create a workplane on the XY plane and generate a box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)
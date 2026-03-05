import cadquery as cq

# Define parameters for the dimensions of the cuboid
height = 100.0  # Total height of the object
width = 25.0    # Width of the object
depth = 12.5    # Depth/Thickness of the object

# Create a simple rectangular solid (box)
# We create a workplane on the XY plane and generate a box
# box(length, width, height) generates a box centered at the origin
result = cq.Workplane("XY").box(width, depth, height)
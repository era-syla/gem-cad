import cadquery as cq

# Define parametric dimensions
length = 200.0  # Total length of the strip
width = 10.0    # Width of the strip
thickness = 2.0 # Thickness of the strip

# Create the rectangular bar
# Using box() to create a simple rectangular prism centered at origin for symmetry,
# but can also be corner-based. Here, centering on X and Y makes sense.
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, using sketch-and-extrude for clarity:
# result = (
#     cq.Workplane("XY")
#     .rect(length, width)
#     .extrude(thickness)
# )
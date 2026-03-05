import cadquery as cq

# Define parameters for the strip
length = 100.0  # Length of the strip
width = 5.0     # Width of the strip
thickness = 1.0 # Thickness of the strip

# Create the solid geometry
# We start with a workplane (XY plane is standard)
# We create a rectangle centered at the origin
# Then we extrude it to create the thickness
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# Alternatively, using rectangle and extrude:
# result = (
#     cq.Workplane("XY")
#     .rect(length, width)
#     .extrude(thickness)
# )
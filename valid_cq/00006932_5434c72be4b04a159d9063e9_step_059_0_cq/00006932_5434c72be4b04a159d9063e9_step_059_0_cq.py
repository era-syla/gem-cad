import cadquery as cq

# Define dimensions
outer_diameter = 20.0  # Outer diameter of the tube
inner_diameter = 16.0  # Inner diameter of the tube
length = 100.0         # Length of the tube

# Create the tube
# We start with a workplane, draw two concentric circles, and extrude them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer circle
    .circle(inner_diameter / 2)  # Inner circle
    .extrude(length)
)

# Alternatively, one could use the difference operation:
# result = (
#     cq.Workplane("XY")
#     .circle(outer_diameter / 2)
#     .extrude(length)
#     .faces(">Z")
#     .hole(inner_diameter)
# )

# The result variable now contains the 3D geometry